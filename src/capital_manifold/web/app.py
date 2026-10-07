"""Capital Manifold: Institutional Planetary Liquidity & Balance-Sheet Graph Engine API.

Provides institutional REST API endpoints and static assets serving the Palantir / Bloomberg / Linear
financial engineering dashboard. Visualizes the 4-tier monetary manifold, live adversarial audit scorecard,
systemic shock simulation gauntlet, Desk Master private asset portfolios, and DuckDB flow events explorer.
"""

from __future__ import annotations

import json
import logging
import math
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import duckdb
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from capital_manifold.adversarial.adversarial_substrate import (
    AdversarialSubstrateBuilder,
    EntityCategory,
)
from capital_manifold.bridge.pgm_adapter import (
    FINANCIAL_ENTITIES,
    ManifoldPGMBridge,
    MonetaryTier,
)
from capital_manifold.simulation.stress_gauntlet import (
    GauntletRegimeResult,
    StressGauntletEngine,
)

logger = logging.getLogger("capital_manifold.web")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
DUCKDB_PATH = DATA_DIR / "cache" / "manifold.duckdb"
STATIC_DIR = Path(__file__).resolve().parent / "static"

TIER_NAMES = {
    0: "Tier 0: Sovereign Genesis",
    1: "Tier 1: Transmission Dealers & Central Banks",
    2: "Tier 2: Interbank Traversal & Clearing Pools",
    3: "Tier 3: Safe-Haven & Monetary Sinks",
}

DATA_SOURCE_BADGES = {
    "ecb": "ECB",
    "target2": "ECB",
    "banque_de_france": "BDF",
    "bundesbank": "BUBA",
    "tresor": "AFT",
    "agence_france_tresor": "AFT",
    "insee": "INSEE",
    "us_treasury": "DTS",
    "dts": "DTS",
    "federal_reserve": "FED",
    "fed": "FED",
    "dtcc": "DTCC",
    "bis": "BIS",
    "sec": "SEC",
    "edgar": "SEC",
    "family_office": "DESK",
    "private": "DESK",
    "launchfizz": "OPCO",
    "vesperspatial": "ACTUARIAL",
    "silvera": "OPCO",
    "scientific": "FLEET",
    "valle_rd": "LEDGER",
    "maritime": "AIS",
    "tanker": "AIS",
    "pboc": "PBOC",
    "boj": "BOJ",
    "cbr": "CBR",
    "rbi": "RBI",
}


def get_provenance_badge(data_source: str) -> str:
    """Extracts a short institutional badge string from data_source."""
    ds = data_source.lower()
    for key, badge in DATA_SOURCE_BADGES.items():
        if key in ds:
            return badge
    return "DTCC" if "repo" in ds else "SYSTEM"


# =============================================================================
# Global Application State & Singletons
# =============================================================================

class AppState:
    bridge: Optional[ManifoldPGMBridge] = None
    builder: Optional[AdversarialSubstrateBuilder] = None
    gauntlet_engine: Optional[StressGauntletEngine] = None
    cached_topology: Optional[Dict[str, Any]] = None
    cached_pools: Optional[List[Dict[str, Any]]] = None


state = AppState()


def get_bridge() -> ManifoldPGMBridge:
    if state.bridge is None:
        logger.info("Initializing ManifoldPGMBridge singleton...")
        state.bridge = ManifoldPGMBridge(
            parquet_dir=PROCESSED_DIR,
            duckdb_path=DUCKDB_PATH,
        )
    return state.bridge


def get_builder() -> AdversarialSubstrateBuilder:
    if state.builder is None:
        logger.info("Initializing AdversarialSubstrateBuilder singleton...")
        state.builder = AdversarialSubstrateBuilder()
    return state.builder


def get_gauntlet_engine() -> StressGauntletEngine:
    if state.gauntlet_engine is None:
        logger.info("Initializing StressGauntletEngine singleton...")
        state.gauntlet_engine = StressGauntletEngine(bridge=get_bridge())
    return state.gauntlet_engine


