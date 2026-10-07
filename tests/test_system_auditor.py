"""Comprehensive Unit & Regression Tests for Adversarial System Auditor.

Tests all five auditing dimensions:
1. AccountingConservationAuditor (Sources, Conduits, Sinks, Leaks, Orphans).
2. DimensionalIntegrityAuditor (Unit errors, basis point spread as fiat, signed flows, FX rates).
3. TemporalCadenceAuditor (Frequency mixing, annualized rate equivalents, Stock vs Flow).
4. GraphTopologyAuditor (117+ node connectivity, articulation points, sink traps, node removals).
5. UnmodeledRiskEstimator (BIS derivatives $600T, Basis trade $800B, Trade discrepancy $175B, PBOC swaps $550B).
6. SystemAuditor (Integrated scorecard, integrity score, anomalies, recommendations).
"""

from __future__ import annotations

import pytest
import pandas as pd
import numpy as np

from capital_manifold.adversarial.system_auditor import (
    AccountingConservationAuditor,
    DimensionalIntegrityAuditor,
    TemporalCadenceAuditor,
    GraphTopologyAuditor,
    UnmodeledRiskEstimator,
    SystemAuditor,
    EntityRole,
    SinkType,
    TemporalCadence,
    FullAuditScorecard,
    DEFAULT_DUCKDB_PATH,
)


@pytest.fixture(scope="module")
def duckdb_available():
    """Verify DuckDB test file exists."""
    assert DEFAULT_DUCKDB_PATH.exists(), f"DuckDB not found at {DEFAULT_DUCKDB_PATH}"
    return DEFAULT_DUCKDB_PATH


# -------------------------------------------------------------------------
# 1. Accounting Conservation Tests
# -------------------------------------------------------------------------

def test_accounting_conservation_roles(duckdb_available):
    """Verifies that entities are properly categorized into Source, Conduit, Sink, or Orphan."""
    auditor = AccountingConservationAuditor(duckdb_path=duckdb_available)
    report = auditor.audit()

    assert report.total_entities_evaluated >= 40
    assert len(report.source_entities) > 0
    assert len(report.conduit_entities) > 0
    assert len(report.sink_entities) > 0
    assert len(report.orphan_entities) > 0

    # shadow_tanker_energy_arbitrage has both Urals intake and refining outflow -> Conduit
    assert "shadow_tanker_energy_arbitrage" in report.conduit_entities
    summary = report.summaries["shadow_tanker_energy_arbitrage"]
    assert summary.role == EntityRole.INTERMEDIATE_CONDUIT
    assert summary.is_conduit is True

    # bundesbank is now a legitimate sink connected via TARGET2 claims
    assert "bundesbank" in report.sink_entities
    # offshore FX swap desk is active as an intermediate conduit
    assert "offshore_fx_swap_desk" in report.conduit_entities
    # Check remaining unharvested orphan nodes
    assert any(e in report.orphan_entities for e in ["bund_risk_free_anchor", "french_republic_oat_market"])


def test_accounting_conservation_double_entry_leaks(duckdb_available):
    """Verifies double-entry conservation and remediation of Russian oil arbitrage and corporate buybacks."""
    auditor = AccountingConservationAuditor(duckdb_path=duckdb_available)
    report = auditor.audit()

    # Verify remediated shadow tanker energy arbitrage: $140B in == $140B out ($55B India + $60B China + $25B Dubai)
    tanker_summary = report.summaries["shadow_tanker_energy_arbitrage"]
    assert tanker_summary.total_inflow_usd == pytest.approx(140.0e9, rel=1e-3)
    assert tanker_summary.total_outflow_usd == pytest.approx(140.0e9, rel=1e-3)
    assert tanker_summary.is_leak is False
    assert tanker_summary.leak_amount_usd == pytest.approx(0.0, abs=1e-3)

    # Verify remediated Apple cash vault: $182.399B in == $182.399B out
    apple_summary = report.summaries["apple_bigtech_treasury_vault"]
    assert apple_summary.is_leak is False
    assert apple_summary.leak_amount_usd == pytest.approx(0.0, abs=1e-3)

    # Verify detector catches synthetic double-entry leaks when present
    mock_df = pd.DataFrame([
        {
            "event_id": "test_leak_in",
            "source_entity": "mock_source",
            "target_entity": "mock_conduit",
            "amount_usd_normalized": 140e9,
            "nominal_amount": 140e9,
            "currency": "USD",
            "flow_type": "trade_settlement",
        },
        {
            "event_id": "test_leak_out",
            "source_entity": "mock_conduit",
            "target_entity": "mock_sink",
            "amount_usd_normalized": 55e9,
            "nominal_amount": 55e9,
            "currency": "USD",
            "flow_type": "trade_settlement",
        },
    ])
    mock_auditor = AccountingConservationAuditor(events_df=mock_df)
    mock_rep = mock_auditor.audit()
    assert len(mock_rep.detected_leaks) == 1
    assert mock_rep.detected_leaks[0]["entity_id"] == "mock_conduit"
    assert mock_rep.detected_leaks[0]["leak_amount_usd"] == pytest.approx(85e9, rel=1e-3)


