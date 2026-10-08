"""Comprehensive Unit & Regression Tests for Siphon & Structural Discrepancy Hunter.

Tests:
1. SiphonHunter initialization across DuckDB, custom DataFrames, and substrates.
2. Bilateral mirror trade discrepancy scanner (Urals crude $85B gap, Swiss gold $33B loop, US-China $109B gap).
3. Absorbing sink & dark conduit hunter (Kirchhoff conservation, $180B Russian trapped capital, $25B Dubai freight margin).
4. Custody nominee triangulation (Belgium Euroclear 43-sigma, China PBOC SAFE $265B attribution, Luxembourg, Cayman).
5. IMF Net Errors & Omissions (NEO) capital flight allocation ($180B across maritime, crypto, real assets).
6. Full report generation, JSON serialization, and tolerance sensitivity.
7. Synthetic custom DataFrame ingestion and leak detection.
8. Web API integration (/api/siphon_report).
"""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from capital_manifold.adversarial.siphon_hunter import (
    DEFAULT_CIF_FOB_MARGIN_PCT,
    DEFAULT_DUCKDB_PATH,
    GLOBAL_NEO_ANNUAL_DISCREPANCY_USD,
    RUSSIAN_URALS_EXPORT_FOB_USD,
    INDIA_REPORTED_URALS_IMPORT_CIF_USD,
    SWISS_RAW_GOLD_DORE_IMPORTS_USD,
    SWISS_REFINED_BULLION_EXPORTS_USD,
    US_CENSUS_REPORTED_CHINA_IMPORTS_USD,
    CHINA_CUSTOMS_REPORTED_US_EXPORTS_USD,
    CUSTODIAN_NOMINEE_PROFILES,
    SiphonHunter,
    SiphonAuditReport,
    BilateralTradeDiscrepancy,
    AbsorbingConduitAnomaly,
    CustodyNomineeAnomaly,
    StatisticalResidualAllocation,
)
from capital_manifold.web.app import app


@pytest.fixture
def hunter() -> SiphonHunter:
    return SiphonHunter()


# -------------------------------------------------------------------------
# 1. Initialization Tests
# -------------------------------------------------------------------------

def test_siphon_hunter_initialization(hunter: SiphonHunter):
    """Verifies clean initialization and access to underlying database."""
    assert hunter.duckdb_path == DEFAULT_DUCKDB_PATH
    df = hunter._get_dataframe()
    assert not df.empty, "DuckDB flow_events table should not be empty"
    assert len(df) >= 100


# -------------------------------------------------------------------------
# 2. Bilateral Mirror Trade Discrepancy Tests
# -------------------------------------------------------------------------

def test_audit_bilateral_trade_discrepancies(hunter: SiphonHunter):
    """Verifies bilateral mirror trade discrepancies across Urals crude, Swiss gold, and US-China trade."""
    discrepancies = hunter.audit_bilateral_trade_discrepancies(cif_fob_adjustment_pct=6.0)
    assert len(discrepancies) == 3

    # Case 1: Russian Urals crude maritime arbitrage
    urals = next(d for d in discrepancies if "RUSSIA-URALS" in d.corridor_id)
    assert urals.exporter_country.startswith("RU")
    assert urals.importer_country.startswith("IN")
    assert urals.reported_export_fob_usd == pytest.approx(RUSSIAN_URALS_EXPORT_FOB_USD, rel=1e-3)
    assert urals.reported_import_cif_usd == pytest.approx(INDIA_REPORTED_URALS_IMPORT_CIF_USD, rel=1e-3)
    assert urals.raw_discrepancy_usd == pytest.approx(85.0e9, rel=1e-3)
    assert urals.adjusted_discrepancy_usd == pytest.approx(93.4e9, rel=1e-3)
    assert urals.discrepancy_type == "SHADOW_MARITIME_DIVERSION"
    assert urals.severity == "CRITICAL"
    assert any("shadow_tanker" in inter for inter in urals.suspected_intermediaries)

    # Case 2: Swiss precious metals refinery loop
    gold = next(d for d in discrepancies if "SWISS-GOLD" in d.corridor_id)
    assert gold.exporter_country.startswith("CH")
    assert gold.reported_export_fob_usd == pytest.approx(SWISS_REFINED_BULLION_EXPORTS_USD, rel=1e-3)
    assert gold.reported_import_cif_usd == pytest.approx(SWISS_RAW_GOLD_DORE_IMPORTS_USD, rel=1e-3)
    assert gold.raw_discrepancy_usd == pytest.approx(33.0e9, rel=1e-3)
    assert gold.discrepancy_type == "REFINERY_VALUE_WASHING"
    assert gold.severity == "HIGH"
    assert any("refineries" in inter for inter in gold.suspected_intermediaries)

    # Case 3: US-China bilateral trade gap
    us_cn = next(d for d in discrepancies if "US-CHINA" in d.corridor_id)
    assert us_cn.exporter_country.startswith("CN")
    assert us_cn.importer_country.startswith("US")
    assert us_cn.reported_export_fob_usd == pytest.approx(CHINA_CUSTOMS_REPORTED_US_EXPORTS_USD, rel=1e-3)
    assert us_cn.reported_import_cif_usd == pytest.approx(US_CENSUS_REPORTED_CHINA_IMPORTS_USD, rel=1e-3)
    assert us_cn.raw_discrepancy_usd == pytest.approx(109.0e9, rel=1e-3)
    assert us_cn.adjusted_discrepancy_usd == pytest.approx(89.92e9, rel=1e-3)
    assert us_cn.discrepancy_type == "HONG_KONG_RE_INVOICING_MARKUP"
    assert us_cn.severity == "HIGH"


