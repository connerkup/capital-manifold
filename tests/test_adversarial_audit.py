"""Comprehensive Unit Tests for Adversarial Audit & Negative Control Suite.

Validates:
1. Adversarial substrate topology (90 nodes, 15 authentic SVTs, 66 deceptive decoys).
2. Continuous harmonic Fourier feature projections (no coordinate slicing).
3. Benchmark 1: Greedy Nearest-Neighbor search trapped by municipal SOE lure vs. Dual-Frontier A* success.
4. Benchmark 2: Negative Control (Hallucination Test) yielding 0.0% false positives.
5. Benchmark 3: Topological invariance of sovereign transmission backbone under decoy eviction.
6. Institutional edge gating integrity (sovereign issuance restricted to licensed SVTs).
"""

import numpy as np
import pytest

from capital_manifold.adversarial.adversarial_substrate import (
    AdversarialSubstrateBuilder,
    EntityCategory,
    greedy_nearest_neighbor_search,
)


@pytest.fixture(scope="module")
def adversarial_env():
    """Module-level fixture providing initialized engine and substrate."""
    builder = AdversarialSubstrateBuilder()
    engine, substrate = builder.build_adversarial_engine(
        max_nodes_k=128,
        max_edges_m=512,
        num_landmark_clusters=8,
        latent_epsilon=0.10,
    )
    return builder, engine, substrate


def test_adversarial_substrate_composition(adversarial_env):
    """Verifies that the substrate contains authentic SVTs and 65+ decoys across 5 categories."""
    builder, _, sub = adversarial_env
    assert len(sub.entities) >= 80
    assert len(sub.entities) == 90

    # Verify 15 Authentic AFT SVTs
    svts = [eid for eid, cat in builder.entity_categories.items() if cat == EntityCategory.SVT_PRIMARY_DEALER]
    assert len(svts) == 15
    for svt in svts:
        m = builder.entity_metrics[svt]
        assert m.svt_dealer_mandate == 1.0
        assert m.target2_direct_participant == 1.0
        assert m.central_bank_refi_access == 1.0

    # Verify Decoys Across All 5 Categories
    cat_counts = {}
    for cat in EntityCategory:
        cat_counts[cat] = sum(1 for c in builder.entity_categories.values() if c == cat)

    assert cat_counts[EntityCategory.DECOY_REGIONAL_SAVINGS] == 15
    assert cat_counts[EntityCategory.DECOY_MUNICIPAL_UTILITY] == 15
    assert cat_counts[EntityCategory.DECOY_REAL_ESTATE_SCPI] == 12
    assert cat_counts[EntityCategory.DECOY_CONSUMER_FINTECH] == 12
    assert cat_counts[EntityCategory.DECOY_OFFSHORE_SPV] == 12

    total_decoys = sum(
        count for cat, count in cat_counts.items()
        if "decoy" in cat.value
    )
    assert total_decoys == 66


def test_continuous_harmonic_projection_geometry(adversarial_env):
    """Verifies that embeddings are unit-norm and distances reflect continuous balance-sheet geometry."""
    _, _, sub = adversarial_env
    for eid, node in sub.entities.items():
        assert node.embedding.shape == (128,)
        norm = np.linalg.norm(node.embedding)
        assert norm == pytest.approx(1.0, abs=1e-5)

    # State-backed utility has high similarity to French sovereign due to state ownership
    tresor_emb = sub.get_entity("french_republic_tresor").embedding
    edf_emb = sub.get_entity("edf_electricite_de_france").embedding
    bund_emb = sub.get_entity("bund_risk_free_anchor").embedding

    cos_edf_bund = float(np.dot(edf_emb, bund_emb))
    # EDF exhibits deceptive similarity to sovereign benchmarks due to state credit characteristics
    assert cos_edf_bund > 0.40


def test_institutional_edge_gating_integrity(adversarial_env):
    """Verifies that sovereign auctions link ONLY to licensed SVTs, never to decoys."""
    builder, _, sub = adversarial_env
    tresor_edges = sub.adjacency.get("french_republic_tresor", {})

    # Sovereign issuance targets must strictly be licensed SVTs
    issuance_targets = [
        tgt_id for tgt_id, edge_list in tresor_edges.items()
        if any(e.relation == "oat_primary_issuance" for e in edge_list)
    ]
    assert len(issuance_targets) == 15
    for tgt_id in issuance_targets:
        assert builder.entity_categories[tgt_id] == EntityCategory.SVT_PRIMARY_DEALER
        assert builder.entity_metrics[tgt_id].svt_dealer_mandate == 1.0

    # No decoy entity can receive primary sovereign issuance
    for eid, cat in builder.entity_categories.items():
        if "decoy" in cat.value:
            assert eid not in issuance_targets


