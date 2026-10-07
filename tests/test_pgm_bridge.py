"""Unit tests verifying Capital Manifold <-> PGM Engine Bridge Adapter.

Tests:
1. Entity and edge registration in L3 substrate.
2. 4-Tier Landmark clustering and coarse corridor scaffolding.
3. Dual-Frontier A* path discovery from French sovereign debt to TARGET2 and German Bund.
4. Topological contraction of intermediate clearing nodes into virtual shortcuts.
5. Shielding of intermediate bridge entities against greedy metric blindness.
"""

import math
import numpy as np
import pytest

from capital_manifold.bridge.pgm_adapter import (
    FINANCIAL_ENTITIES,
    ManifoldPGMBridge,
    MonetaryTier,
)
from pgm_engine.types import EdgeRelation


@pytest.fixture
def bridge() -> ManifoldPGMBridge:
    """Fixture providing initialized ManifoldPGMBridge."""
    return ManifoldPGMBridge()


def test_entity_and_edge_registration(bridge: ManifoldPGMBridge):
    """Verifies that all financial entities and transmission relations are properly registered."""
    sub = bridge.substrate
    assert len(sub.entities) == len(FINANCIAL_ENTITIES)

    # Check key nodes
    key_nodes = [
        "french_republic_tresor",
        "banque_de_france",
        "bundesbank",
        "svt_dealers_bnp_socgen",
        "eurosystem_target2_pool",
        "bund_risk_free_anchor",
        "foreign_export_economies",
    ]
    for nid in key_nodes:
        node = sub.get_entity(nid)
        assert node is not None, f"Node {nid} missing from substrate"
        assert node.embedding.shape == (128,), f"Node {nid} has invalid dimension"
        norm = np.linalg.norm(node.embedding)
        assert norm == pytest.approx(1.0, abs=1e-5), f"Node {nid} embedding not normalized"

    # Verify primary debt issuance relation
    targets = sub.adjacency.get("french_republic_tresor", {})
    assert "svt_dealers_bnp_socgen" in targets
    issuance_edges = targets["svt_dealers_bnp_socgen"]
    assert len(issuance_edges) >= 1
    edge = issuance_edges[0]
    assert edge.relation == "oat_primary_issuance"
    assert edge.weight > 0
    assert edge.relation_embedding is not None
    assert edge.relation_embedding.shape == (32,)

    # Verify central bank clearing relation
    targets_svt = sub.adjacency.get("svt_dealers_bnp_socgen", {})
    assert "banque_de_france" in targets_svt
    clearing_edges = targets_svt["banque_de_france"]
    assert clearing_edges[0].relation == "dealer_reserve_clearing"

    # Verify TARGET2 liability drain relation
    targets_bdf = sub.adjacency.get("banque_de_france", {})
    assert "eurosystem_target2_pool" in targets_bdf
    t2_edges = targets_bdf["eurosystem_target2_pool"]
    assert t2_edges[0].relation == "target2_liability_drain"


def test_edge_weight_friction_and_volume_dynamics(bridge: ManifoldPGMBridge):
    """Verifies that edge weight increases with risk friction and decreases with flow volume."""
    # Base comparison
    w_low_friction = bridge.compute_edge_weight(
        base_weight=1.0,
        flow_volume_eur=10e9,
        risk_friction=0.20,
    )
    w_high_friction = bridge.compute_edge_weight(
        base_weight=1.0,
        flow_volume_eur=10e9,
        risk_friction=1.50,
    )
    # Higher risk friction -> higher impedance / weight
    assert w_high_friction > w_low_friction

    # Volume sensitivity: higher volume -> lower weight (inversely proportional)
    w_high_vol = bridge.compute_edge_weight(
        base_weight=1.0,
        flow_volume_eur=100e9,
        risk_friction=0.50,
    )
    w_low_vol = bridge.compute_edge_weight(
        base_weight=1.0,
        flow_volume_eur=1e9,
        risk_friction=0.50,
    )
    assert w_high_vol < w_low_vol

    # Domestic reinvestment retention: amplified friction sensitivity
    w_domestic = bridge.compute_edge_weight(
        base_weight=1.0,
        flow_volume_eur=10e9,
        risk_friction=0.80,
        is_domestic_retention=True,
    )
    w_foreign = bridge.compute_edge_weight(
        base_weight=1.0,
        flow_volume_eur=10e9,
        risk_friction=0.80,
        is_domestic_retention=False,
    )
    assert w_domestic > w_foreign


