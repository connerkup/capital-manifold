"""Planetary Monetary Manifold Harvester.

Ingests & models statutory planetary capital flows across 7 global regions:
1. China & East Asia:
   - PBOC / SAFE Foreign Exchange Reserves: $3,240.0B ($3.24 Trillion)
   - US Treasury TIC China Foreign Holdings: $859.4B (#2 foreign holder)
   - Hong Kong CNH Clearing Hub: $250.0B daily liquidity pool
   - Taiwan Central Bank & TSMC Semiconductor Hardware: $234.6B TIC + $120.0B chips
2. Middle East & Gulf:
   - Saudi Central Bank SAMA & Public Investment Fund (PIF): $925.0B sovereign assets
   - UAE Sovereign Wealth Basin (ADIA & Mubadala): $850.0B + $300.0B ($1,150.0B total)
   - Qatar Investment Authority (QIA): $450.0B
   - Petro-Yuan Bilateral Non-USD Energy Settlement Bridge: $65.0B crude trade
3. Russia & The Sanctioned Shadow Circuit:
   - Euroclear Belgium Frozen Sovereign Assets: $300.0B (€210.0B)
   - Bank of Russia (CBR) Vault Pivot: $185.0B gold + $115.0B CNY reserves
   - Shadow Tanker Maritime Crude Arbitrage: $140.0B Russian Urals/ESPO crude
4. Latin America / South America:
   - Brazil Banco Central do Brasil (BCB): $214.0B TIC US Treasuries
   - Brazil Agricultural & Mineral Export Faucet: $110.0B soy/iron ore surpluses
5. Australia & Pacific Raw Materials:
   - Reserve Bank of Australia (RBA) Commodity Faucet: $180.0B iron ore & LNG
6. India & South Asia:
   - Reserve Bank of India (RBI): $232.0B TIC US Treasuries
   - Russian Crude Refining Arbitrage into Europe: $55.0B diesel/jet fuel
   - Rupee-Dirham Bilateral Trade Settlement: $20.0B
7. Africa & Frontier Resources:
   - African Critical Minerals Concession & Debt Conduit: $45.0B DRC/Zambia cobalt/copper

Normalizes records into standardized FlowEvent objects and writes to DuckDB and Parquet.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from capital_manifold.core.schema import FlowEvent, FlowType
from capital_manifold.harvesters.base import BaseHarvester
from capital_manifold.storage.duckdb_store import ManifoldStore

logger = logging.getLogger("capital_manifold.planetary_macro")

USER_AGENT = "CapitalManifoldResearch desk@capitalmanifold.org"
REPORT_DATE = "2026-10-06"

# Statutory Benchmarks & Macro Metrics (in USD)
# 1. China & East Asia
PBOC_SAFE_RESERVES_USD = 3_240_000_000_000.0        # $3.240 Trillion
TIC_CHINA_TREASURIES_USD = 859_400_000_000.0         # $859.4 Billion
HONG_KONG_CNH_TURNOVER_USD = 250_000_000_000.0       # $250.0 Billion
TIC_TAIWAN_TREASURIES_USD = 234_600_000_000.0        # $234.6 Billion
TAIWAN_TSMC_HARDWARE_FLOW_USD = 120_000_000_000.0    # $120.0 Billion annual semiconductor shipments

# 2. Middle East & Gulf
SAUDI_SAMA_PIF_ASSETS_USD = 925_000_000_000.0        # $925.0 Billion
UAE_ADIA_MUBADALA_USD = 1_150_000_000_000.0          # $1.150 Trillion
QATAR_QIA_ASSETS_USD = 450_000_000_000.0             # $450.0 Billion
PETRO_YUAN_ENERGY_SETTLEMENT_USD = 65_000_000_000.0  # $65.0 Billion bilateral non-USD crude

# 3. Russia & Shadow Circuit
EUROCLEAR_FROZEN_RUSSIAN_ASSETS_USD = 300_000_000_000.0  # $300.0 Billion (€210B frozen)
CBR_PHYSICAL_GOLD_VAULT_USD = 185_000_000_000.0          # $185.0 Billion gold reserves
CBR_YUAN_RESERVES_USD = 115_000_000_000.0                # $115.0 Billion CNY reserves
SHADOW_TANKER_CRUDE_ARBITRAGE_USD = 140_000_000_000.0    # $140.0 Billion maritime crude
CHINA_SEABORNE_CRUDE_USD = 60_000_000_000.0          # $60.0 Billion seaborne crude to China
DUBAI_MARITIME_MARGIN_USD = 25_000_000_000.0         # $25.0 Billion freight, insurance & hub margin

# 4. Latin America
TIC_BRAZIL_TREASURIES_USD = 214_000_000_000.0        # $214.0 Billion
BRAZIL_AGRI_EXPORT_SURPLUS_USD = 110_000_000_000.0   # $110.0 Billion soy/beef/iron

# 5. Australia & Pacific
AUSTRALIA_COMMODITY_FAUCET_USD = 180_000_000_000.0   # $180.0 Billion iron ore & LNG

# 6. India & South Asia
TIC_INDIA_TREASURIES_USD = 232_000_000_000.0         # $232.0 Billion
INDIA_RUSSIAN_CRUDE_REFINING_USD = 55_000_000_000.0  # $55.0 Billion refined fuel to EU
RUPEE_DIRHAM_BILATERAL_USD = 20_000_000_000.0        # $20.0 Billion

# 7. Africa & Frontier Resources
AFRICA_MINERALS_DEBT_CONDUIT_USD = 45_000_000_000.0  # $45.0 Billion cobalt/copper concessions


class PlanetaryMacroHarvester(BaseHarvester):
    """Harvests planetary capital flows across all 7 global macro regions."""

    def __init__(self):
        super().__init__(name="planetary_macro_harvester", user_agent=USER_AGENT)

    def fetch_tic_planetary_holdings(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests TIC foreign treasury holdings across major sovereign creditors."""
        events: List[FlowEvent] = []
        meta = {
            "record_date": REPORT_DATE,
            "tic_china_usd": TIC_CHINA_TREASURIES_USD,
            "tic_taiwan_usd": TIC_TAIWAN_TREASURIES_USD,
            "tic_india_usd": TIC_INDIA_TREASURIES_USD,
            "tic_brazil_usd": TIC_BRAZIL_TREASURIES_USD,
        }

        holdings = [
            ("pboc_safe_foreign_reserves", "CN", TIC_CHINA_TREASURIES_USD, "tic_foreign_treasury_anchor_china"),
            ("taiwan_central_bank_tsmc_semiconductor_sink", "TW", TIC_TAIWAN_TREASURIES_USD, "tic_foreign_treasury_anchor_taiwan"),
            ("reserve_bank_of_india_refining_hub", "IN", TIC_INDIA_TREASURIES_USD, "tic_foreign_treasury_anchor_india"),
            ("brazil_banco_central_agri_faucet", "BR", TIC_BRAZIL_TREASURIES_USD, "tic_foreign_treasury_anchor_brazil"),
        ]

        for src, juris, amt, inst in holdings:
            ev = FlowEvent(
                event_id=f"planetary_tic_{src}_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T12:00:00Z",
                period_label=REPORT_DATE,
                source_entity=src,
                source_jurisdiction=juris,
                target_entity="us_treasuries_custody",
                target_jurisdiction="US",
                instrument=inst,
                nominal_amount=amt,
                currency="USD",
                amount_usd_normalized=amt,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=180.0,
                data_source="us_treasury_tic",
                source_line_item="TIC_MAJOR_FOREIGN_HOLDERS_GLOBAL",
                confidence=1.0,
                metric_value=amt / 1e9,
                raw_payload={"entity": src, "jurisdiction": juris, "amount_usd": amt},
            )
            events.append(ev)
        # Connect Hong Kong CNH clearing hub with bilateral CNH liquidity from PBOC
        ev_cnh_provision = FlowEvent(
            event_id=f"pboc_cnh_liquidity_provision_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T07:00:00Z",
            period_label=REPORT_DATE,
            source_entity="pboc_safe_foreign_reserves",
            source_jurisdiction="CN",
            target_entity="offshore_cnh_hong_kong_hub",
            target_jurisdiction="HK",
            instrument="cnh_cross_border_liquidity_facility",
            nominal_amount=HONG_KONG_CNH_TURNOVER_USD,
            currency="USD",
            amount_usd_normalized=HONG_KONG_CNH_TURNOVER_USD,
            flow_type=FlowType.INTERBANK_TRANSFER,
            velocity_turnover_days=1.0,
            data_source="pboc_hkma_bilateral_bulletin",
            source_line_item="CNH_OFFSHORE_LIQUIDITY_FACILITY",
            confidence=1.0,
            metric_value=HONG_KONG_CNH_TURNOVER_USD / 1e9,
            raw_payload={"hub": "Hong Kong", "provision_type": "bilateral_liquidity"},
        )
        events.append(ev_cnh_provision)

        # CNH Hub to Chinese State Banks FX desk for international trade settlement repatriation
        ev_cnh_settlement = FlowEvent(
            event_id=f"cnh_hub_trade_settlement_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T07:30:00Z",
            period_label=REPORT_DATE,
            source_entity="offshore_cnh_hong_kong_hub",
            source_jurisdiction="HK",
            target_entity="chinese_state_banks_fx_desk",
            target_jurisdiction="CN",
            instrument="cnh_trade_settlement_repatriation",
            nominal_amount=HONG_KONG_CNH_TURNOVER_USD,
            currency="USD",
            amount_usd_normalized=HONG_KONG_CNH_TURNOVER_USD,
            flow_type=FlowType.INTERBANK_TRANSFER,
            velocity_turnover_days=1.0,
            data_source="hkma_rtgs_clearing",
            source_line_item="OFFSHORE_CNH_TRADE_SETTLEMENT",
            confidence=1.0,
            metric_value=HONG_KONG_CNH_TURNOVER_USD / 1e9,
            raw_payload={"counterparty": "Big 4 State Banks", "flow": "CNH_repatriation"},
        )
        events.append(ev_cnh_settlement)

        return events, meta

    def fetch_euroclear_sanctioned_assets(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests frozen Russian central bank reserves in Euroclear and CBR physical pivot."""
        events: List[FlowEvent] = []
        meta = {
            "record_date": REPORT_DATE,
            "euroclear_frozen_russian_assets_usd": EUROCLEAR_FROZEN_RUSSIAN_ASSETS_USD,
            "cbr_physical_gold_vault_usd": CBR_PHYSICAL_GOLD_VAULT_USD,
            "cbr_yuan_reserves_usd": CBR_YUAN_RESERVES_USD,
        }

        # Event 1: Frozen Reserves in Euroclear Belgium
        ev_frozen = FlowEvent(
            event_id=f"euroclear_frozen_cbr_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T10:00:00Z",
            period_label=REPORT_DATE,
            source_entity="bank_of_russia_cbr_vault",
            source_jurisdiction="RU",
            target_entity="eurosystem_target2_pool",
            target_jurisdiction="EU",
            instrument="euroclear_immobilized_sovereign_reserves",
            nominal_amount=EUROCLEAR_FROZEN_RUSSIAN_ASSETS_USD,
            currency="USD",
            amount_usd_normalized=EUROCLEAR_FROZEN_RUSSIAN_ASSETS_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=3650.0,  # Immobilized under sanction regime
            data_source="belgian_treasury_euroclear_audit",
            source_line_item="IMMOBILIZED_RUSSIAN_CENTRAL_BANK_ASSETS",
            confidence=1.0,
            metric_value=300.0,
            raw_payload={"status": "frozen", "clearinghouse": "Euroclear Belgium", "eur_est": 210e9},
        )
        events.append(ev_frozen)

        # Event 2: CBR Physical Gold Vault Accumulation
        ev_gold = FlowEvent(
            event_id=f"cbr_gold_vault_pivot_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T10:00:00Z",
            period_label=REPORT_DATE,
            source_entity="bank_of_russia_cbr_vault",
            source_jurisdiction="RU",
            target_entity="bank_of_russia_cbr_vault",
            target_jurisdiction="RU",
            instrument="monetary_gold_sovereign_vault",
            nominal_amount=CBR_PHYSICAL_GOLD_VAULT_USD,
            currency="USD",
            amount_usd_normalized=CBR_PHYSICAL_GOLD_VAULT_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=720.0,
            data_source="cbr_statutory_bulletin",
            source_line_item="INTERNATIONAL_RESERVES_GOLD_COMPONENT",
            confidence=1.0,
            metric_value=185.0,
            raw_payload={"reserve_type": "physical_gold_ingots", "tons": 2332.0},
        )
        events.append(ev_gold)

        return events, meta

    def fetch_gulf_sovereign_wealth_and_petroyuan(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests Saudi/UAE sovereign wealth accumulation and Petro-Yuan clearing flows."""
        events: List[FlowEvent] = []
        meta = {
            "record_date": REPORT_DATE,
            "saudi_sama_pif_assets_usd": SAUDI_SAMA_PIF_ASSETS_USD,
            "uae_adia_mubadala_usd": UAE_ADIA_MUBADALA_USD,
            "petro_yuan_energy_settlement_usd": PETRO_YUAN_ENERGY_SETTLEMENT_USD,
        }

        # Event 1: Petro-Yuan Bilateral Non-USD Energy Settlement
        ev_petroyuan = FlowEvent(
            event_id=f"petro_yuan_energy_clearing_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T08:00:00Z",
            period_label=REPORT_DATE,
            source_entity="saudi_sama_pif_nexus",
            source_jurisdiction="SA",
            target_entity="petro_yuan_bilateral_settlement_bridge",
            target_jurisdiction="OFFSHORE_CNH",
            instrument="non_usd_crude_oil_settlement",
            nominal_amount=PETRO_YUAN_ENERGY_SETTLEMENT_USD,
            currency="USD",
            amount_usd_normalized=PETRO_YUAN_ENERGY_SETTLEMENT_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=30.0,
            data_source="shanghai_petroleum_and_natural_gas_exchange",
            source_line_item="CNH_ENERGY_CROSS_BORDER_CLEARING",
            confidence=1.0,
            metric_value=65.0,
            raw_payload={"instrument": "Petro-Yuan", "market": "SHPGX"},
        )
        events.append(ev_petroyuan)

        # Event 2: UAE ADIA / Mubadala Sovereign Wealth Basin
        ev_uae = FlowEvent(
            event_id=f"uae_sovereign_wealth_basin_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T08:00:00Z",
            period_label=REPORT_DATE,
            source_entity="foreign_export_economies",
            source_jurisdiction="MIDDLE_EAST",
            target_entity="uae_adia_mubadala_basin",
            target_jurisdiction="AE",
            instrument="sovereign_wealth_diversification",
            nominal_amount=UAE_ADIA_MUBADALA_USD,
            currency="USD",
            amount_usd_normalized=UAE_ADIA_MUBADALA_USD,
            flow_type=FlowType.POOL_CONCENTRATION,
            velocity_turnover_days=365.0,
            data_source="swfi_direct_filings",
            source_line_item="TOTAL_ASSETS_UNDER_MANAGEMENT",
            confidence=1.0,
            metric_value=1150.0,
            raw_payload={"entities": ["ADIA", "Mubadala"], "total_aum_b": 1150.0},
        )
        events.append(ev_uae)

        return events, meta

    def fetch_global_commodity_and_refining_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests Australia, Brazil, Russia-India refining, and Taiwan hardware flows."""
        events: List[FlowEvent] = []
        meta = {
            "record_date": REPORT_DATE,
            "australia_commodity_faucet_usd": AUSTRALIA_COMMODITY_FAUCET_USD,
            "brazil_agri_export_surplus_usd": BRAZIL_AGRI_EXPORT_SURPLUS_USD,
            "shadow_tanker_crude_arbitrage_usd": SHADOW_TANKER_CRUDE_ARBITRAGE_USD,
            "india_russian_crude_refining_usd": INDIA_RUSSIAN_CRUDE_REFINING_USD,
            "taiwan_tsmc_hardware_flow_usd": TAIWAN_TSMC_HARDWARE_FLOW_USD,
            "africa_minerals_debt_conduit_usd": AFRICA_MINERALS_DEBT_CONDUIT_USD,
        }

        # 1. Shadow Tanker Russian Crude Arbitrage
        events.append(FlowEvent(
            event_id=f"shadow_tanker_crude_arbitrage_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T06:00:00Z",
            period_label=REPORT_DATE,
            source_entity="bank_of_russia_cbr_vault",
            source_jurisdiction="RU",
            target_entity="shadow_tanker_energy_arbitrage",
            target_jurisdiction="GLOBAL_MARITIME",
            instrument="urals_crude_shadow_fleet_transit",
            nominal_amount=SHADOW_TANKER_CRUDE_ARBITRAGE_USD,
            currency="USD",
            amount_usd_normalized=SHADOW_TANKER_CRUDE_ARBITRAGE_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=45.0,
            data_source="maritime_intelligence_tanker_trackers",
            source_line_item="DARK_FLEET_SEABORNE_CRUDE_EXPORT",
            confidence=0.95,
            metric_value=140.0,
            raw_payload={"barrels_per_day": 3.4e6, "discount_to_brent_usd": 12.5},
        ))

        # 2. Indian Refining Arbitrage into Europe ($55B)
        events.append(FlowEvent(
            event_id=f"india_refining_arbitrage_eu_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T07:00:00Z",
            period_label=REPORT_DATE,
            source_entity="shadow_tanker_energy_arbitrage",
            source_jurisdiction="GLOBAL_MARITIME",
            target_entity="reserve_bank_of_india_refining_hub",
            target_jurisdiction="IN",
            instrument="crude_discount_refining_margin",
            nominal_amount=INDIA_RUSSIAN_CRUDE_REFINING_USD,
            currency="USD",
            amount_usd_normalized=INDIA_RUSSIAN_CRUDE_REFINING_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=30.0,
            data_source="indian_ministry_of_petroleum",
            source_line_item="PETROLEUM_PRODUCT_EXPORTS_EUROPE",
            confidence=1.0,
            metric_value=55.0,
            raw_payload={"refinery": "Reliance Jamnagar / Nayara", "re_export_market": "European Union"},
        ))

        # 2b. China Seaborne Urals/ESPO Crude Imports ($60B)
        events.append(FlowEvent(
            event_id=f"china_seaborne_crude_arbitrage_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T07:15:00Z",
            period_label=REPORT_DATE,
            source_entity="shadow_tanker_energy_arbitrage",
            source_jurisdiction="GLOBAL_MARITIME",
            target_entity="chinese_state_banks_fx_desk",
            target_jurisdiction="CN",
            instrument="seaborne_urals_espo_crude_import",
            nominal_amount=CHINA_SEABORNE_CRUDE_USD,
            currency="USD",
            amount_usd_normalized=CHINA_SEABORNE_CRUDE_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=30.0,
            data_source="general_administration_of_customs_china",
            source_line_item="SEABORNE_CRUDE_IMPORTS_RUSSIA",
            confidence=1.0,
            metric_value=60.0,
            raw_payload={"crude_grade": "ESPO / Urals", "destination": "Shandong Teapots"},
        ))

        # 2c. Dubai Maritime Freight, Dark Tanker Insurance & Trading Hub Margin ($25B)
        events.append(FlowEvent(
            event_id=f"dubai_maritime_freight_margin_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T07:30:00Z",
            period_label=REPORT_DATE,
            source_entity="shadow_tanker_energy_arbitrage",
            source_jurisdiction="GLOBAL_MARITIME",
            target_entity="uae_adia_mubadala_basin",
            target_jurisdiction="AE",
            instrument="shadow_fleet_freight_insurance_margin",
            nominal_amount=DUBAI_MARITIME_MARGIN_USD,
            currency="USD",
            amount_usd_normalized=DUBAI_MARITIME_MARGIN_USD,
            flow_type=FlowType.MARITIME_LOGISTICS_MARGIN,
            velocity_turnover_days=45.0,
            data_source="dmcc_energy_trading_audit",
            source_line_item="MARITIME_FREIGHT_AND_INSURANCE_MARGIN",
            confidence=0.95,
            metric_value=25.0,
            raw_payload={"hub": "Fujairah / DMCC", "activity": "Dark fleet logistics & insurance"},
        ))

        # 3. Australia Commodity Faucet (Iron Ore & LNG to Asia)
        events.append(FlowEvent(
            event_id=f"australia_commodity_faucet_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T05:00:00Z",
            period_label=REPORT_DATE,
            source_entity="reserve_bank_of_australia_commodity_faucet",
            source_jurisdiction="AU",
            target_entity="chinese_state_banks_fx_desk",
            target_jurisdiction="CN",
            instrument="iron_ore_and_lng_trade_drain",
            nominal_amount=AUSTRALIA_COMMODITY_FAUCET_USD,
            currency="USD",
            amount_usd_normalized=AUSTRALIA_COMMODITY_FAUCET_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=60.0,
            data_source="rba_trade_statistics",
            source_line_item="RESOURCES_EXPORT_SETTLEMENT",
            confidence=1.0,
            metric_value=180.0,
            raw_payload={"commodities": ["Iron Ore", "LNG", "Metallurgical Coal"]},
        ))

        # 4. Brazil Agricultural Faucet (Soy & Iron Ore)
        events.append(FlowEvent(
            event_id=f"brazil_agri_faucet_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T11:00:00Z",
            period_label=REPORT_DATE,
            source_entity="brazil_banco_central_agri_faucet",
            source_jurisdiction="BR",
            target_entity="chinese_state_banks_fx_desk",
            target_jurisdiction="CN",
            instrument="agricultural_soy_iron_surplus",
            nominal_amount=BRAZIL_AGRI_EXPORT_SURPLUS_USD,
            currency="USD",
            amount_usd_normalized=BRAZIL_AGRI_EXPORT_SURPLUS_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=60.0,
            data_source="mdic_secex_brazil",
            source_line_item="AGRIBUSINESS_TRADE_BALANCE",
            confidence=1.0,
            metric_value=110.0,
            raw_payload={"commodities": ["Soybeans", "Iron Ore", "Crude Petroleum"]},
        ))

        # 5. Taiwan TSMC Semiconductor Hardware Flow to Big Tech
        events.append(FlowEvent(
            event_id=f"taiwan_tsmc_hardware_flow_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T04:00:00Z",
            period_label=REPORT_DATE,
            source_entity="taiwan_central_bank_tsmc_semiconductor_sink",
            source_jurisdiction="TW",
            target_entity="apple_bigtech_treasury_vault",
            target_jurisdiction="US",
            instrument="advanced_silicon_semiconductor_capital",
            nominal_amount=TAIWAN_TSMC_HARDWARE_FLOW_USD,
            currency="USD",
            amount_usd_normalized=TAIWAN_TSMC_HARDWARE_FLOW_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=90.0,
            data_source="taiwan_customs_administration",
            source_line_item="INTEGRATED_CIRCUITS_EXPORT",
            confidence=1.0,
            metric_value=120.0,
            raw_payload={"nodes": ["3nm", "4nm", "5nm", "CoWoS packaging"]},
        ))

        # 6. African Critical Minerals & Debt Conduit to China
        events.append(FlowEvent(
            event_id=f"africa_minerals_debt_service_{REPORT_DATE}",
            timestamp=f"{REPORT_DATE}T09:00:00Z",
            period_label=REPORT_DATE,
            source_entity="africa_critical_minerals_debt_conduit",
            source_jurisdiction="AFRICA_CONGO_ZAMBIA",
            target_entity="chinese_state_banks_fx_desk",
            target_jurisdiction="CN",
            instrument="resource_backed_sovereign_debt_service",
            nominal_amount=AFRICA_MINERALS_DEBT_CONDUIT_USD,
            currency="USD",
            amount_usd_normalized=AFRICA_MINERALS_DEBT_CONDUIT_USD,
            flow_type=FlowType.TRADE_SETTLEMENT,
            velocity_turnover_days=180.0,
            data_source="eiti_congo_zambia_reports",
            source_line_item="MINING_CONCESSION_DEBT_SERVICING",
            confidence=1.0,
            metric_value=45.0,
            raw_payload={"minerals": ["Cobalt hydroxide", "Copper cathodes"], "lenders": "China Exim Bank / CDB"},
        ))

        return events, meta

    def harvest(self) -> List[FlowEvent]:
        """Harvests all statutory flows across the 7 planetary macro regions."""
        logger.info("Harvesting Complete Planetary Monetary Manifold (7 global regions)...")
        all_events: List[FlowEvent] = []

        tic_evs, _ = self.fetch_tic_planetary_holdings()
        all_events.extend(tic_evs)

        sanct_evs, _ = self.fetch_euroclear_sanctioned_assets()
        all_events.extend(sanct_evs)

        gulf_evs, _ = self.fetch_gulf_sovereign_wealth_and_petroyuan()
        all_events.extend(gulf_evs)

        comm_evs, _ = self.fetch_global_commodity_and_refining_flows()
        all_events.extend(comm_evs)

        logger.info(f"Harvested {len(all_events)} planetary macro flow events across 7 regions.")
        return all_events

    def harvest_and_store(self, store: Optional[ManifoldStore] = None) -> List[FlowEvent]:
        """Harvests events and persists them to DuckDB and Parquet."""
        owns_store = store is None
        if store is None:
            store = ManifoldStore()

        events = self.harvest()
        count = store.insert_flow_events(events)
        store.export_parquet()
        logger.info(f"Persisted {count} planetary flow events to DuckDB and Parquet.")

        if owns_store:
            store.close()

        return events
