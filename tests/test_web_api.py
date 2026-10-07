"""Unit tests for Capital Manifold FastAPI Web Service.

Tests all REST API endpoints, static assets, and schema contracts using FastAPI TestClient.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from capital_manifold.web.app import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Provides a shared FastAPI TestClient instance."""
    with TestClient(app) as c:
        yield c


# =============================================================================
# 1. Health and System Status Endpoint Tests
# =============================================================================

def test_api_health(client: TestClient):
    """Verifies GET /api/health returns 200 with database connectivity and node count."""
    res = client.get("/api/health")
    assert res.status_code == 200

    data = res.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Capital Manifold Planetary Web Engine"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data

    # Database telemetry
    db = data["database"]
    assert db["connected"] is True
    assert db["flow_events_count"] >= 97
    assert db["stress_snapshots_count"] >= 1

    # Topology telemetry
    topo = data["topology"]
    assert topo["node_count"] >= 126
    assert topo["edge_count"] >= 200
    assert topo["tiers"]["genesis"] > 0
    assert topo["tiers"]["transmission"] > 0
    assert topo["tiers"]["traversal"] > 0
    assert topo["tiers"]["sink"] > 0


# =============================================================================
# 2. Adversarial Audit Scorecard Endpoint Tests
# =============================================================================

def test_api_scorecard(client: TestClient):
    """Verifies GET /api/scorecard loads audit results and five category scores."""
    res = client.get("/api/scorecard")
    assert res.status_code == 200

    data = res.json()
    assert "system_integrity_score" in data
    assert 80.0 <= data["system_integrity_score"] <= 100.0

    # 5 Pillars
    cats = data["category_scores"]
    assert "conservation" in cats
    assert "dimensional" in cats
    assert "temporal" in cats
    assert "topology" in cats
    assert "dark_matter" in cats
    assert cats["conservation"] == 20.0
    assert cats["dimensional"] == 20.0

    # Zero leakage invariant
    assert data["total_leakage_usd"] == 0.0

    # Anomalies and Remediations
    assert len(data["high_risk_anomalies"]) >= 3
    assert len(data["remediation_recommendations"]) >= 5


# =============================================================================
# 3. Topology Endpoint Tests
# =============================================================================

def test_api_topology(client: TestClient):
    """Verifies GET /api/topology exports Cytoscape-formatted graph with 126+ nodes."""
    res = client.get("/api/topology")
    assert res.status_code == 200

    data = res.json()
    assert data["node_count"] >= 126
    assert data["edge_count"] >= 200

    nodes = data["elements"]["nodes"]
    edges = data["elements"]["edges"]
    assert len(nodes) == data["node_count"]
    assert len(edges) == data["edge_count"]

    # Verify node structure and coordinates
    sample_node = nodes[0]
    assert "data" in sample_node
    assert "position" in sample_node
    assert "x" in sample_node["position"]
    assert "y" in sample_node["position"]

    node_data = sample_node["data"]
    assert "id" in node_data
    assert "name" in node_data
    assert "tier" in node_data
    assert node_data["tier"] in (0, 1, 2, 3)
    assert "tier_label" in node_data
    assert "sector" in node_data
    assert "jurisdiction" in node_data

    # Verify edge structure
    sample_edge = edges[0]
    assert "data" in sample_edge
    edge_data = sample_edge["data"]
    assert "source" in edge_data
    assert "target" in edge_data
    assert "relation" in edge_data
    assert "weight" in edge_data


# =============================================================================
# 4. DuckDB Flows Endpoint Tests
# =============================================================================

def test_api_flows_default(client: TestClient):
    """Verifies GET /api/flows returns paginated flow records with provenance."""
    res = client.get("/api/flows?limit=25&offset=0")
    assert res.status_code == 200

    data = res.json()
    assert data["total"] >= 97
    assert data["limit"] == 25
    assert data["offset"] == 0
    assert len(data["flows"]) <= 25

    flow = data["flows"][0]
    assert "event_id" in flow
    assert "source_entity" in flow
    assert "target_entity" in flow
    assert "nominal_amount" in flow
    assert "amount_usd_normalized" in flow
    assert "annualized_rate_usd" in flow
    assert "provenance_badge" in flow
    assert flow["annualized_rate_usd"] >= 0.0