def test_landmark_clustering_across_tiers(bridge: ManifoldPGMBridge):
    """Verifies that K-Means landmark graph groups entities into 4 coherent monetary tiers."""
    lm = bridge.engine.landmark_graph
    assert lm.num_clusters == 4

    # Ensure all entities have cluster assignments
    for eid in FINANCIAL_ENTITIES.keys():
        assert eid in lm.entity_to_cluster
        cid = lm.entity_to_cluster[eid]
        assert 0 <= cid < 4

    # Entities within same monetary tier should share the same cluster
    c_tresor = lm.entity_to_cluster["french_republic_tresor"]
    c_oat = lm.entity_to_cluster["french_republic_oat_market"]
    assert c_tresor == c_oat, "Tier 0 entities should cluster together"

    c_svt = lm.entity_to_cluster["svt_dealers_bnp_socgen"]
    c_bdf = lm.entity_to_cluster["banque_de_france"]
    assert c_svt == c_bdf, "Tier 1 entities should cluster together"

    c_t2 = lm.entity_to_cluster["eurosystem_target2_pool"]
    c_imp = lm.entity_to_cluster["french_economy_importers"]
    assert c_t2 == c_imp, "Tier 2 entities should cluster together"

    c_bbk = lm.entity_to_cluster["bundesbank"]
    c_bund = lm.entity_to_cluster["bund_risk_free_anchor"]
    assert c_bbk == c_bund, "Tier 3 entities should cluster together"

    # Coarse routing corridor from Tier 0 to Tier 3 should connect through intermediate tiers
    src_emb = bridge.substrate.get_entity("french_republic_tresor").embedding
    tgt_emb = bridge.substrate.get_entity("bund_risk_free_anchor").embedding
    corridor = lm.compute_routing_corridor(src_emb, tgt_emb, allow_neighboring_clusters=True)
    assert c_tresor in corridor
    assert c_bund in corridor
    assert c_svt in corridor
    assert c_t2 in corridor


def test_dual_frontier_a_star_path_to_target2(bridge: ManifoldPGMBridge):
    """Verifies Dual-Frontier A* path discovery from French Treasury to TARGET2 clearing pool."""
    res = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="eurosystem_target2_pool",
    )
    assert res.success is True
    assert res.path_nodes == [
        "french_republic_tresor",
        "svt_dealers_bnp_socgen",
        "banque_de_france",
        "eurosystem_target2_pool",
    ]
    expected_relations = [
        "oat_primary_issuance",
        "dealer_reserve_clearing",
        "target2_liability_drain",
    ]
    actual_relations = [e.relation for e in res.path_edges]
    assert actual_relations == expected_relations
    assert res.total_cost > 0.0
    assert res.iterations > 0

    # Ensure intermediate bridge nodes are admitted to L1 and L2
    assert "svt_dealers_bnp_socgen" in bridge.engine.l1_buffer.entity_to_slot
    assert "banque_de_france" in bridge.engine.l1_buffer.entity_to_slot
    assert bridge.engine.l2_graph.has_node("svt_dealers_bnp_socgen")
    assert bridge.engine.l2_graph.has_node("banque_de_france")


def test_dual_frontier_a_star_path_to_bund_anchor(bridge: ManifoldPGMBridge):
    """Verifies Dual-Frontier A* path discovery from French Treasury to German Bund Anchor."""
    res = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="bund_risk_free_anchor",
    )
    assert res.success is True
    assert res.path_nodes[0] == "french_republic_tresor"
    assert res.path_nodes[-1] == "bund_risk_free_anchor"
    assert len(res.path_nodes) >= 3
    assert res.total_cost > 0.0

    # Endpoints and intermediate entities present in L1
    assert "french_republic_tresor" in bridge.engine.l1_buffer.entity_to_slot
    assert "bund_risk_free_anchor" in bridge.engine.l1_buffer.entity_to_slot


def test_execute_macro_traversal_summary(bridge: ManifoldPGMBridge):
    """Verifies that full macroeconomic traversal pipeline executes with valid invariants."""
    summary = bridge.execute_macro_traversal()
    assert summary["invariants_verified"] is True

    paths = summary["paths"]
    assert paths["target2_drain"]["success"] is True
    assert paths["bund_safe_haven_flight"]["success"] is True
    assert paths["foreign_trade_bleed"]["success"] is True

    # Bridge entities must include key intermediaries
    bridge_entities = summary["bridge_entities"]
    assert "svt_dealers_bnp_socgen" in bridge_entities
    assert "banque_de_france" in bridge_entities

    # Buffer telemetry
    stats = summary["buffer_stats"]
    assert stats["active_l1_nodes"] > 0
    assert stats["active_l1_edges"] > 0
    assert stats["landmark_clusters"] == 4


