"""Capital Manifold <-> Procedural Graph Engine (pgm-engine) Bridge Adapter.

Translates macro-financial FlowEvents and MacroStressSnapshots into PGM Engine's
EntityNode and EdgeRelation substrate, constructs 128-dimensional financial embeddings,
establishes 4-tier monetary landmark scaffolding, and orchestrates non-greedy
Dual-Frontier A* path discovery to trace capital flight and sovereign debt transmission.
"""

from __future__ import annotations

import logging
import math
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import duckdb
import numpy as np

from capital_manifold.core.schema import FlowEvent, FlowType, MacroStressSnapshot
from pgm_engine.engine import ProceduralGraphEngine
from pgm_engine.memory.l3_substrate import L3LatentSubstrate
from pgm_engine.types import EdgeRelation, EntityNode, PathResult

logger = logging.getLogger("capital_manifold.bridge")


class MonetaryTier(IntEnum):
    """Four-tier monetary hierarchy governing macro-financial transmission."""
    GENESIS = 0       # Sovereign fiscal & debt issuance (Treasury, OAT primary auction)
    TRANSMISSION = 1  # Financial intermediaries & central banks (SVTs, Banque de France)
    TRAVERSAL = 2     # Cross-border interbank clearing & trade flows (TARGET2, Importers)
    SINK = 3          # Safe-haven collateral anchors & foreign balance sheets (Bund, Bundesbank)


# Institutional metadata specifications
FINANCIAL_ENTITIES: Dict[str, Dict[str, Any]] = {
    "french_republic_tresor": {
        "tier": MonetaryTier.GENESIS,
        "name": "French Republic Trésor (Agence France Trésor)",
        "sector": "sovereign_issuer",
        "jurisdiction": "FR",
        "description": "Sovereign debt issuer executing OAT auctions and managing French public debt.",
    },
    "french_republic_oat_market": {
        "tier": MonetaryTier.GENESIS,
        "name": "French OAT Sovereign Benchmark Market",
        "sector": "sovereign_market",
        "jurisdiction": "FR",
        "description": "Secondary benchmark yield curve for French obligations assimilables du Trésor.",
    },
    "svt_dealers_bnp_socgen": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Primary Dealers (SVT: BNP Paribas, Société Générale, Crédit Agricole)",
        "sector": "primary_dealer",
        "jurisdiction": "FR_EU",
        "description": "Spécialistes en Valeurs du Trésor underwriting OAT auctions and clearing dealer liquidity.",
    },
    "banque_de_france": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Banque de France",
        "sector": "central_bank",
        "jurisdiction": "FR",
        "description": "Eurosystem national central bank managing dealer reserve accounts and TARGET2 settlement.",
    },
    "eurosystem_target2_pool": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "Eurosystem TARGET2 Clearing Pool",
        "sector": "interbank_clearing",
        "jurisdiction": "EU",
        "description": "ECB wholesale real-time gross settlement system where national balances accumulate.",
    },
    "french_economy_importers": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "French Economy Import Sector",
        "sector": "real_economy_trade",
        "jurisdiction": "FR",
        "description": "Real economy commercial enterprises generating monthly merchandise trade outflows.",
    },
    "bundesbank": {
        "tier": MonetaryTier.SINK,
        "name": "Deutsche Bundesbank",
        "sector": "central_bank_creditor",
        "jurisdiction": "DE",
        "description": "Eurosystem central bank holding positive TARGET2 claims and safe-haven liquidity reserves.",
    },
    "bund_risk_free_anchor": {
        "tier": MonetaryTier.SINK,
        "name": "German Federal Bund Risk-Free Anchor",
        "sector": "safe_haven_anchor",
        "jurisdiction": "DE",
        "description": "German Federal 10Y sovereign debt benchmark acting as the Eurozone risk-free capital sink.",
    },
    "foreign_export_economies": {
        "tier": MonetaryTier.SINK,
        "name": "Foreign Export Economies & Creditor Nations",
        "sector": "foreign_trade_sink",
        "jurisdiction": "GLOBAL",
        "description": "External export economies absorbing French merchandise trade deficit cash drains.",
    },
    "sovereign_debt_holders": {
        "tier": MonetaryTier.SINK,
        "name": "Institutional Sovereign Debt Holders",
        "sector": "debt_investor_sink",
        "jurisdiction": "WORLD",
        "description": "Domestic and global institutional bondholders holding French sovereign debt stock.",
    },
    # Dark Forest Ring 1: Transatlantic Dollar Conduit & Repo Nexus
    "offshore_fx_swap_desk": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "European G-SIB Offshore Synthetic USD FX Swap Desk (London/NY)",
        "sector": "synthetic_dollar_desk",
        "jurisdiction": "GLOBAL_OFFSHORE",
        "description": "Offshore cross-currency synthetic dollar funding desk executing EUR/USD basis swaps.",
    },
    "us_triparty_repo_pool": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "US Triparty Repo SOFR Clearing Basin (DTCC / BNY Mellon)",
        "sector": "us_repo_clearing",
        "jurisdiction": "US",
        "description": "Overnight secured dollar financing pool settling $3.007T/day under SOFR benchmark.",
    },
    "us_prime_mmf_basin": {
        "tier": MonetaryTier.SINK,
        "name": "US Prime Money Market Funds & Institutional Cash Basin",
        "sector": "us_dollar_cash_pool",
        "jurisdiction": "US",
        "description": "Short-term US dollar institutional cash surplus pool investing in triparty repo and paper.",
    },
    "us_treasury_tga": {
        "tier": MonetaryTier.SINK,
        "name": "US Treasury General Account (Federal Reserve Cash Vault)",
        "sector": "us_sovereign_cash_vault",
        "jurisdiction": "US",
        "description": "Operating cash balance of the US Treasury ($883.3B) absorbing banking reserves.",
    },
}