def test_bilateral_trade_cif_fob_margin_sensitivity(hunter: SiphonHunter):
    """Verifies that varying CIF/FOB margin percentages adjusts expected import amounts accordingly."""
    # Test at 5.0%
    d_5 = hunter.audit_bilateral_trade_discrepancies(cif_fob_adjustment_pct=5.0)
    u_5 = next(d for d in d_5 if "RUSSIA-URALS" in d.corridor_id)
    assert u_5.expected_import_cif_usd == pytest.approx(140.0e9 * 1.05, rel=1e-3)

    # Test at 8.0%
    d_8 = hunter.audit_bilateral_trade_discrepancies(cif_fob_adjustment_pct=8.0)
    u_8 = next(d for d in d_8 if "RUSSIA-URALS" in d.corridor_id)
    assert u_8.expected_import_cif_usd == pytest.approx(140.0e9 * 1.08, rel=1e-3)


# -------------------------------------------------------------------------
# 3. Absorbing Sink & Dark Conduit Tests
# -------------------------------------------------------------------------

def test_audit_absorbing_conduits(hunter: SiphonHunter):
    """Verifies identification of trapped capital basins, shadow tanker margins, and commodity fee skimming."""
    anomalies = hunter.audit_absorbing_conduits()
    assert len(anomalies) >= 3

    # Russian Trapped Capital Basin: $180B in, $0 domestic repatriation
    trapped = next(a for a in anomalies if a.entity_id == "russia_offshore_shadow_capital_basin")
    assert trapped.total_inflow_usd >= 180.0e9
    assert trapped.total_outflow_usd == 0.0
    assert trapped.siphoned_volume_usd >= 180.0e9
    assert trapped.retention_ratio_pct == 100.0
    assert trapped.anomaly_classification == "TRAPPED_CAPITAL_BASIN"
    assert trapped.severity == "CRITICAL"
    assert any("gazprombank" in cp for cp in trapped.suspected_counterparties)

    # Shadow Tanker Energy Arbitrage: $25B Dubai freight margin
    tanker = next(a for a in anomalies if a.entity_id == "shadow_tanker_energy_arbitrage")
    assert tanker.total_inflow_usd >= 140.0e9
    assert tanker.siphoned_volume_usd == pytest.approx(25.0e9, rel=1e-3)
    assert tanker.anomaly_classification == "UNRECORDED_MARGIN_EXTRACTION"
    assert tanker.severity == "HIGH"
    assert any("uae" in cp.lower() for cp in tanker.suspected_counterparties)

    # African Critical Minerals: $2.2B commodity dealer skimming
    minerals = next(a for a in anomalies if a.entity_id == "africa_critical_minerals_debt_conduit")
    assert minerals.siphoned_volume_usd == pytest.approx(2.2e9, rel=1e-3)
    assert minerals.anomaly_classification == "COMMODITY_FEE_SKIMMING"


# -------------------------------------------------------------------------
# 4. Custody Nominee Triangulation Tests
# -------------------------------------------------------------------------