# -------------------------------------------------------------------------
# 2. Dimensional Integrity Tests
# -------------------------------------------------------------------------

def test_dimensional_integrity_unit_errors(duckdb_available):
    """Verifies that database is dimensionally sound and detector flags unit/type errors when injected."""
    auditor = DimensionalIntegrityAuditor(duckdb_path=duckdb_available)
    report = auditor.audit()

    # Remediated DuckDB database must be 100% dimensionally sound
    assert report.is_dimensionally_sound is True
    assert report.unit_mismatches_count == 0
    assert report.signed_amount_violations_count == 0

    # Specifically verify detector catches OAT-Bund spread stored as fiat currency
    bad_df = pd.DataFrame([
        {
            "event_id": "spread_oat_bund_bad",
            "instrument": "oat_bund_10y_spread_bp",
            "nominal_amount": 73.0,
            "currency": "EUR",
            "amount_usd_normalized": 79.57,
            "flow_type": "risk_friction",
            "metric_value": 73.0,
        }
    ])
    mock_auditor = DimensionalIntegrityAuditor(events_df=bad_df)
    mock_rep = mock_auditor.audit()
    assert mock_rep.is_dimensionally_sound is False
    assert mock_rep.unit_mismatches_count >= 1
    err = mock_rep.errors[0]
    assert err.error_type == "SPREAD_AS_FIAT_CURRENCY_ERROR"
    assert err.nominal_amount == pytest.approx(73.0, rel=1e-2)
    assert err.currency == "EUR"
    assert err.amount_usd_normalized == pytest.approx(79.57, rel=1e-2)
    assert err.severity == "CRITICAL"


def test_dimensional_integrity_signed_amounts(duckdb_available):
    """Verifies that database has no signed negative amounts and detector flags negative flows."""
    auditor = DimensionalIntegrityAuditor(duckdb_path=duckdb_available)
    report = auditor.audit()

    # Remediated database has zero negative flows
    assert report.signed_amount_violations_count == 0

    # Verify detector catches negative nominal amounts
    bad_df = pd.DataFrame([
        {
            "event_id": "bad_neg_event",
            "instrument": "merchandise_trade_balance",
            "nominal_amount": -8000000000.0,
            "currency": "EUR",
            "amount_usd_normalized": -8720000000.0,
            "flow_type": "trade_settlement",
        }
    ])
    mock_auditor = DimensionalIntegrityAuditor(events_df=bad_df)
    mock_rep = mock_auditor.audit()
    assert mock_rep.signed_amount_violations_count >= 1
    assert mock_rep.errors[0].error_type == "SIGNED_NOMINAL_AMOUNT_ERROR"
    assert mock_rep.errors[0].severity == "HIGH"


def test_dimensional_integrity_fx_verification(duckdb_available):
    """Verifies currency normalizations and FX conversion rates."""
    auditor = DimensionalIntegrityAuditor(duckdb_path=duckdb_available)
    report = auditor.audit()

    # For EUR events that are valid amounts, check FX rate equals 1.09
    for err in report.errors:
        if err.currency == "EUR" and err.nominal_amount != 0:
            assert pytest.approx(err.implied_fx_rate, rel=1e-3) == 1.09


# -------------------------------------------------------------------------
# 3. Temporal Cadence Tests
# -------------------------------------------------------------------------

def test_temporal_cadence_frequency_classification(duckdb_available):
    """Verifies temporal frequency mixing classification and annualized rate equivalents."""
    auditor = TemporalCadenceAuditor(duckdb_path=duckdb_available)
    report = auditor.audit()

    assert report.daily_events_count > 0
    assert report.monthly_events_count > 0
    assert report.quarterly_events_count > 0
    assert report.annual_static_events_count > 0

    # Check daily SOFR repo annualized rate equivalent ($3.007T/day * 252 = $757.764T/yr)
    sofr_metrics = [m for m in report.event_metrics if "sofr_triparty_repo" in m.instrument]
    assert len(sofr_metrics) == 1
    m = sofr_metrics[0]
    assert m.cadence == TemporalCadence.HIGH_FREQUENCY_DAILY
    assert m.annualized_rate_usd == pytest.approx(3.007e12 * 252.0, rel=1e-3)


