"""Private Asset Portfolios & Principal Holdings Harvester.

Integrates local family office, sister operating ventures, scientific compute fleets,
and private real estate assets into the Capital Manifold macro-financial architecture:
1. Layer 0 (Apex Principal): conner_principal_vault (sovereign capital & liquidity allocation).
2. Layer 1 (Operating Sister OpCos):
   - launchfizz_treasury_vault: Studio commercial cashflow & wholesale operating accounts.
   - vesperspatial_actuarial_reserves: Delphi-1.0 catastrophe risk underwriting liquidity.
   - silvera_renewable_packaging: Molded-fiber Capex & ag residue working capital.
3. Layer 2B (Distributed Scientific Fleet):
   - scientific_fleet_compute_pool: TWE / Jarvis / Kinetic compute budget & GPU cluster allocations.
4. Private Assets & Property:
   - valle_rd_asset_ledger: Background real estate holding, mortgage amortizations & equity cushion.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from capital_manifold.core.schema import FlowEvent, FlowType
from capital_manifold.harvesters.base import BaseHarvester
from capital_manifold.storage.duckdb_store import ManifoldStore

logger = logging.getLogger("capital_manifold.harvester.private_assets")

REPORT_DATE = "2026-10-06"

# Quantitative Flow Constants (USD)
CONNER_MMF_YIELD_USD = 450_000.0
CONNER_EQUITY_ENDOWMENT_USD = 1_280_000.0
LAUNCHFIZZ_CREDIT_LINE_USD = 1_850_000.0
LAUNCHFIZZ_EQUITY_INJECTION_USD = 250_000.0
LAUNCHFIZZ_PAYROLL_VENDORS_USD = 1_750_000.0
LAUNCHFIZZ_SAAS_INFRA_USD = 350_000.0
VESPERSPATIAL_COLLATERAL_ESCROW_USD = 2_500_000.0
VESPERSPATIAL_UNDERWRITING_PREMIUMS_USD = 2_500_000.0
SCIENTIFIC_COMPUTE_ENDOWMENT_USD = 480_000.0
SCIENTIFIC_COMPUTE_HARDWARE_USD = 480_000.0
SILVERA_CAPEX_INJECTION_USD = 350_000.0
SILVERA_FEEDSTOCK_TOOLING_USD = 350_000.0
VALLE_RD_EQUITY_CUSHION_USD = 650_000.0
VALLE_RD_MORTGAGE_AMORTIZATION_USD = 120_000.0
VALLE_RD_ESCROW_EQUITY_USD = 530_000.0
COMMERCIAL_BANK_SYSTEMIC_LENDING_USD = 870_972_270_000.0
APPLE_COMPUTE_PROCEEDS_BURN_USD = 480_000.0
PRIME_MMF_YIELD_REPLENISHMENT_USD = 450_000.0


class PrivateAssetsHarvester(BaseHarvester):
    """Harvester for private family office holdings, sister OpCos, and scientific compute fleets."""

    def __init__(self, user_agent: str = "CapitalManifold/1.0 (Private Assets Harvester)"):
        super().__init__(name="private_assets_harvester", user_agent=user_agent)

    def harvest(self) -> List[FlowEvent]:
        """Harvests private asset flows modeling planetary macro transmission into operational accounts."""
        logger.info("Harvesting Private Asset Portfolios & Principal Holdings flows...")
        events: List[FlowEvent] = []

        # =========================================================================
        # 1. LAYER 0 (APEX PRINCIPAL VAULT) & MACRO TRANSMISSION
        # =========================================================================

        # 1a. Yield Transmission: MMF Basin -> Conner Principal Vault ($450k/yr)
        events.append(FlowEvent(
            event_id=f"private_yield_transmission_mmf_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="us_prime_mmf_basin",
            source_jurisdiction="US",
            target_entity="conner_principal_vault",
            target_jurisdiction="US",
            instrument="t_bill_and_prime_mmf_yield_distribution",
            nominal_amount=CONNER_MMF_YIELD_USD,
            currency="USD",
            amount_usd_normalized=CONNER_MMF_YIELD_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=30.0,
            data_source="private_family_office_ledger",
            source_line_item="MMF_TREASURY_BILL_YIELD_PASS_THROUGH",
            confidence=1.0,
            metric_value=450.0,
            raw_payload={"source_facility": "US Prime MMF Basin", "annualized_yield_pct": 5.25},
        ))

        # 1b. MMF Yield Accrual Replenishment ($450k)
        events.append(FlowEvent(
            event_id=f"mmf_yield_accrual_replenishment_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="institutional_cash_liquidity_providers",
            source_jurisdiction="US",
            target_entity="us_prime_mmf_basin",
            target_jurisdiction="US",
            instrument="institutional_mmf_yield_accrual_replenishment",
            nominal_amount=PRIME_MMF_YIELD_REPLENISHMENT_USD,
            currency="USD",
            amount_usd_normalized=PRIME_MMF_YIELD_REPLENISHMENT_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=30.0,
            data_source="private_family_office_ledger",
            source_line_item="INSTITUTIONAL_MMF_INTEREST_ACCRUAL",
            confidence=1.0,
            metric_value=450.0,
        ))

        # 1c. Apex Principal Sovereign Capital Allocation ($1.28M)
        events.append(FlowEvent(
            event_id=f"principal_equity_endowment_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="family_office_principal_endowment",
            source_jurisdiction="US",
            target_entity="conner_principal_vault",
            target_jurisdiction="US",
            instrument="principal_sovereign_equity_capital_allocation",
            nominal_amount=CONNER_EQUITY_ENDOWMENT_USD,
            currency="USD",
            amount_usd_normalized=CONNER_EQUITY_ENDOWMENT_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=360.0,
            data_source="private_family_office_ledger",
            source_line_item="PRINCIPAL_CAPITAL_ALLOCATION_TIER0",
            confidence=1.0,
            metric_value=1280.0,
        ))

        # =========================================================================
        # 2. LAYER 1 (OPERATING SISTER OPCOS)
        # =========================================================================

        # 2a. Operating Credit Line: Commercial Bank Credit Pool -> LaunchFizz Treasury ($1.85M)
        events.append(FlowEvent(
            event_id=f"launchfizz_operating_credit_line_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="us_commercial_bank_credit_pool",
            source_jurisdiction="US",
            target_entity="launchfizz_treasury_vault",
            target_jurisdiction="US",
            instrument="commercial_operating_revenue_and_revolving_line",
            nominal_amount=LAUNCHFIZZ_CREDIT_LINE_USD,
            currency="USD",
            amount_usd_normalized=LAUNCHFIZZ_CREDIT_LINE_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=30.0,
            data_source="launchfizz_commercial_accounting",
            source_line_item="STUDIO_AGENCY_WHOLESALE_REVENUE_LINE",
            confidence=1.0,
            metric_value=1850.0,
        ))

        # 2b. Commercial Bank Systemic Lending Distribution ($870.97227B)
        events.append(FlowEvent(
            event_id=f"commercial_bank_systemic_lending_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="us_commercial_bank_credit_pool",
            source_jurisdiction="US",
            target_entity="us_corporate_and_household_borrowers",
            target_jurisdiction="US",
            instrument="commercial_bank_business_and_household_credit",
            nominal_amount=COMMERCIAL_BANK_SYSTEMIC_LENDING_USD,
            currency="USD",
            amount_usd_normalized=COMMERCIAL_BANK_SYSTEMIC_LENDING_USD,
            flow_type=FlowType.INTERBANK_TRANSFER,
            velocity_turnover_days=1.0,
            data_source="federal_reserve_h8_release",
            source_line_item="COMMERCIAL_BANK_LOANS_AND_LEASES_DOMESTIC",
            confidence=1.0,
            metric_value=870972.27,
        ))

        # 2c. Venture Capital Allocation: Conner Principal Vault -> LaunchFizz Treasury ($250k)
        events.append(FlowEvent(
            event_id=f"launchfizz_equity_injection_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="conner_principal_vault",
            source_jurisdiction="US",
            target_entity="launchfizz_treasury_vault",
            target_jurisdiction="US",
            instrument="venture_capital_equity_injection",
            nominal_amount=LAUNCHFIZZ_EQUITY_INJECTION_USD,
            currency="USD",
            amount_usd_normalized=LAUNCHFIZZ_EQUITY_INJECTION_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=180.0,
            data_source="private_family_office_ledger",
            source_line_item="VENTURE_EQUITY_ALLOCATION_LAUNCHFIZZ",
            confidence=1.0,
            metric_value=250.0,
        ))

        # 2d. LaunchFizz Agency Operating Payroll & Vendor Disbursements ($1.75M)
        events.append(FlowEvent(
            event_id=f"launchfizz_payroll_disbursements_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="launchfizz_treasury_vault",
            source_jurisdiction="US",
            target_entity="agency_operating_payroll_and_vendors",
            target_jurisdiction="US",
            instrument="agency_operating_payroll_and_production_expenses",
            nominal_amount=LAUNCHFIZZ_PAYROLL_VENDORS_USD,
            currency="USD",
            amount_usd_normalized=LAUNCHFIZZ_PAYROLL_VENDORS_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=15.0,
            data_source="launchfizz_commercial_accounting",
            source_line_item="AGENCY_PRODUCTION_PAYROLL_EXPENSES",
            confidence=1.0,
            metric_value=1750.0,
        ))

        # 2e. LaunchFizz Digital Infrastructure & SaaS Vendors ($350k)
        events.append(FlowEvent(
            event_id=f"launchfizz_saas_disbursements_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="launchfizz_treasury_vault",
            source_jurisdiction="US",
            target_entity="commercial_cloud_and_saas_vendors",
            target_jurisdiction="US",
            instrument="commercial_cloud_saas_and_contractor_disbursements",
            nominal_amount=LAUNCHFIZZ_SAAS_INFRA_USD,
            currency="USD",
            amount_usd_normalized=LAUNCHFIZZ_SAAS_INFRA_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=30.0,
            data_source="launchfizz_commercial_accounting",
            source_line_item="COMMERCIAL_SAAS_AND_OPS_DISBURSEMENTS",
            confidence=1.0,
            metric_value=350.0,
        ))

        # 2f. VesperSpatial Catastrophe Reinsurance Premiums Inflow ($2.50M)
        events.append(FlowEvent(
            event_id=f"vesperspatial_underwriting_premiums_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="catastrophe_reinsurance_cedants",
            source_jurisdiction="GLOBAL",
            target_entity="vesperspatial_actuarial_reserves",
            target_jurisdiction="US",
            instrument="delphi_catastrophe_reinsurance_underwriting_premiums",
            nominal_amount=VESPERSPATIAL_UNDERWRITING_PREMIUMS_USD,
            currency="USD",
            amount_usd_normalized=VESPERSPATIAL_UNDERWRITING_PREMIUMS_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=360.0,
            data_source="vesperspatial_actuarial_ledger",
            source_line_item="DELPHI_CAT_REINSURANCE_PREMIUMS_WRITTEN",
            confidence=1.0,
            metric_value=2500.0,
        ))

        # 2g. Underwriting Collateral Escrow: VesperSpatial -> US Treasuries Custody ($2.50M)
        # $2.50M T-bill collateral pledge backing $25M PML underwriting capacity
        events.append(FlowEvent(
            event_id=f"vesperspatial_collateral_escrow_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="vesperspatial_actuarial_reserves",
            source_jurisdiction="US",
            target_entity="us_treasuries_custody",
            target_jurisdiction="US",
            instrument="statutory_reinsurance_collateral_escrow_pledge",
            nominal_amount=VESPERSPATIAL_COLLATERAL_ESCROW_USD,
            currency="USD",
            amount_usd_normalized=VESPERSPATIAL_COLLATERAL_ESCROW_USD,
            flow_type=FlowType.REPO_COLLATERAL,
            velocity_turnover_days=360.0,
            data_source="vesperspatial_actuarial_ledger",
            source_line_item="DELPHI_PML_CUSTODIAL_COLLATERAL_ESCROW",
            confidence=1.0,
            metric_value=2500.0,
            raw_payload={"pml_capacity_usd": 25_000_000.0, "collateral_ratio_pct": 10.0},
        ))

        # 2h. Clean Packaging Capex: Conner Principal Vault -> Silvera Renewable Packaging ($350k)
        events.append(FlowEvent(
            event_id=f"silvera_capex_injection_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="conner_principal_vault",
            source_jurisdiction="US",
            target_entity="silvera_renewable_packaging",
            target_jurisdiction="US",
            instrument="molded_fiber_capex_and_working_capital_allocation",
            nominal_amount=SILVERA_CAPEX_INJECTION_USD,
            currency="USD",
            amount_usd_normalized=SILVERA_CAPEX_INJECTION_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=180.0,
            data_source="silvera_industrial_accounting",
            source_line_item="MOLDED_FIBER_WORKING_CAPITAL_INJECTION",
            confidence=1.0,
            metric_value=350.0,
        ))

        # 2i. Silvera Feedstock & Tooling Procurement ($350k)
        events.append(FlowEvent(
            event_id=f"silvera_feedstock_tooling_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="silvera_renewable_packaging",
            source_jurisdiction="US",
            target_entity="molded_fiber_tooling_and_feedstock_vendors",
            target_jurisdiction="US",
            instrument="industrial_tooling_and_bio_resin_procurement",
            nominal_amount=SILVERA_FEEDSTOCK_TOOLING_USD,
            currency="USD",
            amount_usd_normalized=SILVERA_FEEDSTOCK_TOOLING_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=60.0,
            data_source="silvera_industrial_accounting",
            source_line_item="INDUSTRIAL_CAPEX_MOLDED_FIBER_TOOLING",
            confidence=1.0,
            metric_value=350.0,
        ))

        # =========================================================================
        # 3. LAYER 2B (DISTRIBUTED SCIENTIFIC FLEET)
        # =========================================================================

        # 3a. Scientific Compute Endowment: Conner Principal Vault -> Compute Pool ($480k)
        events.append(FlowEvent(
            event_id=f"scientific_compute_endowment_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="conner_principal_vault",
            source_jurisdiction="US",
            target_entity="scientific_fleet_compute_pool",
            target_jurisdiction="US",
            instrument="scientific_fleet_gpu_and_api_compute_endowment",
            nominal_amount=SCIENTIFIC_COMPUTE_ENDOWMENT_USD,
            currency="USD",
            amount_usd_normalized=SCIENTIFIC_COMPUTE_ENDOWMENT_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=90.0,
            data_source="scientific_fleet_governance",
            source_line_item="TWE_JARVIS_KINETIC_COMPUTE_BUDGET",
            confidence=1.0,
            metric_value=480.0,
            raw_payload={"supported_fleets": ["TWE", "Jarvis", "Kinetic", "Kalshi-Calibration"]},
        ))

        # 3b. Compute Vendor Disbursements: Compute Pool -> Apple BigTech Treasury ($480k)
        events.append(FlowEvent(
            event_id=f"compute_vendor_disbursements_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="scientific_fleet_compute_pool",
            source_jurisdiction="US",
            target_entity="apple_bigtech_treasury_vault",
            target_jurisdiction="US",
            instrument="cloud_compute_and_silicon_hardware_disbursements",
            nominal_amount=SCIENTIFIC_COMPUTE_HARDWARE_USD,
            currency="USD",
            amount_usd_normalized=SCIENTIFIC_COMPUTE_HARDWARE_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=30.0,
            data_source="scientific_fleet_governance",
            source_line_item="INFRASTRUCTURE_HARDWARE_VENDOR_PAYMENTS",
            confidence=1.0,
            metric_value=480.0,
        ))

        # 3c. Apple BigTech Hardware Revenue Buyback Sweep ($480k)
        events.append(FlowEvent(
            event_id=f"apple_hardware_revenue_buyback_sweep_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="apple_bigtech_treasury_vault",
            source_jurisdiction="US",
            target_entity="corporate_share_buyback_burn_chamber",
            target_jurisdiction="US",
            instrument="hardware_revenue_reinvested_into_share_repurchase",
            nominal_amount=APPLE_COMPUTE_PROCEEDS_BURN_USD,
            currency="USD",
            amount_usd_normalized=APPLE_COMPUTE_PROCEEDS_BURN_USD,
            flow_type=FlowType.QT_BURN,
            velocity_turnover_days=1.0,
            data_source="apple_sec_edgar",
            source_line_item="SHARE_REPURCHASE_PROGRAM_ALLOCATION",
            confidence=1.0,
            metric_value=480.0,
        ))

        # =========================================================================
        # 4. PRIVATE ASSETS & PROPERTY (VALLE RD REAL ESTATE)
        # =========================================================================

        # 4a. Real Estate Equity Cushion: Conner Principal Vault -> Valle Rd Asset Ledger ($650k)
        events.append(FlowEvent(
            event_id=f"valle_rd_equity_cushion_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="conner_principal_vault",
            source_jurisdiction="US",
            target_entity="valle_rd_asset_ledger",
            target_jurisdiction="US",
            instrument="private_real_estate_equity_capitalization",
            nominal_amount=VALLE_RD_EQUITY_CUSHION_USD,
            currency="USD",
            amount_usd_normalized=VALLE_RD_EQUITY_CUSHION_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=360.0,
            data_source="valle_rd_property_records",
            source_line_item="EQUITY_COLLATERAL_CUSHION_VALLE_RD",
            confidence=1.0,
            metric_value=650.0,
        ))

        # 4b. Mortgage Debt Service Amortization: Valle Rd -> US Commercial Bank Credit Pool ($120k)
        events.append(FlowEvent(
            event_id=f"valle_rd_mortgage_amortization_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="valle_rd_asset_ledger",
            source_jurisdiction="US",
            target_entity="us_commercial_bank_credit_pool",
            target_jurisdiction="US",
            instrument="mortgage_debt_service_principal_and_interest",
            nominal_amount=VALLE_RD_MORTGAGE_AMORTIZATION_USD,
            currency="USD",
            amount_usd_normalized=VALLE_RD_MORTGAGE_AMORTIZATION_USD,
            flow_type=FlowType.INTERBANK_TRANSFER,
            velocity_turnover_days=30.0,
            data_source="valle_rd_property_records",
            source_line_item="MORTGAGE_PRINCIPAL_AND_INTEREST_AMORTIZATION",
            confidence=1.0,
            metric_value=120.0,
        ))

        # 4c. Real Estate Retained Equity Cushion & Capital Escrow ($530k)
        events.append(FlowEvent(
            event_id=f"valle_rd_retained_equity_escrow_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T12:00:00Z",
            period_label=REPORT_DATE,
            source_entity="valle_rd_asset_ledger",
            source_jurisdiction="US",
            target_entity="valle_rd_property_equity_escrow",
            target_jurisdiction="US",
            instrument="property_equity_appreciation_and_escrow_cushion",
            nominal_amount=VALLE_RD_ESCROW_EQUITY_USD,
            currency="USD",
            amount_usd_normalized=VALLE_RD_ESCROW_EQUITY_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=360.0,
            data_source="valle_rd_property_records",
            source_line_item="RETAINED_EQUITY_VALUE_CUSHION",
            confidence=1.0,
            metric_value=530.0,
        ))

        logger.info(f"Harvested {len(events)} Private Asset Portfolios & Principal Holdings flow events.")
        return events

    def harvest_and_store(self, store: Optional[ManifoldStore] = None) -> List[FlowEvent]:
        """Harvests events and persists them to DuckDB and Parquet."""
        owns_store = store is None
        if store is None:
            store = ManifoldStore()

        events = self.harvest()
        count = store.insert_flow_events(events)
        store.export_parquet()
        logger.info(f"Persisted {count} private asset flow events to DuckDB and Parquet.")

        if owns_store:
            store.close()

        return events