def test_audit_custody_nominees(hunter: SiphonHunter):
    """Verifies that international custodian hubs exceeding 5-sigma capacity are flagged and triangulated."""
    nominees = hunter.audit_custody_nominees(sigma_threshold=5.0)
    assert len(nominees) == 5

    # Check Belgium Euroclear: > 40 sigma, China PBOC SAFE beneficial attribution
    belgium = next(n for n in nominees if n.custodian_entity == "belgium_euroclear_custody")
    assert belgium.reported_treasury_holdings_usd >= 330.0e9
    assert belgium.estimated_domestic_capacity_usd == 28.0e9
    assert belgium.excess_nominee_holdings_usd >= 300.0e9
    assert belgium.nominee_intensity_ratio >= 10.0
    assert belgium.sigma_deviation >= 40.0
    assert belgium.severity == "CRITICAL"

    # Beneficial ownership triangulation: China PBOC SAFE holds ~87.4%
    assert len(belgium.triangulated_beneficial_owners) >= 1
    safe = belgium.triangulated_beneficial_owners[0]
    assert "PBOC SAFE" in safe.beneficial_owner
    assert safe.attributed_pct == pytest.approx(87.4, rel=1e-2)
    assert safe.attributed_volume_usd >= 260.0e9

    # Check Cayman Islands: extreme outlier > 700 sigma (basis trade hedge funds)
    cayman = next(n for n in nominees if n.custodian_entity == "offshore_cayman_hedge_pool")
    assert cayman.reported_treasury_holdings_usd >= 280.0e9
    assert cayman.estimated_domestic_capacity_usd == 1.5e9
    assert cayman.sigma_deviation >= 700.0
    assert any("Basis Trade" in bo.beneficial_owner for bo in cayman.triangulated_beneficial_owners)

    # Check Luxembourg Clearstream / UCITS
    lux = next(n for n in nominees if n.custodian_entity == "luxembourg_ucits_pool")
    assert lux.excess_nominee_holdings_usd >= 300.0e9

    # Check Swiss Banks UBS
    swiss = next(n for n in nominees if n.custodian_entity == "ubs_group_consolidated_gsib")
    assert swiss.excess_nominee_holdings_usd >= 300.0e9

    # Check UK London Eurodollar Pool
    uk = next(n for n in nominees if n.custodian_entity == "london_eurodollar_pool")
    assert uk.excess_nominee_holdings_usd >= 500.0e9


def test_custody_nominee_sigma_filtering(hunter: SiphonHunter):
    """Verifies that increasing sigma threshold filters out lower-sigma custodian hubs."""
    high_sigma = hunter.audit_custody_nominees(sigma_threshold=100.0)
    # Only extreme outliers like Cayman (sigma > 700) should survive threshold of 100
    assert len(high_sigma) == 1
    assert high_sigma[0].custodian_entity == "offshore_cayman_hedge_pool"


# -------------------------------------------------------------------------
# 5. IMF Net Errors & Omissions (NEO) Tests
# -------------------------------------------------------------------------

def test_audit_statistical_residuals(hunter: SiphonHunter):
    """Verifies decomposition of $180B global Net Errors & Omissions across 3 dark vectors."""
    neo = hunter.audit_statistical_residuals()
    assert neo.global_neo_annual_discrepancy_usd == GLOBAL_NEO_ANNUAL_DISCREPANCY_USD
    assert neo.modeled_neo_in_manifold_usd >= 170.0e9
    assert neo.unmodeled_neo_gap_usd <= 10.0e9

    assert len(neo.allocated_vectors) == 3
    total_alloc_pct = sum(v["allocation_pct"] for v in neo.allocated_vectors)
    assert total_alloc_pct == pytest.approx(100.0, abs=1e-5)

    total_alloc_usd = sum(v["allocated_amount_usd"] for v in neo.allocated_vectors)
    assert total_alloc_usd == pytest.approx(GLOBAL_NEO_ANNUAL_DISCREPANCY_USD, rel=1e-3)

    # Vector 1: Shadow maritime fleet (45%)
    v1 = next(v for v in neo.allocated_vectors if "SHADOW-MARITIME" in v["vector_id"])
    assert v1["allocation_pct"] == 45.0
    assert v1["allocated_amount_usd"] == pytest.approx(81.0e9, rel=1e-3)

    # Vector 2: Non-bank informal settlement (35%)
    v2 = next(v for v in neo.allocated_vectors if "NONBANK-INFORMAL" in v["vector_id"])
    assert v2["allocation_pct"] == 35.0
    assert v2["allocated_amount_usd"] == pytest.approx(63.0e9, rel=1e-3)

    # Vector 3: Offshore real asset sinks (20%)
    v3 = next(v for v in neo.allocated_vectors if "OFFSHORE-REAL-ASSET" in v["vector_id"])
    assert v3["allocation_pct"] == 20.0
    assert v3["allocated_amount_usd"] == pytest.approx(36.0e9, rel=1e-3)