def test_api_flows_with_currency_filter(client: TestClient):
    """Verifies GET /api/flows filters correctly by currency."""
    res = client.get("/api/flows?currency=USD&limit=10")
    assert res.status_code == 200

    data = res.json()
    for f in data["flows"]:
        assert f["currency"] == "USD"


def test_api_flows_with_search_filter(client: TestClient):
    """Verifies GET /api/flows text search filter across entities and instruments."""
    res = client.get("/api/flows?search=repo&limit=10")
    assert res.status_code == 200

    data = res.json()
    assert data["total"] > 0
    for f in data["flows"]:
        combined = (f["source_entity"] + f["target_entity"] + f["instrument"] + f["data_source"]).lower()
        assert "repo" in combined


# =============================================================================
# 5. Macro Stress Snapshots Endpoint Tests
# =============================================================================

def test_api_stress_snapshots(client: TestClient):
    """Verifies GET /api/stress_snapshots queries macro stress records."""
    res = client.get("/api/stress_snapshots")
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    snap = data[0]
    assert "oat_10y_yield" in snap
    assert "bund_10y_yield" in snap
    assert "oat_bund_spread_bp" in snap
    assert snap["oat_bund_spread_bp"] > 0.0
    assert "target2_net_position_eur" in snap


# =============================================================================
# 6. Stress Gauntlet Simulation Endpoint Tests
# =============================================================================

def test_api_simulate_regime_1(client: TestClient):
    """Verifies POST /api/simulate for Regime 1 (French OAT Blowout)."""
    res = client.post("/api/simulate", json={"regime": 1})
    assert res.status_code == 200

    data = res.json()
    assert data["regime_id"] == "REGIME-01-OAT-CRISIS"
    assert data["bypass_corridor_activation_pct"] == 100.0
    assert "ca_cib_natixis_dealer_syndicate" in data["active_bypasses"]
    assert data["zero_hallucinations_verified"] is True
    assert "french_republic_tresor->eurosystem_target2_pool" in data["routes"]


def test_api_simulate_regime_2(client: TestClient):
    """Verifies POST /api/simulate for Regime 2 (Transatlantic Dollar Repo Freeze)."""
    res = client.post("/api/simulate", json={"regime": 2})
    assert res.status_code == 200

    data = res.json()
    assert data["regime_id"] == "REGIME-02-DOLLAR-FREEZE"
    assert data["bypass_corridor_activation_pct"] == 100.0
    assert "ficc_sponsored_repo_clearing" in data["active_bypasses"]
    assert data["zero_hallucinations_verified"] is True


def test_api_simulate_regime_3(client: TestClient):
    """Verifies POST /api/simulate for Regime 3 (Planetary Compound Crisis)."""
    res = client.post("/api/simulate", json={"regime": 3})
    assert res.status_code == 200

    data = res.json()
    assert data["regime_id"] == "REGIME-03-COMPOUND-SUPER-CRISIS"
    assert data["zero_hallucinations_verified"] is True

    # Severed route check
    interdicted = data["routes"]["bank_of_russia_cbr_vault->french_economy_importers"]
    assert interdicted["is_severed_expected"] is True
    assert interdicted["shocked_success"] is False


def test_api_simulate_invalid_regime(client: TestClient):
    """Verifies POST /api/simulate rejects invalid regime IDs."""
    res = client.post("/api/simulate", json={"regime": 99})
    assert res.status_code == 422


# =============================================================================
# 7. Macro Circuits & Pure Macro Isolation Tests
# =============================================================================

