"""Global Macro Dark Matter Harvester.

Ingests shadow liquidity, off-balance-sheet commitments, and unmodeled macro risk:
1. BIS OTC Derivatives: $25T Gross Market Value ($600T Notional)
2. DTCC Treasury Basis Trade: $800B Cash-Futures Repo Arbitrage
3. PBOC Bilateral Currency Swap Lines: $550B Cross-Border Liquidity Facility
4. IMF Global Trade Discrepancy: $175B Net Errors & Omissions Capital Flight
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from capital_manifold.core.schema import FlowEvent, FlowType
from capital_manifold.harvesters.base import BaseHarvester
from capital_manifold.storage.duckdb_store import ManifoldStore

logger = logging.getLogger("capital_manifold.harvester.dark_matter")

REPORT_DATE = "2026-10-06"
BIS_OTC_GMV_USD = 25.0e12
BIS_OTC_NOTIONAL_USD = 600.0e12
DTCC_BASIS_TRADE_REPO_USD = 800.0e9
PBOC_BILATERAL_SWAPS_USD = 550.0e9
IMF_ERRORS_OMISSIONS_USD = 175.0e9


class DarkMatterHarvester(BaseHarvester):
    """Harvester for off-balance-sheet shadow liquidity and global dark matter commitments."""

    def __init__(self, user_agent: str = "CapitalManifold/1.0 (Dark Matter Harvester)"):
        super().__init__(name="dark_matter_harvester", user_agent=user_agent)

    def harvest(self) -> List[FlowEvent]:
        """Harvests the four canonical pillars of global macro dark matter."""
        logger.info("Harvesting Global Macro Dark Matter flows (BIS, DTCC, PBOC, IMF)...")
        events: List[FlowEvent] = []

        # 1. BIS OTC Derivatives Gross Market Value ($25T GMV, $600T Notional)
        events.append(FlowEvent(
            event_id=f"bis_otc_derivatives_gmv_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="svt_dealers_bnp_socgen",
            source_jurisdiction="FR",
            target_entity="london_eurodollar_pool",
            target_jurisdiction="UK",
            instrument="bis_otc_derivatives_gross_market_value",
            nominal_amount=BIS_OTC_GMV_USD,
            currency="USD",
            amount_usd_normalized=BIS_OTC_GMV_USD,
            flow_type=FlowType.SYNTHETIC_DERIVATIVE,
            velocity_turnover_days=1.0,
            data_source="bis_derivatives_statistics",
            source_line_item="OTC_DERIVATIVES_GROSS_MARKET_VALUE_SEMIANNUAL",
            confidence=1.0,
            metric_value=600.0,
            raw_payload={
                "gross_market_value_usd": BIS_OTC_GMV_USD,
                "notional_outstanding_usd": BIS_OTC_NOTIONAL_USD,
                "asset_class": "Interest Rate & FX Swaps",
            },
        ))

        # 2. DTCC Treasury Basis Trade Repo ($800B)
        events.append(FlowEvent(
            event_id=f"dtcc_treasury_basis_trade_repo_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="offshore_cayman_hedge_pool",
            source_jurisdiction="KY",
            target_entity="us_triparty_repo_pool",
            target_jurisdiction="US",
            instrument="dtcc_treasury_cash_futures_basis_repo",
            nominal_amount=DTCC_BASIS_TRADE_REPO_USD,
            currency="USD",
            amount_usd_normalized=DTCC_BASIS_TRADE_REPO_USD,
            flow_type=FlowType.REPO_COLLATERAL,
            velocity_turnover_days=1.0,
            data_source="dtcc_ficc_repo_benchmarks",
            source_line_item="SPONSORED_SERVICE_TREASURY_BASIS_VOLUME",
            confidence=0.95,
            metric_value=800.0,
            raw_payload={
                "repo_facility": "FICC Sponsored Repo",
                "underlying": "UST Cash vs CME Futures",
            },
        ))

        # 3. PBOC Bilateral Currency Swaps ($550B)
        events.append(FlowEvent(
            event_id=f"pboc_bilateral_swap_network_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="pboc_safe_foreign_reserves",
            source_jurisdiction="CN",
            target_entity="foreign_export_economies",
            target_jurisdiction="WORLD",
            instrument="pboc_bilateral_currency_swap_network",
            nominal_amount=PBOC_BILATERAL_SWAPS_USD,
            currency="USD",
            amount_usd_normalized=PBOC_BILATERAL_SWAPS_USD,
            flow_type=FlowType.BILATERAL_SWAP,
            velocity_turnover_days=90.0,
            data_source="pboc_monetary_policy_report",
            source_line_item="BILATERAL_LOCAL_CURRENCY_SWAP_AGREEMENTS",
            confidence=1.0,
            metric_value=550.0,
            raw_payload={
                "agreements_count": 40,
                "total_credit_line_usd": PBOC_BILATERAL_SWAPS_USD,
            },
        ))

        # 4. IMF Global Trade Errors and Omissions ($175B)
        events.append(FlowEvent(
            event_id=f"imf_global_trade_discrepancy_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="foreign_export_economies",
            source_jurisdiction="WORLD",
            target_entity="offshore_cayman_hedge_pool",
            target_jurisdiction="KY",
            instrument="imf_global_trade_errors_and_omissions",
            nominal_amount=IMF_ERRORS_OMISSIONS_USD,
            currency="USD",
            amount_usd_normalized=IMF_ERRORS_OMISSIONS_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=180.0,
            data_source="imf_balance_of_payments_statistics",
            source_line_item="GLOBAL_CURRENT_ACCOUNT_STATISTICAL_DISCREPANCY",
            confidence=0.90,
            metric_value=175.0,
            raw_payload={
                "asymmetry_type": "Global Net Errors and Omissions",
                "capital_flight_est_usd": IMF_ERRORS_OMISSIONS_USD,
            },
        ))

        logger.info(f"Harvested {len(events)} Global Macro Dark Matter flow events.")
        return events

    def harvest_and_store(self, store: Optional[ManifoldStore] = None) -> List[FlowEvent]:
        """Harvests events and persists them to DuckDB and Parquet."""
        owns_store = store is None
        if store is None:
            store = ManifoldStore()

        events = self.harvest()
        count = store.insert_flow_events(events)
        store.export_parquet()
        logger.info(f"Persisted {count} dark matter flow events to DuckDB and Parquet.")

        if owns_store:
            store.close()

        return events