# -------------------------------------------------------------------------
# 6. Master Report Generation & Serialization Tests
# -------------------------------------------------------------------------

def test_generate_siphon_report_and_serialization(hunter: SiphonHunter, tmp_path: Path):
    """Verifies complete synthesis, grand totals, top critical leaks, and JSON persistence."""
    out_file = tmp_path / "test_siphon_report.json"
    report = hunter.generate_siphon_report(output_path=out_file)

    assert isinstance(report, SiphonAuditReport)
    assert report.total_siphoned_volume_usd >= 250.0e9
    assert report.total_discrepancy_volume_usd >= 400.0e9
    assert len(report.bilateral_discrepancies) == 3
    assert len(report.absorbing_conduits) >= 3
    assert len(report.custody_nominees) == 5
    assert len(report.top_critical_leaks) >= 5
    assert len(report.suspected_intermediaries) >= 15
    assert len(report.remediation_actions) >= 4

    # Top leak must be the Russian trapped capital basin ($180B)
    assert report.top_critical_leaks[0]["volume_usd"] >= 180.0e9

    # JSON persistence check
    assert out_file.exists()
    with open(out_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["total_siphoned_volume_usd"] == report.total_siphoned_volume_usd
    assert data["total_discrepancy_volume_usd"] == report.total_discrepancy_volume_usd
    assert len(data["bilateral_discrepancies"]) == 3
    assert len(data["custody_nominees"]) == 5


# -------------------------------------------------------------------------
# 7. Custom Synthetic Data Ingestion Tests
# -------------------------------------------------------------------------

def test_siphon_hunter_custom_events_dataframe():
    """Verifies that SiphonHunter correctly operates over custom mocked DataFrames."""
    mock_df = pd.DataFrame([
        {
            "event_id": "mock_shadow_tanker_in",
            "source_entity": "mock_cbr",
            "target_entity": "shadow_tanker_energy_arbitrage",
            "amount_usd_normalized": 200.0e9,
            "nominal_amount": 200.0e9,
            "currency": "USD",
            "flow_type": "trade_settlement",
            "instrument": "urals_crude",
        },
        {
            "event_id": "mock_india_in",
            "source_entity": "shadow_tanker_energy_arbitrage",
            "target_entity": "reserve_bank_of_india_refining_hub",
            "amount_usd_normalized": 50.0e9,
            "nominal_amount": 50.0e9,
            "currency": "USD",
            "flow_type": "trade_settlement",
            "instrument": "refined_crude",
        },
    ])

    custom_hunter = SiphonHunter(events_df=mock_df)
    discrepancies = custom_hunter.audit_bilateral_trade_discrepancies(cif_fob_adjustment_pct=6.0)
    urals = next(d for d in discrepancies if "RUSSIA-URALS" in d.corridor_id)

    # In mock data: export is $200B, import is $50B -> raw gap is $150B
    assert urals.reported_export_fob_usd == 200.0e9
    assert urals.reported_import_cif_usd == 50.0e9
    assert urals.raw_discrepancy_usd == 150.0e9
    assert urals.expected_import_cif_usd == 200.0e9 * 1.06


# -------------------------------------------------------------------------
# 8. Web API Integration Test
# -------------------------------------------------------------------------

def test_web_api_siphon_report_endpoint():
    """Verifies GET /api/siphon_report returns 200 OK and valid structured intelligence."""
    client = TestClient(app)
    response = client.get("/api/siphon_report")
    assert response.status_code == 200
    data = response.json()

    assert "total_siphoned_volume_usd" in data
    assert "total_discrepancy_volume_usd" in data
    assert "bilateral_discrepancies" in data
    assert "absorbing_conduits" in data
    assert "custody_nominees" in data
    assert "statistical_residual_allocation" in data
    assert "top_critical_leaks" in data
    assert "suspected_intermediaries" in data
    assert data["total_siphoned_volume_usd"] >= 250.0e9