def test_temporal_cadence_stock_flow_confusion(duckdb_available):
    """Verifies detection of stock vs. flow confusions and path cadence mismatches."""
    auditor = TemporalCadenceAuditor(duckdb_path=duckdb_available)
    report = auditor.audit()

    assert len(report.stock_flow_confusions) >= 5
    # Public debt stocks should be flagged as static stock state variables
    debt_confusions = [c for c in report.stock_flow_confusions if "debt" in c["instrument"] or "debt" in c["event_id"]]
    assert len(debt_confusions) > 0

    assert len(report.path_cadence_mismatches) > 0
    mismatch = report.path_cadence_mismatches[0]
    assert mismatch["velocity_ratio"] >= 10.0


# -------------------------------------------------------------------------
# 4. Graph Topology Tests
# -------------------------------------------------------------------------

def test_graph_topology_connectivity_and_cut_vertices():
    """Verifies graph connectivity metrics and articulation points on 117+ node substrate."""
    auditor = GraphTopologyAuditor()
    report = auditor.audit()

    assert report.total_nodes >= 117
    assert report.total_edges >= 150
    assert report.weakly_connected_components > 0
    assert len(report.articulation_points) > 0

    # French Treasury and import conduit are cut vertices in sovereign trade circuits
    assert "french_republic_tresor" in report.articulation_points or "french_economy_importers" in report.articulation_points


def test_graph_topology_absorbing_sinks():
    """Verifies distinction between legitimate monetary burns and unintended sink traps."""
    auditor = GraphTopologyAuditor()
    report = auditor.audit()

    assert len(report.absorbing_sinks) >= 15
    assert len(report.legitimate_burn_sinks) >= 4
    assert len(report.unintended_sink_traps) >= 8

    # Legitimate burns
    assert "fed_soma_qt_burn_chamber" in report.legitimate_burn_sinks
    assert "corporate_share_buyback_burn_chamber" in report.legitimate_burn_sinks
    assert "fed_on_rrp_buffer_sink" in report.legitimate_burn_sinks

    # Decoy fintech dead-ends
    assert any("fintech" in s or "broker" in s or "credit" in s for s in report.unintended_sink_traps)


def test_graph_topology_critical_node_removal():
    """Verifies route stability under removal of us_triparty_repo_pool and svt_dealers_bnp_socgen."""
    auditor = GraphTopologyAuditor()
    report = auditor.audit()

    assert "us_triparty_repo_pool" in report.critical_node_removals
    repo_impact = report.critical_node_removals["us_triparty_repo_pool"]
    # Phase 3 mitigation: FICC sponsored repo bypass reduces disruption from 100% to 33.3%
    assert repo_impact["disruption_pct"] <= 50.0
    assert len(repo_impact["severed_routes"]) == 1

    assert "svt_dealers_bnp_socgen" in report.critical_node_removals
    svt_impact = report.critical_node_removals["svt_dealers_bnp_socgen"]
    # Phase 3 mitigation: CA-CIB / Natixis secondary syndicate bypass reduces disruption from 66.7% to 33.3%
    assert svt_impact["disruption_pct"] <= 50.0
    assert len(svt_impact["severed_routes"]) == 1


# -------------------------------------------------------------------------
# 5. Unmodeled Risk Estimator Tests
# -------------------------------------------------------------------------