def test_benchmark_1_greedy_nearest_neighbor_trapped_in_lure(adversarial_env):
    """Benchmark 1A: Verifies that naive greedy 1-hop search gets trapped in deceptive SOE distractor."""
    _, _, sub = adversarial_env
    src = "french_republic_tresor"
    tgt = "bund_risk_free_anchor"

    success, path, reason = greedy_nearest_neighbor_search(
        source_id=src,
        target_id=tgt,
        substrate=sub,
        max_hops=10,
    )
    # Greedy must fail
    assert success is False
    assert len(path) > 1
    # Hop 1 must have greedily committed to the deceptive municipal utility lure
    assert path[1] == "edf_electricite_de_france"
    # Trapped inside corporate utility chain
    assert "sncf_reseau_transport" in path


def test_benchmark_1_dual_frontier_a_star_success(adversarial_env):
    """Benchmark 1B: Verifies that Dual-Frontier A* successfully discovers the authentic SVT path."""
    _, engine, _ = adversarial_env
    src = "french_republic_tresor"
    tgt_bund = "bund_risk_free_anchor"
    tgt_t2 = "eurosystem_target2_pool"

    # Traversal to German Bund Anchor
    res_bund = engine.query_reasoning_corridor(src, tgt_bund)
    assert res_bund.success is True
    assert res_bund.path_nodes[0] == src
    assert res_bund.path_nodes[-1] == tgt_bund
    # Must route through an authentic SVT primary dealer, not a decoy
    svt_in_path = any("svt_" in n for n in res_bund.path_nodes)
    assert svt_in_path is True
    assert "edf_electricite_de_france" not in res_bund.path_nodes

    # Traversal to TARGET2 Clearing Pool
    res_t2 = engine.query_reasoning_corridor(src, tgt_t2)
    assert res_t2.success is True
    assert res_t2.path_nodes[0] == src
    assert res_t2.path_nodes[-1] == tgt_t2
    assert "banque_de_france" in res_t2.path_nodes
    actual_relations = [e.relation for e in res_t2.path_edges]
    assert "oat_primary_issuance" in actual_relations
    assert "dealer_reserve_clearing" in actual_relations
    assert "target2_liability_drain" in actual_relations


def test_benchmark_2_negative_control_zero_hallucinations(adversarial_env):
    """Benchmark 2: Verifies that completely disconnected components produce 0 hallucinated edges."""
    _, engine, _ = adversarial_env

    negative_test_pairs = [
        ("caisse_epargne_idf", "lux_spv_capital_alpha"),
        ("sncf_voyageurs", "cayman_macro_opportunistic_fund"),
        ("meilleurtaux_courtage_broker", "bund_risk_free_anchor"),
        ("scpi_corum_origin_fonciere", "eurosystem_target2_pool"),
        ("finfrog_micro_credit", "bundesbank"),
    ]

    for src, tgt in negative_test_pairs:
        res = engine.query_reasoning_corridor(src, tgt)
        assert res.success is False, f"Expected no path between {src} and {tgt}"
        assert len(res.path_nodes) == 0, f"Expected 0 path nodes for disconnected pair {src}->{tgt}"
        assert len(res.path_edges) == 0, f"Expected 0 path edges for disconnected pair {src}->{tgt}"
        assert res.total_cost == float("inf")


def test_benchmark_3_topological_invariance_under_decoy_eviction(adversarial_env):
    """Benchmark 3: Verifies that evicting decoys from working memory preserves sovereign corridor."""
    _, engine, sub = adversarial_env
    src = "french_republic_tresor"
    tgt = "eurosystem_target2_pool"

    # 1. Establish baseline path
    res_before = engine.query_reasoning_corridor(src, tgt)
    assert res_before.success is True

    # 2. Allocate decoy nodes into L1 working memory
    test_decoys = [
        "caisse_epargne_idf",
        "sncf_reseau_transport",
        "pretto_digital_mortgage",
        "scpi_primovie_fonciere",
    ]
    for d in test_decoys:
        node = sub.get_entity(d)
        if node and not engine.l1_buffer.is_node_full:
            engine.l1_buffer.allocate_node(d, node.embedding)

    # 3. Evict decoys via TopologyGuard safe pruning
    active_set = set(engine.l1_buffer.entity_to_slot.keys())
    for d in test_decoys:
        if d in engine.l1_buffer.entity_to_slot:
            permitted, _ = engine.topology_guard.safe_prune_or_contract(
                node_id=d,
                active_nodes=active_set,
                l2_graph=engine.l2_graph,
                l1_buffer=engine.l1_buffer,
                force_contraction=True,
            )
            assert permitted is True
            assert d not in engine.l1_buffer.entity_to_slot

    # 4. Invariant: Sovereign corridor must remain 100% operational
    res_after = engine.query_reasoning_corridor(src, tgt)
    assert res_after.success is True
    assert res_after.path_nodes == res_before.path_nodes
    assert len(res_after.path_edges) == len(res_before.path_edges)