def test_topological_contraction_of_intermediate_clearing_nodes(bridge: ManifoldPGMBridge):
    """Verifies that an intermediate clearing node is safely contracted into a virtual shortcut."""
    # First, materialize path from Treasury to TARGET2
    res = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="eurosystem_target2_pool",
    )
    assert res.success is True

    l1_buf = bridge.engine.l1_buffer
    l2_graph = bridge.engine.l2_graph
    top_guard = bridge.engine.topology_guard

    # Verify svt_dealers_bnp_socgen is active in L1
    assert "svt_dealers_bnp_socgen" in l1_buf.entity_to_slot
    active_nodes = set(l1_buf.entity_to_slot.keys())

    # Get original incoming and outgoing edge weights
    in_edge = l2_graph.in_edges["svt_dealers_bnp_socgen"]["french_republic_tresor"]["oat_primary_issuance"]
    out_edge = l2_graph.out_edges["svt_dealers_bnp_socgen"]["banque_de_france"]["dealer_reserve_clearing"]
    expected_weight = in_edge.weight * out_edge.weight * 0.95

    # Execute topological contraction
    permitted, synth_edges = top_guard.safe_prune_or_contract(
        node_id="svt_dealers_bnp_socgen",
        active_nodes=active_nodes,
        l2_graph=l2_graph,
        l1_buffer=l1_buf,
        force_contraction=True,
    )

    assert permitted is True
    # At least one virtual shortcut was synthesized connecting Tresor to Banque de France
    matching_synth = [
        e for e in synth_edges
        if e.source_id == "french_republic_tresor" and e.target_id == "banque_de_france"
    ]
    assert len(matching_synth) == 1
    shortcut = matching_synth[0]
    assert shortcut.is_virtual is True
    assert shortcut.weight == pytest.approx(expected_weight, rel=1e-3)
    assert shortcut.provenance == ["svt_dealers_bnp_socgen"]
    assert "virtual" in shortcut.relation

    # Node is evicted from L1 buffer
    assert "svt_dealers_bnp_socgen" not in l1_buf.entity_to_slot

    # Reachability between endpoints is preserved in L2
    assert "banque_de_france" in l2_graph.out_edges["french_republic_tresor"]
    assert shortcut.relation in l2_graph.out_edges["french_republic_tresor"]["banque_de_france"]


def test_spof_mitigation_triparty_repo_outage_activates_ficc_bypass(bridge: ManifoldPGMBridge):
    """Verifies that simulated outage of us_triparty_repo_pool activates FICC sponsored repo bypass."""
    # 1. Baseline path verification
    res_base = bridge.materialize_liquidity_path(
        source_id="japan_institutional_carry_desk",
        target_id="us_treasury_tga",
    )
    assert res_base.success is True
    assert "japan_institutional_carry_desk" == res_base.path_nodes[0]
    assert "us_treasury_tga" == res_base.path_nodes[-1]

    # 2. Simulate catastrophic SPOF outage of us_triparty_repo_pool
    sub = bridge.substrate
    sub.entities.pop("us_triparty_repo_pool", None)
    sub.adjacency.pop("us_triparty_repo_pool", None)
    for neighbors in sub.adjacency.values():
        neighbors.pop("us_triparty_repo_pool", None)

    # Refresh landmark graph to reflect outage
    bridge.initialize_landmarks()

    # 3. Query liquidity path under simulated outage
    res_bypass = bridge.materialize_liquidity_path(
        source_id="japan_institutional_carry_desk",
        target_id="us_treasury_tga",
    )
    assert res_bypass.success is True
    assert "us_triparty_repo_pool" not in res_bypass.path_nodes
    assert "ficc_sponsored_repo_clearing" in res_bypass.path_nodes
    assert "us_treasury_tga" == res_bypass.path_nodes[-1]


def test_spof_mitigation_svt_dealer_outage_activates_syndicate_bypass(bridge: ManifoldPGMBridge):
    """Verifies that simulated outage of svt_dealers_bnp_socgen activates CA-CIB Natixis syndicate bypass."""
    sub = bridge.substrate
    # Simulate catastrophic outage of primary SVT dealers
    sub.entities.pop("svt_dealers_bnp_socgen", None)
    sub.adjacency.pop("svt_dealers_bnp_socgen", None)
    for neighbors in sub.adjacency.values():
        neighbors.pop("svt_dealers_bnp_socgen", None)

    bridge.initialize_landmarks()

    res_syndicate = bridge.materialize_liquidity_path(
        source_id="french_republic_tresor",
        target_id="eurosystem_target2_pool",
    )
    assert res_syndicate.success is True
    assert "svt_dealers_bnp_socgen" not in res_syndicate.path_nodes
    assert "ca_cib_natixis_dealer_syndicate" in res_syndicate.path_nodes
    assert "banque_de_france" in res_syndicate.path_nodes
    assert "eurosystem_target2_pool" == res_syndicate.path_nodes[-1]