class ManifoldPGMBridge:
    """Production-grade bridge adapter connecting Capital Manifold to Procedural Graph Engine."""

    def __init__(
        self,
        parquet_dir: Path = Path("/home/ubuntu/repos/capital-manifold/data/processed"),
        duckdb_path: Path = Path("/home/ubuntu/repos/capital-manifold/data/cache/manifold.duckdb"),
        node_dim: int = 128,
        rel_dim: int = 32,
        num_landmark_clusters: int = 4,
        max_nodes_k: int = 128,
        max_edges_m: int = 512,
    ):
        self.parquet_dir = Path(parquet_dir)
        self.duckdb_path = Path(duckdb_path)
        self.node_dim = node_dim
        self.rel_dim = rel_dim
        self.num_landmark_clusters = num_landmark_clusters
        self.max_nodes_k = max_nodes_k
        self.max_edges_m = max_edges_m

        # Internal state
        self.flow_events: List[FlowEvent] = []
        self.stress_snapshot: Optional[MacroStressSnapshot] = None
        self.entity_embeddings: Dict[str, np.ndarray] = {}
        self.relation_embeddings: Dict[str, np.ndarray] = {}

        # Procedural Graph Engine components
        self.substrate = L3LatentSubstrate(node_dim=self.node_dim, rel_dim=self.rel_dim)
        self.engine = ProceduralGraphEngine(
            max_nodes_k=self.max_nodes_k,
            max_edges_m=self.max_edges_m,
            node_dim=self.node_dim,
            rel_dim=self.rel_dim,
            num_landmark_clusters=self.num_landmark_clusters,
            substrate=self.substrate,
        )

        self._load_records()
        self._build_relation_embeddings()
        self._build_entity_embeddings()
        self._populate_substrate()
        self.initialize_landmarks()

    def _load_records(self) -> None:
        """Loads FlowEvents and MacroStressSnapshot from Parquet or DuckDB cache."""
        events_parquet = self.parquet_dir / "flow_events.parquet"
        stress_parquet = self.parquet_dir / "stress_snapshots.parquet"

        if events_parquet.exists():
            try:
                con = duckdb.connect()
                df = con.execute(f"SELECT * FROM '{events_parquet}'").df()
                self.flow_events = []
                for _, r in df.iterrows():
                    self.flow_events.append(
                        FlowEvent(
                            event_id=str(r["event_id"]),
                            timestamp=str(r["timestamp"]),
                            period_label=str(r["period_label"]),
                            source_entity=str(r["source_entity"]),
                            source_jurisdiction=str(r["source_jurisdiction"]),
                            target_entity=str(r["target_entity"]),
                            target_jurisdiction=str(r["target_jurisdiction"]),
                            instrument=str(r["instrument"]),
                            nominal_amount=float(r["nominal_amount"]),
                            currency=str(r["currency"]),
                            amount_usd_normalized=float(r["amount_usd_normalized"]),
                            flow_type=FlowType(str(r["flow_type"])),
                            velocity_turnover_days=float(r["velocity_turnover_days"]) if r.get("velocity_turnover_days") is not None else None,
                            data_source=str(r["data_source"]),
                            source_line_item=str(r["source_line_item"]),
                            confidence=float(r.get("confidence", 1.0)),
                            metric_value=float(r["metric_value"]) if r.get("metric_value") is not None and not math.isnan(r["metric_value"]) else None,
                        )
                    )
                logger.info(f"Loaded {len(self.flow_events)} flow events from {events_parquet}")
            except Exception as ex:
                logger.warning(f"Could not load flow_events.parquet: {ex}")

        if stress_parquet.exists():
            try:
                con = duckdb.connect()
                df_s = con.execute(f"SELECT * FROM '{stress_parquet}' ORDER BY created_at DESC LIMIT 1").df()
                if not df_s.empty:
                    r = df_s.iloc[0]
                    self.stress_snapshot = MacroStressSnapshot(
                        timestamp=str(r["timestamp"]),
                        jurisdiction=str(r["jurisdiction"]),
                        oat_10y_yield=float(r["oat_10y_yield"]),
                        bund_10y_yield=float(r["bund_10y_yield"]),
                        oat_bund_spread_bp=float(r["oat_bund_spread_bp"]),
                        target2_net_position_eur=float(r["target2_net_position_eur"]),
                        maastricht_debt_nominal_eur=float(r["maastricht_debt_nominal_eur"]),
                        maastricht_debt_pct_gdp=float(r["maastricht_debt_pct_gdp"]),
                        latest_monthly_trade_deficit_eur=float(r["latest_monthly_trade_deficit_eur"]),
                        net_liquidity_pressure_score=float(r["net_liquidity_pressure_score"]),
                    )
                    logger.info(f"Loaded macro stress snapshot: score={self.stress_snapshot.net_liquidity_pressure_score}")
            except Exception as ex:
                logger.warning(f"Could not load stress_snapshots.parquet: {ex}")

        # Fallback default stress snapshot if file absent
        if self.stress_snapshot is None:
            self.stress_snapshot = MacroStressSnapshot(
                timestamp="2026-10-06T00:00:00Z",
                jurisdiction="FR",
                oat_10y_yield=4.00,
                bund_10y_yield=3.185,
                oat_bund_spread_bp=81.5,
                target2_net_position_eur=-181_336_520_000.0,
                maastricht_debt_nominal_eur=3_536_067_700_000.0,
                maastricht_debt_pct_gdp=117.6,
                latest_monthly_trade_deficit_eur=-8_129_600_000.0,
                net_liquidity_pressure_score=79.64,
            )

    def _build_relation_embeddings(self) -> None:
        """Constructs normalized 32-d relation embeddings for transmission edges."""
        relation_types = [
            "oat_primary_issuance",
            "secondary_market_distribution",
            "debt_inventory_placement",
            "dealer_reserve_clearing",
            "target2_liability_drain",
            "target2_claim_accumulation",
            "safe_haven_monetary_sink",
            "spread_friction_flight",
            "fiscal_stimulus_import_demand",
            "trade_deficit_drain",
            "trade_surplus_repatriation",
            "global_trade_settlement",
            # Dark Forest Ring 1: Transatlantic Dollar Conduit
            "synthetic_usd_fx_swap",
            "repo_dollar_financing",
            "mmf_cash_repo_lending",
            "repo_liquidity_absorption",
            "tga_reserve_absorption_drain",
        ]
        for idx, r_name in enumerate(relation_types):
            vec = np.zeros(self.rel_dim, dtype=np.float32)
            # Orthogonal base slot + harmonic wave
            slot = (idx * 2) % self.rel_dim
            vec[slot] = 1.0
            vec[(slot + 1) % self.rel_dim] = 0.5
            for k in range(self.rel_dim):
                vec[k] += 0.2 * math.cos(2.0 * math.pi * (idx + 1) * (k + 1) / self.rel_dim)
            norm = np.linalg.norm(vec)
            if norm > 1e-9:
                vec /= norm
            self.relation_embeddings[r_name] = vec

    def _build_entity_embeddings(self) -> None:
        """Designs high-dimensional (d=128) embeddings for financial entities.

        Subspace layout:
        - Dims 0..31:   Monetary Tier Scaffolding (Genesis, Transmission, Traversal, Sink)
        - Dims 32..63:  Institutional Sector & Jurisdiction Topology
        - Dims 64..95:  Balance Sheet Modality & Financial Role
        - Dims 96..127: Macro Stress Dynamic Modulation (spread, debt ratio, TARGET2 deficit)
        """
        stress = self.stress_snapshot
        spread_norm = min(2.0, stress.oat_bund_spread_bp / 100.0)
        debt_norm = min(2.0, stress.maastricht_debt_pct_gdp / 100.0)
        t2_norm = min(2.0, abs(stress.target2_net_position_eur) / 200e9)
        trade_norm = min(2.0, abs(stress.latest_monthly_trade_deficit_eur) / 10e9)
        pressure_norm = stress.net_liquidity_pressure_score / 100.0

        sector_offsets = {
            "sovereign_issuer": 32,
            "sovereign_market": 36,
            "primary_dealer": 40,
            "central_bank": 44,
            "interbank_clearing": 48,
            "real_economy_trade": 52,
            "central_bank_creditor": 56,
            "safe_haven_anchor": 60,
            "foreign_trade_sink": 62,
            "debt_investor_sink": 63,
            # Dark Forest Ring 1 sectors
            "synthetic_dollar_desk": 42,
            "us_repo_clearing": 50,
            "us_dollar_cash_pool": 58,
            "us_sovereign_cash_vault": 61,
        }

        for eid, meta in FINANCIAL_ENTITIES.items():
            vec = np.zeros(self.node_dim, dtype=np.float32)
            tier: MonetaryTier = meta["tier"]
            sector = meta["sector"]

            # 1. Tier Scaffolding Subspace (0..31): strong block activation
            tier_start = int(tier) * 8
            vec[tier_start : tier_start + 8] = 2.0

            # 2. Sector & Jurisdiction Subspace (32..63): unique institutional identity
            sec_slot = sector_offsets.get(sector, 32)
            vec[sec_slot : sec_slot + 4] += 1.5
            if "FR" in meta["jurisdiction"]:
                vec[32] += 0.8
            if "DE" in meta["jurisdiction"]:
                vec[33] += 0.8
            if "EU" in meta["jurisdiction"]:
                vec[34] += 0.8
            if "GLOBAL" in meta["jurisdiction"] or "WORLD" in meta["jurisdiction"]:
                vec[35] += 0.8
            if "US" in meta["jurisdiction"]:
                vec[35] += 1.2
            if "OFFSHORE" in meta["jurisdiction"]:
                vec[34] += 0.9

            # 3. Balance Sheet Modality Subspace (64..95)
            if tier == MonetaryTier.GENESIS:
                vec[64:72] = np.array([1.2, 0.9, 0.4, 0.2, 0.8, 0.3, 0.1, 0.5], dtype=np.float32)
            elif tier == MonetaryTier.TRANSMISSION:
                vec[72:80] = np.array([0.5, 1.4, 1.2, 0.8, 0.2, 0.7, 0.9, 0.4], dtype=np.float32)
            elif tier == MonetaryTier.TRAVERSAL:
                vec[80:88] = np.array([0.2, 0.6, 1.5, 1.3, 0.4, 0.1, 0.8, 0.7], dtype=np.float32)
            elif tier == MonetaryTier.SINK:
                vec[88:96] = np.array([0.1, 0.3, 0.5, 0.7, 1.5, 1.4, 1.2, 1.1], dtype=np.float32)

            # 4. Macro Stress Dynamic Modulation (96..127)
            # Sovereign issuer responds to debt & yield pressure
            if eid == "french_republic_tresor":
                vec[96:104] = np.array([debt_norm, pressure_norm, spread_norm, 0.5, debt_norm * 0.8, 0.3, 0.2, 0.1], dtype=np.float32)
            elif eid == "french_republic_oat_market":
                vec[96:104] = np.array([spread_norm, pressure_norm, 0.9, 0.4, spread_norm * 1.1, 0.2, 0.1, 0.5], dtype=np.float32)
            elif eid == "svt_dealers_bnp_socgen":
                vec[104:112] = np.array([spread_norm * 0.7, pressure_norm * 0.6, 0.8, 0.5, t2_norm * 0.5, 0.4, 0.3, 0.2], dtype=np.float32)
            elif eid == "banque_de_france":
                vec[104:112] = np.array([t2_norm, pressure_norm * 0.8, spread_norm * 0.5, 0.7, t2_norm * 1.2, 0.3, 0.1, 0.6], dtype=np.float32)
            elif eid == "eurosystem_target2_pool":
                vec[112:120] = np.array([t2_norm, pressure_norm, 0.7, 0.9, t2_norm * 1.3, 0.5, 0.2, 0.4], dtype=np.float32)
            elif eid == "french_economy_importers":
                vec[112:120] = np.array([trade_norm, pressure_norm * 0.5, 0.6, 0.8, trade_norm * 1.1, 0.2, 0.1, 0.3], dtype=np.float32)
            elif eid == "bundesbank":
                vec[120:128] = np.array([t2_norm, 0.2, 0.8, 1.4, spread_norm * 0.4, 0.9, 1.1, 0.7], dtype=np.float32)
            elif eid == "bund_risk_free_anchor":
                vec[120:128] = np.array([spread_norm, 0.1, 1.5, 1.6, 0.3, 1.2, 1.4, 0.8], dtype=np.float32)
            elif eid == "foreign_export_economies":
                vec[120:128] = np.array([trade_norm, 0.3, 1.1, 0.9, trade_norm * 0.8, 0.7, 0.6, 0.5], dtype=np.float32)
            elif eid == "sovereign_debt_holders":
                vec[120:128] = np.array([debt_norm * 0.5, spread_norm * 0.5, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3], dtype=np.float32)
            elif eid == "offshore_fx_swap_desk":
                vec[104:112] = np.array([spread_norm * 1.4, pressure_norm * 0.9, 1.2, 0.8, t2_norm * 0.7, 0.5, 0.4, 0.3], dtype=np.float32)
            elif eid == "us_triparty_repo_pool":
                vec[112:120] = np.array([0.4, 0.8, 1.6, 1.5, 0.2, 1.1, 0.9, 0.7], dtype=np.float32)
            elif eid == "us_prime_mmf_basin":
                vec[120:128] = np.array([0.2, 0.5, 1.4, 1.3, 0.1, 0.9, 1.2, 0.8], dtype=np.float32)
            elif eid == "us_treasury_tga":
                vec[120:128] = np.array([0.8, 0.9, 1.1, 1.6, 0.4, 0.7, 1.5, 1.2], dtype=np.float32)

            # Strict L2 normalization to unit sphere
            norm = np.linalg.norm(vec)
            if norm > 1e-9:
                vec = vec / norm
            self.entity_embeddings[eid] = vec

    def compute_edge_weight(
        self,
        base_weight: float,
        flow_volume_eur: float,
        risk_friction: float,
        is_domestic_retention: bool = False,
        friction_sensitivity: float = 1.0,
        volume_sensitivity: float = 0.5,
    ) -> float:
        """Calculates edge weight directly proportional to risk friction and inversely to flow volume.

        Formula:
            Weight (impedance) = W_base * (1 + kappa * risk_friction) / (1 + gamma * log10(1 + V_B))
            where V_B is normalized volume in Billions EUR.
        Domestic reinvestment incurs amplified impedance when sovereign risk friction spreads widen.
        """
        vol_b = max(0.0, abs(flow_volume_eur) / 1e9)
        kappa = friction_sensitivity * (2.2 if is_domestic_retention else 1.0)
        gamma = volume_sensitivity

        # Directly proportional to friction, inversely proportional to flow volume
        weight = base_weight * (1.0 + kappa * risk_friction) / (1.0 + gamma * math.log10(1.0 + vol_b))
        return max(0.02, float(weight))

    def _populate_substrate(self) -> None:
        """Populates L3 substrate with financial entity nodes and macroeconomic transmission edges."""
        # 1. Register all Entity Nodes
        for eid, meta in FINANCIAL_ENTITIES.items():
            emb = self.entity_embeddings[eid]
            tier = meta["tier"]
            self.substrate.add_entity(
                entity_id=eid,
                embedding=emb,
                cluster_id=int(tier),
                metadata=meta,
            )

        # 2. Extract flow figures from harvest
        stress = self.stress_snapshot
        spread_friction = stress.oat_bund_spread_bp / 100.0  # e.g. 0.815
        debt_eur = stress.maastricht_debt_nominal_eur       # e.g. €3.536 Trillion
        t2_eur = abs(stress.target2_net_position_eur)        # e.g. €181.3 Billion
        trade_eur = abs(stress.latest_monthly_trade_deficit_eur)  # e.g. €8.13 Billion

        # 3. Construct transmission relations
        # Corridor 1: Sovereign Debt Issuance -> Primary Dealers -> Central Bank -> TARGET2
        w_issuance = self.compute_edge_weight(
            base_weight=1.2,
            flow_volume_eur=debt_eur / 100.0,  # ~€35B annual gross issuance tranche
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="french_republic_tresor",
            target_id="svt_dealers_bnp_socgen",
            relation="oat_primary_issuance",
            weight=w_issuance,
            rel_embedding=self.relation_embeddings["oat_primary_issuance"],
            metadata={
                "instrument": "oat_primary_auction",
                "nominal_eur": debt_eur / 100.0,
                "tier_step": "0->1",
            },
        )

        w_clearing = self.compute_edge_weight(
            base_weight=1.1,
            flow_volume_eur=t2_eur * 0.5,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="svt_dealers_bnp_socgen",
            target_id="banque_de_france",
            relation="dealer_reserve_clearing",
            weight=w_clearing,
            rel_embedding=self.relation_embeddings["dealer_reserve_clearing"],
            metadata={
                "instrument": "central_bank_reserve_drain",
                "nominal_eur": t2_eur * 0.5,
                "tier_step": "1->1",
            },
        )

        w_t2_drain = self.compute_edge_weight(
            base_weight=1.0,
            flow_volume_eur=t2_eur,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="banque_de_france",
            target_id="eurosystem_target2_pool",
            relation="target2_liability_drain",
            weight=w_t2_drain,
            rel_embedding=self.relation_embeddings["target2_liability_drain"],
            metadata={
                "instrument": "target2_net_balance",
                "nominal_eur": t2_eur,
                "tier_step": "1->2",
            },
        )

        # Corridor 2: TARGET2 Pool -> Bundesbank -> German Bund Risk-Free Anchor
        w_t2_claim = self.compute_edge_weight(
            base_weight=1.0,
            flow_volume_eur=t2_eur,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="eurosystem_target2_pool",
            target_id="bundesbank",
            relation="target2_claim_accumulation",
            weight=w_t2_claim,
            rel_embedding=self.relation_embeddings["target2_claim_accumulation"],
            metadata={
                "instrument": "bundesbank_target2_claim",
                "nominal_eur": t2_eur,
                "tier_step": "2->3",
            },
        )

        w_bund_sink = self.compute_edge_weight(
            base_weight=0.9,
            flow_volume_eur=t2_eur * 0.8,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="bundesbank",
            target_id="bund_risk_free_anchor",
            relation="safe_haven_monetary_sink",
            weight=w_bund_sink,
            rel_embedding=self.relation_embeddings["safe_haven_monetary_sink"],
            metadata={
                "instrument": "bund_flight_reallocation",
                "nominal_eur": t2_eur * 0.8,
                "tier_step": "3->3",
            },
        )

        # Corridor 3: Domestic secondary placement vs. Risk Spread Friction Flight
        w_domestic_dist = self.compute_edge_weight(
            base_weight=0.8,
            flow_volume_eur=debt_eur * 0.05,
            risk_friction=spread_friction,
            is_domestic_retention=True,  # Higher impedance due to OAT-Bund spread
        )
        self.substrate.add_relation(
            source_id="svt_dealers_bnp_socgen",
            target_id="french_republic_oat_market",
            relation="secondary_market_distribution",
            weight=w_domestic_dist,
            rel_embedding=self.relation_embeddings["secondary_market_distribution"],
            metadata={
                "instrument": "oat_secondary_distribution",
                "is_domestic": True,
            },
        )

        w_spread_flight = self.compute_edge_weight(
            base_weight=1.3,
            flow_volume_eur=debt_eur * 0.02,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="french_republic_oat_market",
            target_id="bund_risk_free_anchor",
            relation="spread_friction_flight",
            weight=w_spread_flight,
            rel_embedding=self.relation_embeddings["spread_friction_flight"],
            metadata={
                "instrument": "oat_bund_10y_spread_bp",
                "spread_bp": stress.oat_bund_spread_bp,
            },
        )

        # Corridor 4: Fiscal Stimulus -> Trade Deficit -> Foreign Exporters -> Bundesbank
        w_fiscal_stim = self.compute_edge_weight(
            base_weight=0.9,
            flow_volume_eur=trade_eur * 12.0,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="french_republic_tresor",
            target_id="french_economy_importers",
            relation="fiscal_stimulus_import_demand",
            weight=w_fiscal_stim,
            rel_embedding=self.relation_embeddings["fiscal_stimulus_import_demand"],
            metadata={
                "instrument": "public_spending_trade_demand",
                "nominal_eur": trade_eur * 12.0,
                "tier_step": "0->2",
            },
        )

        w_trade_drain = self.compute_edge_weight(
            base_weight=1.0,
            flow_volume_eur=trade_eur,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="french_economy_importers",
            target_id="foreign_export_economies",
            relation="trade_deficit_drain",
            weight=w_trade_drain,
            rel_embedding=self.relation_embeddings["trade_deficit_drain"],
            metadata={
                "instrument": "merchandise_trade_balance",
                "nominal_eur": trade_eur,
                "tier_step": "2->3",
            },
        )

        w_trade_repat = self.compute_edge_weight(
            base_weight=0.95,
            flow_volume_eur=trade_eur * 0.7,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="foreign_export_economies",
            target_id="bundesbank",
            relation="trade_surplus_repatriation",
            weight=w_trade_repat,
            rel_embedding=self.relation_embeddings["trade_surplus_repatriation"],
            metadata={
                "instrument": "german_trade_surplus_deposit",
                "nominal_eur": trade_eur * 0.7,
                "tier_step": "3->3",
            },
        )

        # Corridor 5: Transatlantic US Dollar Conduit & Shadow Banking Nexus
        # A) SVT Primary Dealers -> Offshore FX Swap Desk (synthetic USD funding)
        # Scaled by OAT haircut friction (spread friction)
        w_fx_swap = self.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=t2_eur * 0.4,
            risk_friction=spread_friction * 1.5,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="svt_dealers_bnp_socgen",
            target_id="offshore_fx_swap_desk",
            relation="synthetic_usd_fx_swap",
            weight=w_fx_swap,
            rel_embedding=self.relation_embeddings["synthetic_usd_fx_swap"],
            metadata={"haircut_bps": stress.oat_bund_spread_bp * 0.5, "tier_step": "1->1"},
        )

        # B) Offshore FX Swap Desk -> US Triparty Repo Pool ($3.007T SOFR turnover)
        w_repo_financing = self.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=3007e9,
            risk_friction=spread_friction,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="offshore_fx_swap_desk",
            target_id="us_triparty_repo_pool",
            relation="repo_dollar_financing",
            weight=w_repo_financing,
            rel_embedding=self.relation_embeddings["repo_dollar_financing"],
            metadata={"sofr_rate": 3.89, "daily_volume_usd": 3007e9, "tier_step": "1->2"},
        )

        # C) US Triparty Repo Pool -> US Prime MMF Basin (Collateral allocation / cash absorption)
        w_mmf_drain = self.compute_edge_weight(
            base_weight=0.95,
            flow_volume_eur=2500e9,
            risk_friction=spread_friction * 0.5,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="us_triparty_repo_pool",
            target_id="us_prime_mmf_basin",
            relation="repo_liquidity_absorption",
            weight=w_mmf_drain,
            rel_embedding=self.relation_embeddings["repo_liquidity_absorption"],
            metadata={"instrument": "prime_mmf_cash_pool", "tier_step": "2->3"},
        )
        self.substrate.add_relation(
            source_id="us_prime_mmf_basin",
            target_id="us_triparty_repo_pool",
            relation="mmf_cash_repo_lending",
            weight=w_mmf_drain,
            rel_embedding=self.relation_embeddings["mmf_cash_repo_lending"],
            metadata={"instrument": "mmf_overnight_repo_cash", "tier_step": "3->2"},
        )

        # D) US Treasury TGA -> US Triparty Repo Pool (Reserve drain friction)
        w_tga_drain = self.compute_edge_weight(
            base_weight=1.35,
            flow_volume_eur=12.154e9,
            risk_friction=spread_friction * 1.8,
            is_domestic_retention=True,
        )
        self.substrate.add_relation(
            source_id="us_treasury_tga",
            target_id="us_triparty_repo_pool",
            relation="tga_reserve_absorption_drain",
            weight=w_tga_drain,
            rel_embedding=self.relation_embeddings["tga_reserve_absorption_drain"],
            metadata={"tga_closing_usd": 883.335e9, "net_drain_usd": 12.154e9, "tier_step": "3->2"},
        )

    def initialize_landmarks(self) -> None:
        """Builds coarse landmark clusters across the 4 monetary tiers."""
        self.engine.initialize_landmarks()
        logger.info(
            f"Initialized Global Landmark Graph with {self.engine.landmark_graph.num_clusters} clusters. "
            f"Adjacency: {dict(self.engine.landmark_graph.cluster_adjacency)}"
        )

    def materialize_liquidity_path(
        self,
        source_id: str,
        target_id: str,
        use_landmarks: bool = True,
        max_iterations: int = 500,
    ) -> PathResult:
        """Discovers and materializes non-greedy multi-hop liquidity path in PGM Engine.

        Overcomes bridge entity blindness via coarse landmark scaffolding and bidirectional A*.
        """
        result = self.engine.query_reasoning_corridor(
            source_id=source_id,
            target_id=target_id,
            use_landmarks=use_landmarks,
            max_iterations=max_iterations,
        )
        return result

    def execute_macro_traversal(self) -> Dict[str, Any]:
        """Executes full macroeconomic traversal from French sovereign debt to Eurosystem and US sinks.

        Returns:
            Dictionary containing:
            - paths: Traversal results to TARGET2, German Bund anchor, Foreign Trade Sinks, and US MMF Basin
            - bridge_entities: Intermediate clearing dealers and settlement hubs
            - buffer_stats: L1/L2 memory telemetry
            - macro_stress: Stress metrics underlying the network state
            - invariants_verified: Confirmation of topological contraction and reachability
        """
        src = "french_republic_tresor"
        tgt_t2 = "eurosystem_target2_pool"
        tgt_bund = "bund_risk_free_anchor"
        tgt_trade = "foreign_export_economies"
        tgt_mmf = "us_prime_mmf_basin"

        res_t2 = self.materialize_liquidity_path(src, tgt_t2)
        res_bund = self.materialize_liquidity_path(src, tgt_bund)
        res_trade = self.materialize_liquidity_path(src, tgt_trade)
        res_mmf = self.materialize_liquidity_path(src, tgt_mmf)

        all_bridge_entities = set()
        for res in [res_t2, res_bund, res_trade, res_mmf]:
            if res.success and len(res.path_nodes) > 2:
                # Bridge entities are intermediate nodes excluding src and tgt
                all_bridge_entities.update(res.path_nodes[1:-1])

        telemetry = self.engine.get_telemetry()

        # Invariant checks
        invariants = {
            "target2_reachability": res_t2.success,
            "bund_anchor_reachability": res_bund.success,
            "trade_sink_reachability": res_trade.success,
            "transatlantic_mmf_reachability": res_mmf.success,
            "bridge_entities_shielded": len(all_bridge_entities) > 0,
            "l1_memory_contained": telemetry["active_l1_nodes"] <= self.max_nodes_k,
        }

        return {
            "paths": {
                "target2_drain": {
                    "success": res_t2.success,
                    "nodes": res_t2.path_nodes,
                    "edges": [e.relation for e in res_t2.path_edges],
                    "total_cost": res_t2.total_cost,
                    "iterations": res_t2.iterations,
                    "expanded_nodes": res_t2.expanded_nodes,
                },
                "bund_safe_haven_flight": {
                    "success": res_bund.success,
                    "nodes": res_bund.path_nodes,
                    "edges": [e.relation for e in res_bund.path_edges],
                    "total_cost": res_bund.total_cost,
                    "iterations": res_bund.iterations,
                    "expanded_nodes": res_bund.expanded_nodes,
                },
                "foreign_trade_bleed": {
                    "success": res_trade.success,
                    "nodes": res_trade.path_nodes,
                    "edges": [e.relation for e in res_trade.path_edges],
                    "total_cost": res_trade.total_cost,
                    "iterations": res_trade.iterations,
                    "expanded_nodes": res_trade.expanded_nodes,
                },
                "transatlantic_dollar_conduit": {
                    "success": res_mmf.success,
                    "nodes": res_mmf.path_nodes,
                    "edges": [e.relation for e in res_mmf.path_edges],
                    "total_cost": res_mmf.total_cost,
                    "iterations": res_mmf.iterations,
                    "expanded_nodes": res_mmf.expanded_nodes,
                },
            },
            "bridge_entities": sorted(list(all_bridge_entities)),
            "buffer_stats": telemetry,
            "macro_stress": self.stress_snapshot.model_dump() if self.stress_snapshot else {},
            "invariants_verified": all(invariants.values()),
            "invariant_details": invariants,
        }