def get_duckdb_con() -> duckdb.DuckDBPyConnection:
    """Returns a read-only DuckDB connection."""
    if not DUCKDB_PATH.exists():
        raise HTTPException(status_code=503, detail=f"DuckDB database not found at {DUCKDB_PATH}")
    return duckdb.connect(str(DUCKDB_PATH), read_only=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to pre-warm singletons and cached topology."""
    logger.info("Starting Capital Manifold Web Application...")
    try:
        get_bridge()
        get_builder()
        get_gauntlet_engine()
        build_cached_topology()
        logger.info("Singletons initialized successfully.")
    except Exception as e:
        logger.warning(f"Error during pre-warming singletons: {e}")
    yield
    logger.info("Shutting down Capital Manifold Web Application...")


app = FastAPI(
    title="Capital Manifold: Institutional Planetary Liquidity & Balance-Sheet Graph Engine",
    description="Live financial engineering dashboard and macro-financial balance-sheet network explorer.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Helper: Graph Topology Construction & Harmonization
# =============================================================================

def build_cached_topology() -> Dict[str, Any]:
    """Extracts, merges, and harmonizes the 140-node 317-edge balance sheet graph."""
    if state.cached_topology is not None:
        return state.cached_topology

    bridge = get_bridge()
    builder = get_builder()
    adv_sub, adv_metrics = builder.build_adversarial_substrate()

    all_entity_ids = sorted(list(set(bridge.substrate.entities.keys()) | set(adv_sub.entities.keys())))

    # Tier assignment and coordinates
    nodes: List[Dict[str, Any]] = []
    pools_summary: List[Dict[str, Any]] = []
    tier_counts = {0: 0, 1: 0, 2: 0, 3: 0}

    # First pass: assign tier to each entity
    entity_tiers: Dict[str, int] = {}
    for eid in all_entity_ids:
        if eid in FINANCIAL_ENTITIES:
            t = int(FINANCIAL_ENTITIES[eid]["tier"])
        elif eid in builder.entity_categories:
            cat = builder.entity_categories[eid]
            if cat == EntityCategory.SOVEREIGN_ISSUER:
                t = 0
            elif cat in (EntityCategory.CENTRAL_BANK, EntityCategory.SVT_PRIMARY_DEALER):
                t = 1
            elif cat == EntityCategory.SAFE_HAVEN_ANCHOR:
                t = 3
            else:
                t = 2
        else:
            t = 2
        entity_tiers[eid] = t
        tier_counts[t] += 1

    # Tier X coordinates
    tier_x_coords = {
        0: 120,    # Sovereign Genesis
        1: 520,    # Transmission Dealers & Central Banks
        2: 980,    # Interbank Traversal & Clearing
        3: 1440,   # Monetary Sinks & Collateral Anchors
    }

    tier_y_tracker = {0: 0, 1: 0, 2: 0, 3: 0}
    tier_y_spacing = {0: 95, 1: 52, 2: 30, 3: 65}

    for eid in all_entity_ids:
        t = entity_tiers[eid]
        y_pos = 80 + (tier_y_tracker[t] * tier_y_spacing[t])
        x_pos = tier_x_coords[t]
        tier_y_tracker[t] += 1

        # Determine name, sector, jurisdiction, description
        if eid in FINANCIAL_ENTITIES:
            spec = FINANCIAL_ENTITIES[eid]
            name = spec.get("name", eid.replace("_", " ").title())
            sector = spec.get("sector", "financial_institution")
            jurisdiction = spec.get("jurisdiction", "US")
            description = spec.get("description", "")
            is_decoy = False
        elif eid in adv_sub.entities:
            meta = adv_sub.entities[eid].metadata
            cat = meta.get("category", "decoy_financial")
            name = eid.replace("_", " ").title()
            sector = cat
            jurisdiction = "FR_EU" if "french" in eid or "paris" in eid or "lyon" in eid else "GLOBAL"
            description = f"Institutional entity classified under {cat.replace('_', ' ')}."
            is_decoy = "decoy" in cat
        else:
            name = eid.replace("_", " ").title()
            sector = "market_participant"
            jurisdiction = "GLOBAL"
            description = "Capital flow counterparty pool."
            is_decoy = False

        metrics_obj = adv_metrics.get(eid)
        metrics_dict = metrics_obj.__dict__ if metrics_obj else {}

        node_data = {
            "id": eid,
            "label": name,
            "name": name,
            "tier": t,
            "tier_label": TIER_NAMES.get(t, f"Tier {t}"),
            "sector": sector,
            "jurisdiction": jurisdiction,
            "description": description,
            "is_decoy": is_decoy,
            "metrics": metrics_dict,
        }

        nodes.append({
            "data": node_data,
            "position": {"x": x_pos, "y": y_pos},
        })

        pools_summary.append({
            "id": eid,
            "name": name,
            "tier": t,
            "tier_label": TIER_NAMES.get(t, f"Tier {t}"),
            "sector": sector,
            "jurisdiction": jurisdiction,
            "description": description,
            "is_decoy": is_decoy,
            "metrics": metrics_dict,
        })

    # Edges merge
    edges: List[Dict[str, Any]] = []
    seen_edges = set()

    # Collect from bridge
    for u, targets in bridge.substrate.adjacency.items():
        for v, elist in targets.items():
            for e in elist:
                key = (u, v, e.relation)
                if key not in seen_edges:
                    seen_edges.add(key)
                    meta = e.metadata or {}
                    vol_usd = (
                        meta.get("volume_usd")
                        or meta.get("nominal_usd")
                        or meta.get("syndicate_volume_eur", 0.0) * 1.09
                        or meta.get("sponsored_repo_volume_usd")
                        or meta.get("frozen_reserves_usd")
                        or 0.0
                    )
                    is_bypass = meta.get("bypass", False) or "bypass" in e.relation
                    edges.append({
                        "data": {
                            "id": f"{u}->{v}:{e.relation}",
                            "source": u,
                            "target": v,
                            "relation": e.relation,
                            "label": e.relation.replace("_", " "),
                            "weight": round(float(e.weight), 4),
                            "volume_usd": float(vol_usd),
                            "is_bypass": bool(is_bypass),
                            "metadata": meta,
                        }
                    })

    # Collect from adv_sub
    for u, targets in adv_sub.adjacency.items():
        for v, elist in targets.items():
            for e in elist:
                key = (u, v, e.relation)
                if key not in seen_edges:
                    seen_edges.add(key)
                    meta = e.metadata or {}
                    vol_usd = meta.get("volume_usd", 0.0)
                    is_bypass = meta.get("bypass", False)
                    edges.append({
                        "data": {
                            "id": f"{u}->{v}:{e.relation}",
                            "source": u,
                            "target": v,
                            "relation": e.relation,
                            "label": e.relation.replace("_", " "),
                            "weight": round(float(e.weight), 4),
                            "volume_usd": float(vol_usd),
                            "is_bypass": bool(is_bypass),
                            "metadata": meta,
                        }
                    })

    topology = {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "tiers": {
            "genesis": tier_counts[0],
            "transmission": tier_counts[1],
            "traversal": tier_counts[2],
            "sink": tier_counts[3],
        },
        "elements": {
            "nodes": nodes,
            "edges": edges,
        },
    }

    state.cached_topology = topology
    state.cached_pools = pools_summary
    return topology


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/api/health")
def get_health() -> Dict[str, Any]:
    """Health status, database connection, node count, and runtime diagnostics."""
    db_connected = False
    flow_count = 0
    stress_count = 0
    db_error = None

    try:
        con = get_duckdb_con()
        flow_count = con.execute("SELECT count(*) FROM flow_events").fetchone()[0]
        stress_count = con.execute("SELECT count(*) FROM macro_stress_snapshots").fetchone()[0]
        con.close()
        db_connected = True
    except Exception as ex:
        db_error = str(ex)

    topo = build_cached_topology()

    return {
        "status": "healthy" if db_connected else "degraded",
        "service": "Capital Manifold Planetary Web Engine",
        "version": "0.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": {
            "connected": db_connected,
            "path": str(DUCKDB_PATH),
            "flow_events_count": flow_count,
            "stress_snapshots_count": stress_count,
            "error": db_error,
        },
        "topology": {
            "node_count": topo["node_count"],
            "edge_count": topo["edge_count"],
            "tiers": topo["tiers"],
        },
    }


@app.get("/api/scorecard")
def get_scorecard() -> Dict[str, Any]:
    """Loads audit_scorecard.json (Integrity score 90.8/100, 5 category scores, anomalies)."""
    scorecard_path = PROCESSED_DIR / "audit_scorecard.json"
    if scorecard_path.exists():
        try:
            with open(scorecard_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.warning(f"Could not read scorecard file: {e}")

    # Fallback to direct auditor execution
    from capital_manifold.adversarial.system_auditor import SystemAuditor
    auditor = SystemAuditor(duckdb_path=DUCKDB_PATH)
    sc = auditor.run_full_audit()
    return sc.to_dict()


@app.get("/api/topology")
def get_topology() -> Dict[str, Any]:
    """Exports full 140-node 317-edge balance-sheet graph formatted for Cytoscape.js."""
    return build_cached_topology()


@app.get("/api/flows")
def get_flows(
    currency: Optional[str] = Query(None, description="Currency filter (e.g. USD, EUR)"),
    tier: Optional[int] = Query(None, description="Node tier filter (0 to 3)"),
    flow_type: Optional[str] = Query(None, description="FlowType enum string"),
    source: Optional[str] = Query(None, description="Source entity ID filter"),
    target: Optional[str] = Query(None, description="Target entity ID filter"),
    jurisdiction: Optional[str] = Query(None, description="Source or target jurisdiction filter"),
    search: Optional[str] = Query(None, description="Text search filter across entities and instruments"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> Dict[str, Any]:
    """Queries flow_events table in DuckDB with rich filtering and annualized velocity metrics."""
    con = get_duckdb_con()
    try:
        where_clauses: List[str] = []
        params: List[Any] = []

        if currency:
            where_clauses.append("currency = ?")
            params.append(currency.upper())

        if flow_type:
            where_clauses.append("flow_type = ?")
            params.append(flow_type)

        if source:
            where_clauses.append("source_entity = ?")
            params.append(source)

        if target:
            where_clauses.append("target_entity = ?")
            params.append(target)

        if jurisdiction:
            where_clauses.append("(source_jurisdiction = ? OR target_jurisdiction = ?)")
            params.extend([jurisdiction.upper(), jurisdiction.upper()])

        if search:
            search_pattern = f"%{search.lower()}%"
            where_clauses.append(
                "(lower(source_entity) LIKE ? OR lower(target_entity) LIKE ? OR lower(instrument) LIKE ? OR lower(data_source) LIKE ?)"
            )
            params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

        where_stmt = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        # Total count
        count_query = f"SELECT count(*) FROM flow_events{where_stmt}"
        total_count = con.execute(count_query, params).fetchone()[0]

        # Paginated fetch
        query = f"""
            SELECT
                event_id,
                timestamp,
                period_label,
                source_entity,
                source_jurisdiction,
                target_entity,
                target_jurisdiction,
                instrument,
                nominal_amount,
                currency,
                amount_usd_normalized,
                flow_type,
                velocity_turnover_days,
                data_source,
                source_line_item,
                confidence,
                metric_value
            FROM flow_events
            {where_stmt}
            ORDER BY timestamp DESC, amount_usd_normalized DESC
            LIMIT ? OFFSET ?
        """
        rows = con.execute(query, params + [limit, offset]).fetchall()
        cols = [
            "event_id", "timestamp", "period_label", "source_entity",
            "source_jurisdiction", "target_entity", "target_jurisdiction",
            "instrument", "nominal_amount", "currency", "amount_usd_normalized",
            "flow_type", "velocity_turnover_days", "data_source",
            "source_line_item", "confidence", "metric_value",
        ]

        flows: List[Dict[str, Any]] = []
        for r in rows:
            f_dict = dict(zip(cols, r))
            nominal = float(f_dict["nominal_amount"])
            vel = f_dict["velocity_turnover_days"]
            vel_days = float(vel) if vel is not None and not math.isnan(float(vel)) else None

            # Annualized rate calculation
            if vel_days and vel_days > 0:
                annualized_usd = f_dict["amount_usd_normalized"] * (365.0 / vel_days)
            else:
                annualized_usd = f_dict["amount_usd_normalized"]

            f_dict["annualized_rate_usd"] = round(annualized_usd, 2)
            f_dict["provenance_badge"] = get_provenance_badge(f_dict["data_source"])
            flows.append(f_dict)

        return {
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "flows": flows,
        }
    finally:
        con.close()


@app.get("/api/stress_snapshots")
def get_stress_snapshots() -> List[Dict[str, Any]]:
    """Queries macro_stress_snapshots from DuckDB."""
    con = get_duckdb_con()
    try:
        rows = con.execute("SELECT * FROM macro_stress_snapshots ORDER BY timestamp DESC").fetchall()
        desc = [d[0] for d in con.description]
        snapshots = []
        for r in rows:
            snapshots.append(dict(zip(desc, r)))
        return snapshots
    finally:
        con.close()


class SimulateRequest(BaseModel):
    regime: int = Field(..., ge=1, le=3, description="Crisis regime number: 1, 2, or 3")


@app.post("/api/simulate")
def post_simulate(req: SimulateRequest) -> Dict[str, Any]:
    """Accepts regime (1, 2, or 3), executes StressGauntletEngine, and returns comparative telemetry."""
    engine = get_gauntlet_engine()

    try:
        if req.regime == 1:
            result = engine.run_regime_1_sovereign_blowout()
        elif req.regime == 2:
            result = engine.run_regime_2_dollar_freeze()
        elif req.regime == 3:
            result = engine.run_regime_3_compound_super_crisis()
        else:
            raise HTTPException(status_code=400, detail="Invalid regime. Choose 1, 2, or 3.")

        return result.to_dict()
    except Exception as ex:
        logger.error(f"Error during simulation gauntlet regime {req.regime}: {ex}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(ex))



# =============================================================================
# User-Requested Explorer Endpoints: Pools, Deep Pool Inspection, Paths, Circuits
# =============================================================================

@app.get("/api/pools")
def get_pools(
    tier: Optional[int] = Query(None, description="Tier filter (0, 1, 2, 3)"),
    search: Optional[str] = Query(None, description="Search term for name or ID"),
) -> List[Dict[str, Any]]:
    """Returns structured list of all 140 capital pools with aggregated inflow/outflow and graph neighbors."""
    topo = build_cached_topology()
    nodes = topo["elements"]["nodes"]
    edges = topo["elements"]["edges"]

    # Calculate upstream and downstream adjacency
    upstream_map: Dict[str, List[Dict[str, Any]]] = {}
    downstream_map: Dict[str, List[Dict[str, Any]]] = {}

    for e in edges:
        s = e["data"]["source"]
        t = e["data"]["target"]
        rel = e["data"]["relation"]
        w = e["data"]["weight"]

        if s not in downstream_map:
            downstream_map[s] = []
        downstream_map[s].append({"id": t, "relation": rel, "weight": w})

        if t not in upstream_map:
            upstream_map[t] = []
        upstream_map[t].append({"id": s, "relation": rel, "weight": w})

    # Query flow volume totals per pool from DuckDB
    con = get_duckdb_con()
    inflow_totals: Dict[str, float] = {}
    outflow_totals: Dict[str, float] = {}
    event_counts: Dict[str, int] = {}

    try:
        inflows = con.execute(
            "SELECT target_entity, sum(amount_usd_normalized), count(*) FROM flow_events GROUP BY target_entity"
        ).fetchall()
        for tgt, sum_val, cnt in inflows:
            inflow_totals[tgt] = float(sum_val or 0.0)
            event_counts[tgt] = event_counts.get(tgt, 0) + cnt

        outflows = con.execute(
            "SELECT source_entity, sum(amount_usd_normalized), count(*) FROM flow_events GROUP BY source_entity"
        ).fetchall()
        for src, sum_val, cnt in outflows:
            outflow_totals[src] = float(sum_val or 0.0)
            event_counts[src] = event_counts.get(src, 0) + cnt
    finally:
        con.close()

    pools: List[Dict[str, Any]] = []
    for n in nodes:
        d = n["data"]
        eid = d["id"]

        if tier is not None and d["tier"] != tier:
            continue
        if search and (search.lower() not in eid.lower() and search.lower() not in d["name"].lower()):
            continue

        in_usd = inflow_totals.get(eid, 0.0)
        out_usd = outflow_totals.get(eid, 0.0)
        net_usd = in_usd - out_usd

        if in_usd == 0.0 and out_usd > 0.0:
            role = "source"
        elif out_usd == 0.0 and in_usd > 0.0:
            role = "sink"
        else:
            role = "conduit"

        pools.append({
            "id": eid,
            "name": d["name"],
            "tier": d["tier"],
            "tier_label": d["tier_label"],
            "sector": d["sector"],
            "jurisdiction": d["jurisdiction"],
            "description": d["description"],
            "is_decoy": d["is_decoy"],
            "role": role,
            "inflow_usd": in_usd,
            "outflow_usd": out_usd,
            "net_flow_usd": net_usd,
            "flow_event_count": event_counts.get(eid, 0),
            "upstream_count": len(upstream_map.get(eid, [])),
            "downstream_count": len(downstream_map.get(eid, [])),
            "upstream_sources": upstream_map.get(eid, [])[:6],
            "downstream_destinations": downstream_map.get(eid, [])[:6],
            "metrics": d.get("metrics", {}),
        })

    return pools


@app.get("/api/pools/{pool_id}")
def get_pool_detail(pool_id: str) -> Dict[str, Any]:
    """Deep-dive breakdown for an individual capital pool / balance sheet node."""
    topo = build_cached_topology()
    matching_node = next((n for n in topo["elements"]["nodes"] if n["data"]["id"] == pool_id), None)
    if not matching_node:
        raise HTTPException(status_code=404, detail=f"Pool '{pool_id}' not found in manifold topology.")

    node_data = matching_node["data"]

    # Neighbors
    edges = topo["elements"]["edges"]
    upstream = [e["data"] for e in edges if e["data"]["target"] == pool_id]
    downstream = [e["data"] for e in edges if e["data"]["source"] == pool_id]

    # DuckDB flows
    con = get_duckdb_con()
    try:
        inbound_rows = con.execute(
            """SELECT event_id, timestamp, source_entity, source_jurisdiction, instrument,
                      nominal_amount, currency, amount_usd_normalized, flow_type, data_source
               FROM flow_events WHERE target_entity = ?
               ORDER BY amount_usd_normalized DESC""",
            [pool_id],
        ).fetchall()
        inbound_cols = ["event_id", "timestamp", "source_entity", "source_jurisdiction", "instrument",
                        "nominal_amount", "currency", "amount_usd_normalized", "flow_type", "data_source"]
        inbound_flows = [dict(zip(inbound_cols, r)) for r in inbound_rows]

        outbound_rows = con.execute(
            """SELECT event_id, timestamp, target_entity, target_jurisdiction, instrument,
                      nominal_amount, currency, amount_usd_normalized, flow_type, data_source
               FROM flow_events WHERE source_entity = ?
               ORDER BY amount_usd_normalized DESC""",
            [pool_id],
        ).fetchall()
        outbound_cols = ["event_id", "timestamp", "target_entity", "target_jurisdiction", "instrument",
                         "nominal_amount", "currency", "amount_usd_normalized", "flow_type", "data_source"]
        outbound_flows = [dict(zip(outbound_cols, r)) for r in outbound_rows]
    finally:
        con.close()

    total_in_usd = sum(f["amount_usd_normalized"] for f in inbound_flows)
    total_out_usd = sum(f["amount_usd_normalized"] for f in outbound_flows)
    net_usd = total_in_usd - total_out_usd

    if abs(net_usd) < 1e-4 and total_in_usd > 0:
        conservation_status = "strictly_conserved_conduit"
    elif total_in_usd == 0 and total_out_usd > 0:
        conservation_status = "sovereign_faucet_genesis"
    elif total_out_usd == 0 and total_in_usd > 0:
        conservation_status = "accumulating_monetary_sink"
    else:
        conservation_status = "active_financial_intermediary"

    return {
        "pool": node_data,
        "conservation_status": conservation_status,
        "totals": {
            "inflow_usd": total_in_usd,
            "outflow_usd": total_out_usd,
            "net_usd": net_usd,
            "inbound_flow_count": len(inbound_flows),
            "outbound_flow_count": len(outbound_flows),
        },
        "upstream_neighbors": upstream,
        "downstream_neighbors": downstream,
        "inbound_flows": inbound_flows,
        "outbound_flows": outbound_flows,
    }


@app.get("/api/paths")
def get_discovered_path(
    source_id: str = Query(..., description="Originating capital pool / entity ID"),
    target_id: str = Query(..., description="Destination capital pool / entity ID"),
) -> Dict[str, Any]:
    """Path discovery between two pools executing Dual-Frontier A* algorithm."""
    engine = get_gauntlet_engine()
    proc_engine = engine.engine

    # Check existence
    sub = engine.base_substrate
    if source_id not in sub.entities:
        raise HTTPException(status_code=404, detail=f"Source entity '{source_id}' does not exist in graph.")
    if target_id not in sub.entities:
        raise HTTPException(status_code=404, detail=f"Target entity '{target_id}' does not exist in graph.")

    result = proc_engine.query_reasoning_corridor(source_id, target_id)

    topo = build_cached_topology()
    nodes_by_id = {n["data"]["id"]: n["data"] for n in topo["elements"]["nodes"]}

    if not result.success:
        import networkx as nx
        G = nx.DiGraph()
        for e in topo["elements"]["edges"]:
            d = e["data"]
            G.add_edge(d["source"], d["target"], weight=float(d.get("weight", 1.0)), relation=d.get("relation", "capital_flow"))
        if nx.has_path(G, source_id, target_id):
            p_nodes = nx.shortest_path(G, source_id, target_id, weight="weight")
            p_edges = []
            cost_sum = 0.0
            for i in range(len(p_nodes) - 1):
                u = p_nodes[i]
                v = p_nodes[i + 1]
                ed = G[u][v]
                w = float(ed.get("weight", 1.0))
                sc = round(1.0 / max(0.01, w), 4)
                cost_sum += sc
                p_edges.append({
                    "source": u,
                    "target": v,
                    "relation": ed.get("relation", "capital_flow"),
                    "weight": round(w, 4),
                    "step_cost": sc,
                })
            bypasses = [nid for nid in p_nodes if any(k in nid for k in ("natixis", "sponsored_repo", "standing_repo", "bypass"))]
            hop_details = []
            for nid in p_nodes:
                if nid in nodes_by_id:
                    hop_details.append({
                        "id": nid,
                        "name": nodes_by_id[nid]["name"],
                        "tier": nodes_by_id[nid]["tier"],
                        "sector": nodes_by_id[nid]["sector"],
                        "jurisdiction": nodes_by_id[nid]["jurisdiction"],
                    })
                else:
                    hop_details.append({
                        "id": nid,
                        "name": nid.replace("_", " ").title(),
                        "tier": 2,
                        "sector": "financial_conduit",
                        "jurisdiction": "GLOBAL",
                    })
            return {
                "success": True,
                "source_id": source_id,
                "target_id": target_id,
                "total_cost": round(cost_sum, 4),
                "hops": len(p_nodes),
                "path_nodes": p_nodes,
                "path_edges": p_edges,
                "bypasses_used": bypasses,
                "hop_details": hop_details,
            }

    bypasses = [nid for nid in result.path_nodes if any(k in nid for k in ("natixis", "sponsored_repo", "standing_repo", "bypass"))]
    hop_details = []
    for nid in result.path_nodes:
        if nid in nodes_by_id:
            hop_details.append({
                "id": nid,
                "name": nodes_by_id[nid]["name"],
                "tier": nodes_by_id[nid]["tier"],
                "sector": nodes_by_id[nid]["sector"],
                "jurisdiction": nodes_by_id[nid]["jurisdiction"],
            })
        else:
            hop_details.append({
                "id": nid,
                "name": nid.replace("_", " ").title(),
                "tier": 2,
                "sector": "financial_conduit",
                "jurisdiction": "GLOBAL",
            })

    edges_formatted = []
    for e in result.path_edges:
        edges_formatted.append({
            "source": e.source_id,
            "target": e.target_id,
            "relation": e.relation,
            "weight": round(float(e.weight), 4),
            "step_cost": round(1.0 / max(0.01, float(e.weight)), 4),
        })

    return {
        "success": result.success,
        "source_id": source_id,
        "target_id": target_id,
        "total_cost": round(float(result.total_cost), 4) if not math.isinf(result.total_cost) else None,
        "hops": len(result.path_nodes),
        "path_nodes": result.path_nodes,
        "path_edges": edges_formatted,
        "bypasses_used": bypasses,
        "hop_details": hop_details,
    }


@app.get("/api/circuits")
@app.get("/api/circuits/featured")
def get_featured_circuits() -> List[Dict[str, Any]]:
    """Curated institutional circuits for instant one-click graph animation and synchronized inspection."""
    return [
        {
            "id": "CIRCUIT-01-OAT-BUND",
            "title": "French Sovereign OAT to German Bund Safe-Haven Flight",
            "subtitle": "Eurozone sovereign yield curve flight through SVT primary dealers and TARGET2 clearing",
            "source_id": "french_republic_tresor",
            "target_id": "bund_risk_free_anchor",
            "macro_theme": "European Sovereign Spread Crisis & TARGET2 Imbalance",
            "description": "Traces French Treasury primary bond issuance into SVT primary dealers (BNP/SocGen), clearing across the Eurosystem TARGET2 RTGS pool into the German Bund risk-free anchor.",
            "regime_link": 1,
            "key_nodes": [
                "french_republic_tresor",
                "svt_dealers_bnp_socgen",
                "french_republic_oat_market",
                "banque_de_france",
                "eurosystem_target2_pool",
                "bundesbank",
                "bund_risk_free_anchor",
            ],
        },
        {
            "id": "CIRCUIT-02-YEN-CARRY",
            "title": "Japanese Institutional Carry Trade to US Treasury Repo",
            "subtitle": "BoJ zero-interest liquidity crossing offshore FX basis swaps into DTCC Triparty repo",
            "source_id": "japan_institutional_carry_desk",
            "target_id": "us_treasury_tga",
            "macro_theme": "Transatlantic & Transpacific Dollar Funding Nexus",
            "description": "Traces Japanese institutional carry capital funded in yen, swapped synthetically into dollars via offshore FX desks, clearing through the $3T/day US Triparty repo basin into the Treasury General Account.",
            "regime_link": 2,
            "key_nodes": [
                "japan_institutional_carry_desk",
                "offshore_fx_swap_desk",
                "us_triparty_repo_pool",
                "us_treasury_tga",
            ],
        },
        {
            "id": "CIRCUIT-03-QT-BURN",
            "title": "Federal Reserve SOMA QT Money Burn Chamber",
            "subtitle": "Permanent base-money destruction via maturing Treasury runoff and ON RRP drainage",
            "source_id": "us_corporate_and_household_borrowers",
            "target_id": "fed_soma_qt_burn_chamber",
            "macro_theme": "Central Bank Balance Sheet Contraction",
            "description": "Visualizes the QT runoff circuit where non-financial debt service and Treasury redemptions result in literal destruction of central bank base money ($2.157T burned).",
            "regime_link": 2,
            "key_nodes": [
                "us_corporate_and_household_borrowers",
                "us_commercial_bank_credit_pool",
                "us_treasury_tga",
                "fed_soma_qt_burn_chamber",
            ],
        },
        {
            "id": "CIRCUIT-04-SHADOW-CRUDE",
            "title": "Eurasian Shadow Crude Maritime Energy Arbitrage",
            "subtitle": "Russian Urals crude via dark maritime fleet to Indian refining and European diesel imports",
            "source_id": "bank_of_russia_cbr_vault",
            "target_id": "french_economy_importers",
            "macro_theme": "Sanctions Arbitrage & Hydrocarbon Rerouting",
            "description": "Models Russian crude petroleum flows bypassing G7 price caps via shadow tankers, refined into clean diesel in Gujarat, India, and re-imported into the French real economy.",
            "regime_link": 3,
            "key_nodes": [
                "bank_of_russia_cbr_vault",
                "shadow_tanker_energy_arbitrage",
                "reserve_bank_of_india_refining_hub",
                "french_economy_importers",
            ],
        },
        {
            "id": "CIRCUIT-05-TECH-BUYBACK",
            "title": "Apple BigTech Cash Hoard & Equity Buyback Chamber",
            "subtitle": "Global consumer and enterprise tech revenue swept into equity share retirement",
            "source_id": "global_enterprise_tech_buyers",
            "target_id": "corporate_share_buyback_burn_chamber",
            "macro_theme": "Corporate Liquidity Hoarding & Financial Engineering",
            "description": "Traces global software and hardware expenditures flowing into Apple's offshore cash vaults, which are channeled directly into open-market share repurchases, retiring equity capital.",
            "regime_link": None,
            "key_nodes": [
                "global_enterprise_tech_buyers",
                "apple_bigtech_treasury_vault",
                "corporate_share_buyback_burn_chamber",
            ],
        },
        {
            "id": "CIRCUIT-06-GULF-PETRODOLLAR",
            "title": "Gulf Petrodollar Sovereign Wealth Recycling",
            "subtitle": "Hydrocarbon revenues accumulated into sovereign wealth funds and recycled into Western capital anchors",
            "source_id": "gulf_petrodollar_sovereign_wealth_basin",
            "target_id": "french_republic_oat_market",
            "macro_theme": "Planetary Petrodollar Recycling",
            "description": "Traces crude oil dollar revenues flowing from Saudi SAMA/PIF and UAE Mubadala basins through cross-border clearing into European sovereign debt and global capital anchors.",
            "regime_link": None,
            "key_nodes": [
                "saudi_sama_pif_nexus",
                "uae_adia_mubadala_basin",
                "gulf_petrodollar_sovereign_wealth_basin",
                "french_republic_oat_market",
            ],
        },
        {
            "id": "CIRCUIT-07-CHINA-PETROYUAN-CIPS",
            "title": "China Petro-Yuan CIPS & Sovereign FX Reserve Recycling",
            "subtitle": "$3.24T PBOC FX reserves, $550B bilateral swap network, and cross-border renminbi clearing",
            "source_id": "saudi_sama_pif_nexus",
            "target_id": "pboc_safe_foreign_reserves",
            "macro_theme": "Cross-Border De-Dollarization & Sovereign Reserve Recycling",
            "description": "Traces bilateral crude oil trade settled in non-USD renminbi via the Shanghai Petroleum Exchange (SHPGX), traversing the Hong Kong offshore CNH clearing hub and Chinese Big 4 state-bank trading desks (ICBC/CCB/BoC/ABC) into the People's Bank of China & SAFE sovereign reserve vaults ($3.24T), backed by a $550B bilateral central bank swap network.",
            "regime_link": None,
            "key_nodes": [
                "saudi_sama_pif_nexus",
                "petro_yuan_bilateral_settlement_bridge",
                "offshore_cnh_hong_kong_hub",
                "chinese_state_banks_fx_desk",
                "pboc_safe_foreign_reserves",
                "pboc_bilateral_swap_network",
            ],
        },
        {
            "id": "CIRCUIT-08-DARK-MATTER",
            "title": "Global Macro Dark Matter (BIS OTC Derivatives & Shadow Banking)",
            "subtitle": "$600 Trillion unmodeled derivative notional and Treasury basis trade leverage",
            "source_id": "bis_otc_derivatives_dark_matter",
            "target_id": "global_systemic_bank_nexus",
            "macro_theme": "Off-Balance-Sheet Systemic Blindspots",
            "description": "Exposes the enormous $600T unmodeled OTC derivatives universe, non-centrally cleared bilateral repos, and hedge fund basis trade leverage that evade conventional balance-sheet metrics.",
            "regime_link": None,
            "key_nodes": [
                "bis_otc_derivatives_dark_matter",
                "hedge_fund_basis_trade_leverage",
                "global_systemic_bank_nexus",
            ],
        },
    ]


# =============================================================================
# Serve Frontend Static Assets
# =============================================================================

@app.get("/")
def serve_root():
    """Serves the main dashboard HTML."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Capital Manifold Web API is live. Static index.html not yet created."}


# Mount static directory for JS/CSS assets
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