def test_circuits_and_pure_macro_isolation(client: TestClient):
    """Verifies that private asset demo endpoints are absent and institutional macro circuits are active."""
    res_priv = client.get("/api/private_assets")
    assert res_priv.status_code == 404

    res_circ = client.get("/api/circuits")
    assert res_circ.status_code == 200
    circuits = res_circ.json()
    circuit_ids = [c["id"] for c in circuits]
    assert "CIRCUIT-06-GULF-PETRODOLLAR" in circuit_ids
    assert "CIRCUIT-06-CONNER-APEX" not in circuit_ids


# =============================================================================
# 8. Capital Pools Explorer & Path Discovery Tests
# =============================================================================

def test_api_pools_list(client: TestClient):
    """Verifies GET /api/pools returns full list of pools with aggregated volumes."""
    res = client.get("/api/pools")
    assert res.status_code == 200

    pools = res.json()
    assert isinstance(pools, list)
    assert len(pools) >= 126

    sample = pools[0]
    assert "id" in sample
    assert "name" in sample
    assert "tier" in sample
    assert "role" in sample
    assert sample["role"] in ("source", "sink", "conduit")
    assert "inflow_usd" in sample
    assert "outflow_usd" in sample
    assert "net_flow_usd" in sample


def test_api_pool_detail_valid(client: TestClient):
    """Verifies GET /api/pools/{pool_id} returns detailed breakdown."""
    res = client.get("/api/pools/french_republic_tresor")
    assert res.status_code == 200

    data = res.json()
    assert data["pool"]["id"] == "french_republic_tresor"
    assert data["conservation_status"] in (
        "strictly_conserved_conduit",
        "sovereign_faucet_genesis",
        "accumulating_monetary_sink",
        "active_financial_intermediary",
    )
    assert "totals" in data
    assert "upstream_neighbors" in data
    assert "downstream_neighbors" in data


def test_api_pool_detail_not_found(client: TestClient):
    """Verifies GET /api/pools/{pool_id} returns 404 for unknown pool."""
    res = client.get("/api/pools/non_existent_pool_99999")
    assert res.status_code == 404


def test_api_paths_discovery(client: TestClient):
    """Verifies GET /api/paths executes Dual-Frontier A* between two pools."""
    res = client.get("/api/paths?source_id=french_republic_tresor&target_id=bund_risk_free_anchor")
    assert res.status_code == 200

    data = res.json()
    assert data["success"] is True
    assert data["source_id"] == "french_republic_tresor"
    assert data["target_id"] == "bund_risk_free_anchor"
    assert data["hops"] >= 3
    assert len(data["path_nodes"]) == data["hops"]
    assert len(data["hop_details"]) == data["hops"]
    assert data["total_cost"] is not None
    assert data["total_cost"] > 0.0


def test_api_featured_circuits(client: TestClient):
    """Verifies GET /api/circuits/featured returns curated institutional circuits."""
    res = client.get("/api/circuits/featured")
    assert res.status_code == 200

    circuits = res.json()
    assert isinstance(circuits, list)
    assert len(circuits) >= 5

    c0 = circuits[0]
    assert "id" in c0
    assert "title" in c0
    assert "source_id" in c0
    assert "target_id" in c0
    assert "key_nodes" in c0
    assert len(c0["key_nodes"]) >= 3


# =============================================================================
# 9. Static Assets & Root HTML Delivery Tests
# =============================================================================

def test_static_root_html(client: TestClient):
    """Verifies GET / serves index.html."""
    res = client.get("/")
    assert res.status_code == 200
    assert "CAPITAL MANIFOLD" in res.text
    assert "Planetary Capital Graph" in res.text


def test_static_assets_css_and_js(client: TestClient):
    """Verifies static assets (CSS, JS) are properly served with 200 OK."""
    res_css = client.get("/static/styles.css")
    assert res_css.status_code == 200
    assert "CAPITAL MANIFOLD" in res_css.text

    res_js = client.get("/static/app.js")
    assert res_js.status_code == 200
    assert "CAPITAL MANIFOLD" in res_js.text