def test_unmodeled_risk_estimator_dark_matter(duckdb_available):
    """Verifies quantitative benchmarking against global dark matter."""
    estimator = UnmodeledRiskEstimator(duckdb_path=duckdb_available)
    report = estimator.audit()

    assert report.total_unmodeled_dark_matter_usd >= 500e12  # Over $500 Trillion remaining gap
    assert report.overall_coverage_ratio_pct < 20.0          # Coverage ~10.9%
    assert report.dark_matter_multiplier > 5.0               # Multiplier > 5x
    assert report.systemic_blindspot_score > 70.0            # High blindspot

    # Check 4 pillars
    benchmarks_by_domain = {b.domain_name: b for b in report.benchmarks}
    assert "BIS OTC Derivatives" in benchmarks_by_domain
    assert "Treasury Basis Trade & Hedge Fund Repo" in benchmarks_by_domain
    assert "Global Trade Statistical Discrepancy (Errors & Omissions)" in benchmarks_by_domain
    assert "Foreign Central Bank Currency Swap Lines (PBOC & Bilateral)" in benchmarks_by_domain

    bis_b = benchmarks_by_domain["BIS OTC Derivatives"]
    assert bis_b.real_world_notional_usd == 600e12
    assert bis_b.modeled_notional_usd == 25e12
    assert bis_b.gap_usd == 575e12

    basis_b = benchmarks_by_domain["Treasury Basis Trade & Hedge Fund Repo"]
    assert basis_b.real_world_notional_usd == 800e9
    assert basis_b.modeled_notional_usd == 800e9
    assert basis_b.gap_usd == 0.0

    trade_b = benchmarks_by_domain["Global Trade Statistical Discrepancy (Errors & Omissions)"]
    assert trade_b.real_world_notional_usd == 175e9
    assert trade_b.modeled_notional_usd == 175e9
    assert trade_b.gap_usd == 0.0

    pboc_b = benchmarks_by_domain["Foreign Central Bank Currency Swap Lines (PBOC & Bilateral)"]
    assert pboc_b.real_world_notional_usd == 550e9
    assert pboc_b.modeled_notional_usd >= 550e9
    assert pboc_b.gap_usd == 0.0


# -------------------------------------------------------------------------
# 6. Integrated End-to-End System Auditor Scorecard Test
# -------------------------------------------------------------------------

def test_system_auditor_end_to_end_scorecard(duckdb_available):
    """Verifies that SystemAuditor synthesizes all audits into an integrated scorecard."""
    auditor = SystemAuditor(duckdb_path=duckdb_available)
    scorecard = auditor.run_full_audit()

    assert isinstance(scorecard, FullAuditScorecard)
    assert 0.0 <= scorecard.system_integrity_score <= 100.0
    assert scorecard.system_integrity_score >= 50.0
    assert scorecard.dimensional_score == 20.0  # Remediated dimensional integrity
    assert scorecard.conservation_score > 5.0
    assert scorecard.temporal_score > 10.0
    assert scorecard.topology_score > 5.0
    assert scorecard.dark_matter_score > 4.0

    assert len(scorecard.high_risk_anomalies) >= 3
    assert len(scorecard.remediation_recommendations) >= 5

    # Check remaining open systemic anomalies
    anomaly_ids = [a["id"] for a in scorecard.high_risk_anomalies]
    assert "ANOMALY-TEMPORAL-01" in anomaly_ids
    assert "ANOMALY-TOPOLOGY-01" in anomaly_ids
    assert "ANOMALY-DARKMATTER-01" in anomaly_ids

    # Negative control: verify detector generates critical anomalies when presented with legacy flawed data
    flawed_df = pd.DataFrame([
        {
            "event_id": "flawed_oil_in",
            "source_entity": "bank_of_russia_cbr_vault",
            "target_entity": "shadow_tanker_energy_arbitrage",
            "amount_usd_normalized": 140e9,
            "nominal_amount": 140e9,
            "currency": "USD",
            "flow_type": "trade_settlement",
            "instrument": "dark_crude_arbitrage",
        },
        {
            "event_id": "flawed_oil_out",
            "source_entity": "shadow_tanker_energy_arbitrage",
            "target_entity": "reserve_bank_of_india_refining_hub",
            "amount_usd_normalized": 55e9,
            "nominal_amount": 55e9,
            "currency": "USD",
            "flow_type": "trade_settlement",
            "instrument": "dark_crude_arbitrage",
        },
        {
            "event_id": "flawed_spread",
            "source_entity": "french_republic_tresor",
            "target_entity": "banque_de_france",
            "amount_usd_normalized": 79.57,
            "nominal_amount": 73.0,
            "currency": "EUR",
            "flow_type": "risk_friction",
            "instrument": "oat_bund_10y_spread_bp",
            "metric_value": 73.0,
        },
    ])
    flawed_auditor = SystemAuditor(events_df=flawed_df)
    flawed_scorecard = flawed_auditor.run_full_audit()
    flawed_anomaly_ids = [a["id"] for a in flawed_scorecard.high_risk_anomalies]
    assert "ANOMALY-CONSERVATION-01" in flawed_anomaly_ids
    assert "ANOMALY-DIMENSIONAL-01" in flawed_anomaly_ids
