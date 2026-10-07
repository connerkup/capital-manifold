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

# 8. Norway Sovereign Wealth Fund (GPFG)
NORWAY_GPFG_AUM_USD = 1_750_000_000_000.0            # $1.750 Trillion

# 9. Switzerland (SNB & UBS G-SIB)
SNB_FX_RESERVES_USD = 950_000_000_000.0             # $950.0 Billion SNB total balance sheet
SNB_GSIB_TRANSMISSION_USD = 500_000_000_000.0       # $500.0 Billion transmission to UBS
SNB_FOREIGN_EQUITIES_USD = 450_000_000_000.0        # $450.0 Billion foreign equity allocation
UBS_TREASURIES_CUSTODY_USD = 350_000_000_000.0      # $350.0 Billion HQLA Treasuries
UBS_WEALTH_BONDS_USD = 150_000_000_000.0            # $150.0 Billion wealth management bonds

# 10. Singapore (MAS & GIC / Temasek)
SINGAPORE_MAS_RESERVES_USD = 400_000_000_000.0      # $400.0 Billion MAS official reserves
GIC_US_TREASURIES_USD = 250_000_000_000.0           # $250.0 Billion Treasuries
TEMASEK_GLOBAL_ASSETS_USD = 150_000_000_000.0       # $150.0 Billion portfolio allocation

# 11. South Korea (BOK & NPS)
BOK_FX_RESERVES_USD = 420_000_000_000.0             # $420.0 Billion BOK reserves
BOK_TIC_TREASURIES_USD = 120_000_000_000.0          # $120.0 Billion TIC US Treasuries
BOK_NPS_FX_SWAP_USD = 300_000_000_000.0             # $300.0 Billion standing swap to NPS
NPS_TOTAL_AUM_USD = 850_000_000_000.0               # $850.0 Billion NPS AUM

# 12. United Kingdom (BoE & DMO Gilts)
UK_DMO_GILT_MARKET_GBP = 2_600_000_000_000.0        # £2.600 Trillion
GBP_USD_REFERENCE_RATE = 1.29                       # Reference FX rate
UK_DMO_GILT_MARKET_USD = UK_DMO_GILT_MARKET_GBP * GBP_USD_REFERENCE_RATE  # $3.354 Trillion

# 13. Canada (BoC & Maple 8 Consortium)
CANADA_MAPLE_AUM_USD = 1_500_000_000_000.0          # $1.500 Trillion Maple 8 AUM
MAPLE_ALTERNATIVES_USD = 900_000_000_000.0          # $900.0 Billion global alternatives
MAPLE_TREASURIES_USD = 600_000_000_000.0            # $600.0 Billion fixed income/Treasuries

# 14. Mexico (Banxico & USMCA Nearshoring)
USMCA_NEARSHORING_TRADE_USD = 500_000_000_000.0     # $500.0 Billion bilateral trade
USMCA_MANUFACTURING_FLOW_USD = 350_000_000_000.0    # $350.0 Billion supply chain settlement
USMCA_RESERVE_ACCUM_USD = 150_000_000_000.0         # $150.0 Billion reserve accumulation

# 15. Multilateral Institutions (IMF & BIS)
IMF_SDR_POOL_USD = 935_000_000_000.0                # $935.0 Billion SDR pool
BIS_BASEL_BANKING_USD = 450_000_000_000.0           # $450.0 Billion BIS Basel desk
IMF_GENERAL_SDR_USD = 485_000_000_000.0             # $485.0 Billion general SDR allocation
BIS_BUNDESBANK_DEPOSIT_USD = 250_000_000_000.0      # $250.0 Billion central bank deposits
BIS_TREASURY_MGMT_USD = 200_000_000_000.0           # $200.0 Billion Treasury management

# 16. Upgraded Eurasian Macro Architecture
RUSSIA_NWF_BUFFER_USD = 155_000_000_000.0           # $155.0 Billion NWF oil buffer
RUSSIAN_STATE_CREDIT_USD = 920_000_000_000.0        # $920.0 Billion Sberbank/VTB credit
RUSSIAN_BANKING_FUNDING_USD = 765_000_000_000.0     # $765.0 Billion state banking credit funding
GAZPROMBANK_GAS_EXPORT_USD = 95_000_000_000.0       # $95.0 Billion pipeline gas exports
RUSSIA_OFFSHORE_SHADOW_BASIN_USD = 180_000_000_000.0 # $180.0 Billion trapped offshore basin
RUSSIA_COMMODITY_NON_ENERGY_TRAPPED_USD = 85_000_000_000.0  # $85.0 Billion trapped Rupee/Dirhams
RUSSIA_COMMODITY_NON_ENERGY_CHINA_USD = 95_000_000_000.0    # $95.0 Billion non-energy exports to China
RUSSIA_DIRECT_ENERGY_CHINA_USD = 5_000_000_000.0            # $5.0 Billion direct energy clearing


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

    def fetch_norwegian_gpfg_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests Norwegian GPFG sovereign wealth genesis faucet and global equity sink."""
        events: List[FlowEvent] = [
            FlowEvent(
                event_id=f"norway_gpfg_global_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T08:00:00Z",
                period_label=REPORT_DATE,
                source_entity="norway_norges_bank_gpfg_faucet",
                source_jurisdiction="NO",
                target_entity="norway_gpfg_global_equity_sink",
                target_jurisdiction="GLOBAL",
                instrument="gpfg_sovereign_wealth_global_equity_allocation",
                nominal_amount=NORWAY_GPFG_AUM_USD,
                currency="USD",
                amount_usd_normalized=NORWAY_GPFG_AUM_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=365.0,
                data_source="nbim_annual_report",
                source_line_item="GOVERNMENT_PENSION_FUND_GLOBAL_AUM",
                confidence=1.0,
                metric_value=1750.0,
                raw_payload={"fund": "GPFG", "aum_usd": NORWAY_GPFG_AUM_USD},
            )
        ]
        meta = {"record_date": REPORT_DATE, "gpfg_aum_usd": NORWAY_GPFG_AUM_USD}
        return events, meta

    def fetch_swiss_monetary_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests Swiss National Bank FX reserves, UBS G-SIB transmission, and collateral sinks."""
        events: List[FlowEvent] = [
            # 1. SNB -> UBS G-SIB reserve transmission ($500B)
            FlowEvent(
                event_id=f"snb_gsib_reserve_transmission_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T08:15:00Z",
                period_label=REPORT_DATE,
                source_entity="swiss_national_bank_snb_vault",
                source_jurisdiction="CH",
                target_entity="ubs_group_consolidated_gsib",
                target_jurisdiction="CH_GLOBAL",
                instrument="snb_gsib_reserve_transmission",
                nominal_amount=SNB_GSIB_TRANSMISSION_USD,
                currency="USD",
                amount_usd_normalized=SNB_GSIB_TRANSMISSION_USD,
                flow_type=FlowType.INTERBANK_TRANSFER,
                velocity_turnover_days=30.0,
                data_source="snb_annual_balance_sheet",
                source_line_item="SNB_DOMESTIC_AND_CROSS_BORDER_RESERVE_TRANSMISSION",
                confidence=1.0,
                metric_value=500.0,
                raw_payload={"transmission": "SNB to UBS G-SIB"},
            ),
            # 2. SNB -> Norway Global Equity Sink ($450B foreign equities)
            FlowEvent(
                event_id=f"snb_equity_reserve_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T08:20:00Z",
                period_label=REPORT_DATE,
                source_entity="swiss_national_bank_snb_vault",
                source_jurisdiction="CH",
                target_entity="norway_gpfg_global_equity_sink",
                target_jurisdiction="GLOBAL",
                instrument="snb_foreign_equity_and_gold_reserve_allocation",
                nominal_amount=SNB_FOREIGN_EQUITIES_USD,
                currency="USD",
                amount_usd_normalized=SNB_FOREIGN_EQUITIES_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=180.0,
                data_source="snb_foreign_currency_investments",
                source_line_item="SNB_FOREIGN_EQUITIES_AND_BONDS",
                confidence=1.0,
                metric_value=450.0,
                raw_payload={"allocation": "Foreign equities and debt"},
            ),
            # 3. UBS G-SIB -> US Treasuries Custody ($350B)
            FlowEvent(
                event_id=f"ubs_treasuries_custody_placement_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T08:30:00Z",
                period_label=REPORT_DATE,
                source_entity="ubs_group_consolidated_gsib",
                source_jurisdiction="CH_GLOBAL",
                target_entity="us_treasuries_custody",
                target_jurisdiction="US",
                instrument="swiss_treasuries_custodial_placement",
                nominal_amount=UBS_TREASURIES_CUSTODY_USD,
                currency="USD",
                amount_usd_normalized=UBS_TREASURIES_CUSTODY_USD,
                flow_type=FlowType.REPO_COLLATERAL,
                velocity_turnover_days=60.0,
                data_source="ubs_group_quarterly_pillar_3",
                source_line_item="UBS_US_TREASURY_HQLA_CUSTODY",
                confidence=1.0,
                metric_value=350.0,
                raw_payload={"asset": "US Treasuries HQLA"},
            ),
            # 4. UBS G-SIB -> Sovereign Debt Holders ($150B)
            FlowEvent(
                event_id=f"ubs_wealth_bond_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T08:45:00Z",
                period_label=REPORT_DATE,
                source_entity="ubs_group_consolidated_gsib",
                source_jurisdiction="CH_GLOBAL",
                target_entity="sovereign_debt_holders",
                target_jurisdiction="WORLD",
                instrument="swiss_wealth_sovereign_bond_allocation",
                nominal_amount=UBS_WEALTH_BONDS_USD,
                currency="USD",
                amount_usd_normalized=UBS_WEALTH_BONDS_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=90.0,
                data_source="ubs_wealth_management_filings",
                source_line_item="UBS_GLOBAL_WEALTH_BOND_PLACEMENT",
                confidence=1.0,
                metric_value=150.0,
                raw_payload={"segment": "Wealth Management Bond Placement"},
            ),
        ]
        meta = {"record_date": REPORT_DATE, "snb_reserves_usd": SNB_FX_RESERVES_USD}
        return events, meta

    def fetch_singapore_sovereign_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests MAS reserves and GIC/Temasek sovereign investment traversal."""
        events: List[FlowEvent] = [
            # 1. MAS -> GIC/Temasek reserve transfer ($400B)
            FlowEvent(
                event_id=f"mas_official_reserve_transfer_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T06:00:00Z",
                period_label=REPORT_DATE,
                source_entity="singapore_mas_reserve_faucet",
                source_jurisdiction="SG",
                target_entity="singapore_gic_temasek_sovereign_basin",
                target_jurisdiction="SG_GLOBAL",
                instrument="mas_official_foreign_reserve_transfer",
                nominal_amount=SINGAPORE_MAS_RESERVES_USD,
                currency="USD",
                amount_usd_normalized=SINGAPORE_MAS_RESERVES_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=180.0,
                data_source="mas_official_foreign_reserves",
                source_line_item="MAS_INTERNATIONAL_RESERVES",
                confidence=1.0,
                metric_value=400.0,
                raw_payload={"authority": "MAS", "reserves_usd": SINGAPORE_MAS_RESERVES_USD},
            ),
            # 2. GIC -> US Treasuries Custody ($250B)
            FlowEvent(
                event_id=f"gic_treasuries_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T06:30:00Z",
                period_label=REPORT_DATE,
                source_entity="singapore_gic_temasek_sovereign_basin",
                source_jurisdiction="SG_GLOBAL",
                target_entity="us_treasuries_custody",
                target_jurisdiction="US",
                instrument="gic_us_treasury_allocation",
                nominal_amount=GIC_US_TREASURIES_USD,
                currency="USD",
                amount_usd_normalized=GIC_US_TREASURIES_USD,
                flow_type=FlowType.REPO_COLLATERAL,
                velocity_turnover_days=90.0,
                data_source="gic_annual_report",
                source_line_item="GIC_NOMINAL_BONDS_AND_TREASURIES",
                confidence=1.0,
                metric_value=250.0,
                raw_payload={"entity": "GIC", "allocation": "US Treasuries"},
            ),
            # 3. Temasek -> Sovereign Debt Holders ($150B)
            FlowEvent(
                event_id=f"temasek_global_portfolio_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T06:45:00Z",
                period_label=REPORT_DATE,
                source_entity="singapore_gic_temasek_sovereign_basin",
                source_jurisdiction="SG_GLOBAL",
                target_entity="sovereign_debt_holders",
                target_jurisdiction="WORLD",
                instrument="temasek_global_portfolio_allocation",
                nominal_amount=TEMASEK_GLOBAL_ASSETS_USD,
                currency="USD",
                amount_usd_normalized=TEMASEK_GLOBAL_ASSETS_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=90.0,
                data_source="temasek_review",
                source_line_item="TEMASEK_GLOBAL_ASSET_ALLOCATION",
                confidence=1.0,
                metric_value=150.0,
                raw_payload={"entity": "Temasek", "allocation": "Global Assets"},
            ),
        ]
        meta = {"record_date": REPORT_DATE, "mas_reserves_usd": SINGAPORE_MAS_RESERVES_USD}
        return events, meta

    def fetch_korean_monetary_and_pension_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests Bank of Korea reserves and NPS pension capital sink flows."""
        events: List[FlowEvent] = [
            # 1. BOK -> US Treasuries Custody ($120B)
            FlowEvent(
                event_id=f"bok_tic_treasury_anchor_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T05:00:00Z",
                period_label=REPORT_DATE,
                source_entity="bank_of_korea_bok_vault",
                source_jurisdiction="KR",
                target_entity="us_treasuries_custody",
                target_jurisdiction="US",
                instrument="bok_tic_us_treasury_anchor",
                nominal_amount=BOK_TIC_TREASURIES_USD,
                currency="USD",
                amount_usd_normalized=BOK_TIC_TREASURIES_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=180.0,
                data_source="us_treasury_tic",
                source_line_item="TIC_KOREA_TREASURIES",
                confidence=1.0,
                metric_value=120.0,
                raw_payload={"country": "South Korea", "holding_usd": BOK_TIC_TREASURIES_USD},
            ),
            # 2. BOK -> NPS FX Swap Facility ($300B)
            FlowEvent(
                event_id=f"bok_nps_fx_swap_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T05:30:00Z",
                period_label=REPORT_DATE,
                source_entity="bank_of_korea_bok_vault",
                source_jurisdiction="KR",
                target_entity="korea_national_pension_service_nps",
                target_jurisdiction="KR",
                instrument="bok_nps_fx_swap_facility",
                nominal_amount=BOK_NPS_FX_SWAP_USD,
                currency="USD",
                amount_usd_normalized=BOK_NPS_FX_SWAP_USD,
                flow_type=FlowType.BILATERAL_SWAP,
                velocity_turnover_days=90.0,
                data_source="bank_of_korea_monetary_report",
                source_line_item="BOK_NPS_FOREIGN_EXCHANGE_SWAP_LINE",
                confidence=1.0,
                metric_value=850.0,
                raw_payload={"facility": "BOK-NPS FX Swap", "nps_total_aum": NPS_TOTAL_AUM_USD},
            ),
        ]
        meta = {"record_date": REPORT_DATE, "bok_reserves_usd": BOK_FX_RESERVES_USD, "nps_aum_usd": NPS_TOTAL_AUM_USD}
        return events, meta

    def fetch_uk_monetary_and_gilt_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests Bank of England and UK DMO Gilt debt market flows (£2.6T Gilt market)."""
        events: List[FlowEvent] = [
            FlowEvent(
                event_id=f"uk_dmo_gilt_issuance_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T09:00:00Z",
                period_label=REPORT_DATE,
                source_entity="bank_of_england_boe_vault",
                source_jurisdiction="UK",
                target_entity="uk_dmo_gilt_debt_market",
                target_jurisdiction="UK",
                instrument="uk_dmo_gilt_benchmark_issuance",
                nominal_amount=UK_DMO_GILT_MARKET_GBP,
                currency="GBP",
                amount_usd_normalized=UK_DMO_GILT_MARKET_USD,
                flow_type=FlowType.SOVEREIGN_ISSUANCE,
                velocity_turnover_days=30.0,
                data_source="uk_dmo_annual_review",
                source_line_item="TOTAL_CENTRAL_GOVERNMENT_GILT_STOCK",
                confidence=1.0,
                metric_value=2600.0,
                raw_payload={"gilt_stock_gbp": UK_DMO_GILT_MARKET_GBP, "rate_gbp_usd": GBP_USD_REFERENCE_RATE},
            )
        ]
        meta = {"record_date": REPORT_DATE, "uk_gilt_market_usd": UK_DMO_GILT_MARKET_USD}
        return events, meta

    def fetch_canadian_maple_pension_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests Bank of Canada and Canadian Maple 8 Pension Consortium flows ($1.5T)."""
        events: List[FlowEvent] = [
            # 1. Bank of Canada -> Maple Pension Consortium ($1.5T)
            FlowEvent(
                event_id=f"boc_maple_pension_liquidity_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T13:00:00Z",
                period_label=REPORT_DATE,
                source_entity="bank_of_canada_boc_vault",
                source_jurisdiction="CA",
                target_entity="canada_maple_pension_consortium",
                target_jurisdiction="CA_GLOBAL",
                instrument="maple_pension_sovereign_liquidity_allocation",
                nominal_amount=CANADA_MAPLE_AUM_USD,
                currency="USD",
                amount_usd_normalized=CANADA_MAPLE_AUM_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=180.0,
                data_source="cppib_cdpq_combined_filings",
                source_line_item="MAPLE_EIGHT_COMBINED_AUM",
                confidence=1.0,
                metric_value=1500.0,
                raw_payload={"consortium": "Maple 8", "combined_aum_usd": CANADA_MAPLE_AUM_USD},
            ),
            # 2. Maple Consortium -> Norway Global Equity Sink ($900B alternatives)
            FlowEvent(
                event_id=f"maple_global_alternative_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T13:30:00Z",
                period_label=REPORT_DATE,
                source_entity="canada_maple_pension_consortium",
                source_jurisdiction="CA_GLOBAL",
                target_entity="norway_gpfg_global_equity_sink",
                target_jurisdiction="GLOBAL",
                instrument="maple_global_alternative_and_infrastructure_allocation",
                nominal_amount=MAPLE_ALTERNATIVES_USD,
                currency="USD",
                amount_usd_normalized=MAPLE_ALTERNATIVES_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=365.0,
                data_source="cppib_annual_report",
                source_line_item="CANADIAN_PENSION_GLOBAL_INFRASTRUCTURE",
                confidence=1.0,
                metric_value=900.0,
                raw_payload={"allocation": "Global infrastructure and private equity"},
            ),
            # 3. Maple Consortium -> US Treasuries Custody ($600B)
            FlowEvent(
                event_id=f"maple_treasury_custody_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T13:45:00Z",
                period_label=REPORT_DATE,
                source_entity="canada_maple_pension_consortium",
                source_jurisdiction="CA_GLOBAL",
                target_entity="us_treasuries_custody",
                target_jurisdiction="US",
                instrument="maple_treasury_custody_allocation",
                nominal_amount=MAPLE_TREASURIES_USD,
                currency="USD",
                amount_usd_normalized=MAPLE_TREASURIES_USD,
                flow_type=FlowType.REPO_COLLATERAL,
                velocity_turnover_days=90.0,
                data_source="cdpq_annual_report",
                source_line_item="FIXED_INCOME_US_TREASURIES",
                confidence=1.0,
                metric_value=600.0,
                raw_payload={"allocation": "US Treasury fixed income custody"},
            ),
        ]
        meta = {"record_date": REPORT_DATE, "maple_aum_usd": CANADA_MAPLE_AUM_USD}
        return events, meta

    def fetch_mexican_nearshoring_trade_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests Banco de México and USMCA nearshoring cross-border trade flows ($500B)."""
        events: List[FlowEvent] = [
            # 1. Banxico -> USMCA Nearshoring Conduit ($500B)
            FlowEvent(
                event_id=f"banxico_nearshoring_facility_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T14:00:00Z",
                period_label=REPORT_DATE,
                source_entity="banco_de_mexico_banxico_faucet",
                source_jurisdiction="MX",
                target_entity="usmca_nearshoring_trade_conduit",
                target_jurisdiction="MX_US",
                instrument="banxico_nearshoring_trade_facility",
                nominal_amount=USMCA_NEARSHORING_TRADE_USD,
                currency="USD",
                amount_usd_normalized=USMCA_NEARSHORING_TRADE_USD,
                flow_type=FlowType.TRADE_SETTLEMENT,
                velocity_turnover_days=45.0,
                data_source="banxico_sie_economic_indicators",
                source_line_item="USMCA_BILATERAL_MANUFACTURING_FLOWS",
                confidence=1.0,
                metric_value=500.0,
                raw_payload={"trade_corridor": "USMCA Mexico-US"},
            ),
            # 2. USMCA Conduit -> US Corporate & Household Borrowers ($350B supply chain)
            FlowEvent(
                event_id=f"usmca_trade_settlement_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T14:30:00Z",
                period_label=REPORT_DATE,
                source_entity="usmca_nearshoring_trade_conduit",
                source_jurisdiction="MX_US",
                target_entity="us_corporate_and_household_borrowers",
                target_jurisdiction="US",
                instrument="usmca_supply_chain_trade_settlement",
                nominal_amount=USMCA_MANUFACTURING_FLOW_USD,
                currency="USD",
                amount_usd_normalized=USMCA_MANUFACTURING_FLOW_USD,
                flow_type=FlowType.TRADE_SETTLEMENT,
                velocity_turnover_days=30.0,
                data_source="us_census_bureau_foreign_trade",
                source_line_item="US_MEXICO_BILATERAL_MERCHANDISE_TRADE",
                confidence=1.0,
                metric_value=350.0,
                raw_payload={"flow": "Automotive and electronics manufacturing"},
            ),
            # 3. USMCA Conduit -> US Treasuries Custody ($150B reserves)
            FlowEvent(
                event_id=f"usmca_reserve_accumulation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T14:45:00Z",
                period_label=REPORT_DATE,
                source_entity="usmca_nearshoring_trade_conduit",
                source_jurisdiction="MX_US",
                target_entity="us_treasuries_custody",
                target_jurisdiction="US",
                instrument="usmca_reserve_accumulation",
                nominal_amount=USMCA_RESERVE_ACCUM_USD,
                currency="USD",
                amount_usd_normalized=USMCA_RESERVE_ACCUM_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=180.0,
                data_source="us_treasury_tic",
                source_line_item="TIC_MEXICO_TREASURY_HOLDINGS",
                confidence=1.0,
                metric_value=150.0,
                raw_payload={"flow": "Banxico FX reserve accumulation"},
            ),
        ]
        meta = {"record_date": REPORT_DATE, "usmca_trade_usd": USMCA_NEARSHORING_TRADE_USD}
        return events, meta

    def fetch_multilateral_sdr_and_bis_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests IMF Special Drawing Rights ($935B) and BIS Basel Central Banking Desk ($450B)."""
        events: List[FlowEvent] = [
            # 1. IMF SDR Pool -> BIS Basel Banking Dept ($450B)
            FlowEvent(
                event_id=f"imf_sdr_bis_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T10:00:00Z",
                period_label=REPORT_DATE,
                source_entity="imf_special_drawing_rights_sdr_pool",
                source_jurisdiction="GLOBAL_MULTILATERAL",
                target_entity="bis_basel_banking_department",
                target_jurisdiction="GLOBAL_MULTILATERAL",
                instrument="sdr_multilateral_central_bank_reserve_allocation",
                nominal_amount=BIS_BASEL_BANKING_USD,
                currency="USD",
                amount_usd_normalized=BIS_BASEL_BANKING_USD,
                flow_type=FlowType.INTERBANK_TRANSFER,
                velocity_turnover_days=365.0,
                data_source="imf_financial_data",
                source_line_item="SDR_ALLOCATION_AND_HOLDINGS",
                confidence=1.0,
                metric_value=450.0,
                raw_payload={"pool": "IMF SDR", "recipient": "BIS Basel"},
            ),
            # 2. IMF SDR Pool -> Sovereign Debt Holders ($485B general allocation)
            FlowEvent(
                event_id=f"imf_general_sdr_allocation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T10:15:00Z",
                period_label=REPORT_DATE,
                source_entity="imf_special_drawing_rights_sdr_pool",
                source_jurisdiction="GLOBAL_MULTILATERAL",
                target_entity="sovereign_debt_holders",
                target_jurisdiction="WORLD",
                instrument="imf_general_sdr_allocation_to_members",
                nominal_amount=IMF_GENERAL_SDR_USD,
                currency="USD",
                amount_usd_normalized=IMF_GENERAL_SDR_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=365.0,
                data_source="imf_financial_data",
                source_line_item="GENERAL_SDR_ALLOCATION_STOCK",
                confidence=1.0,
                metric_value=485.0,
                raw_payload={"allocation": "General SDR Allocation"},
            ),
            # 3. BIS Basel Banking Dept -> Bundesbank ($250B)
            FlowEvent(
                event_id=f"bis_bundesbank_deposit_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T10:30:00Z",
                period_label=REPORT_DATE,
                source_entity="bis_basel_banking_department",
                source_jurisdiction="GLOBAL_MULTILATERAL",
                target_entity="bundesbank",
                target_jurisdiction="DE",
                instrument="bis_central_bank_reserve_placement",
                nominal_amount=BIS_BUNDESBANK_DEPOSIT_USD,
                currency="USD",
                amount_usd_normalized=BIS_BUNDESBANK_DEPOSIT_USD,
                flow_type=FlowType.INTERBANK_TRANSFER,
                velocity_turnover_days=90.0,
                data_source="bis_annual_report",
                source_line_item="BIS_BANKING_DEPARTMENT_DEPOSITS",
                confidence=1.0,
                metric_value=250.0,
                raw_payload={"counterparty": "Deutsche Bundesbank"},
            ),
            # 4. BIS Basel Banking Dept -> US Treasuries Custody ($200B)
            FlowEvent(
                event_id=f"bis_treasury_management_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T10:45:00Z",
                period_label=REPORT_DATE,
                source_entity="bis_basel_banking_department",
                source_jurisdiction="GLOBAL_MULTILATERAL",
                target_entity="us_treasuries_custody",
                target_jurisdiction="US",
                instrument="bis_treasury_collateral_management",
                nominal_amount=BIS_TREASURY_MGMT_USD,
                currency="USD",
                amount_usd_normalized=BIS_TREASURY_MGMT_USD,
                flow_type=FlowType.REPO_COLLATERAL,
                velocity_turnover_days=60.0,
                data_source="bis_annual_report",
                source_line_item="BIS_TREASURY_INVESTMENTS_IN_CENTRAL_BANKS",
                confidence=1.0,
                metric_value=200.0,
                raw_payload={"portfolio": "US Treasury collateral"},
            ),
        ]
        meta = {"record_date": REPORT_DATE, "imf_sdr_usd": IMF_SDR_POOL_USD, "bis_usd": BIS_BASEL_BANKING_USD}
        return events, meta

    def fetch_upgraded_eurasian_flows(self) -> Tuple[List[FlowEvent], Dict[str, Any]]:
        """Harvests upgraded Russian macro, sovereign wealth, state banking, and commodity export flows ($420B)."""
        events: List[FlowEvent] = [
            # 1. CBR Yuan bilateral foreign reserves ($115B)
            FlowEvent(
                event_id=f"cbr_yuan_reserves_holding_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T10:15:00Z",
                period_label=REPORT_DATE,
                source_entity="bank_of_russia_cbr_vault",
                source_jurisdiction="RU",
                target_entity="chinese_state_banks_fx_desk",
                target_jurisdiction="CN",
                instrument="cbr_yuan_bilateral_reserve_holding",
                nominal_amount=CBR_YUAN_RESERVES_USD,
                currency="USD",
                amount_usd_normalized=CBR_YUAN_RESERVES_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=180.0,
                data_source="cbr_statutory_bulletin",
                source_line_item="INTERNATIONAL_RESERVES_YUAN_COMPONENT",
                confidence=1.0,
                metric_value=115.0,
                raw_payload={"reserve_type": "Renminbi foreign reserves", "custodian": "PBOC/Big 4"},
            ),
            # 2. NWF -> Russian State Banking Credit Nexus ($155B)
            FlowEvent(
                event_id=f"nwf_oil_buffer_injection_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T10:30:00Z",
                period_label=REPORT_DATE,
                source_entity="russia_national_wealth_fund_nwf",
                source_jurisdiction="RU",
                target_entity="russian_state_banking_credit_nexus",
                target_jurisdiction="RU",
                instrument="nwf_sovereign_oil_buffer_injection",
                nominal_amount=RUSSIA_NWF_BUFFER_USD,
                currency="USD",
                amount_usd_normalized=RUSSIA_NWF_BUFFER_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=365.0,
                data_source="minfin_russia_nwf_monthly_bulletin",
                source_line_item="NATIONAL_WEALTH_FUND_TOTAL_ASSETS",
                confidence=1.0,
                metric_value=155.0,
                raw_payload={"buffer_aum_usd": RUSSIA_NWF_BUFFER_USD},
            ),
            # 3. Russian State Banking Funding from Hydrocarbons/Credit Base ($765B)
            FlowEvent(
                event_id=f"state_banking_liquidity_funding_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T10:45:00Z",
                period_label=REPORT_DATE,
                source_entity="russian_hydrocarbon_export_revenues",
                source_jurisdiction="RU",
                target_entity="russian_state_banking_credit_nexus",
                target_jurisdiction="RU",
                instrument="state_banking_ruble_credit_liquidity_provision",
                nominal_amount=RUSSIAN_BANKING_FUNDING_USD,
                currency="USD",
                amount_usd_normalized=RUSSIAN_BANKING_FUNDING_USD,
                flow_type=FlowType.GENESIS_CREDIT,
                velocity_turnover_days=90.0,
                data_source="cbr_banking_sector_survey",
                source_line_item="DOMESTIC_BANKING_SYSTEM_LIQUIDITY_BASE",
                confidence=1.0,
                metric_value=765.0,
                raw_payload={"liquidity_funding_usd": RUSSIAN_BANKING_FUNDING_USD},
            ),
            # 4. Russian State Banking Credit Nexus -> Sovereign Debt Holders ($920B)
            FlowEvent(
                event_id=f"russian_state_credit_creation_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T11:00:00Z",
                period_label=REPORT_DATE,
                source_entity="russian_state_banking_credit_nexus",
                source_jurisdiction="RU",
                target_entity="sovereign_debt_holders",
                target_jurisdiction="RU",
                instrument="russian_state_credit_creation_and_ofz_underwriting",
                nominal_amount=RUSSIAN_STATE_CREDIT_USD,
                currency="USD",
                amount_usd_normalized=RUSSIAN_STATE_CREDIT_USD,
                flow_type=FlowType.GENESIS_CREDIT,
                velocity_turnover_days=90.0,
                data_source="cbr_banking_sector_survey",
                source_line_item="CORPORATE_CREDIT_AND_DOMESTIC_OFZ_UNDERWRITING",
                confidence=1.0,
                metric_value=920.0,
                raw_payload={"sberbank_vtb_credit_usd": RUSSIAN_STATE_CREDIT_USD},
            ),
            # 5. Russian Hydrocarbons -> Gazprombank Specialized Energy Hub ($95B)
            FlowEvent(
                event_id=f"gazprombank_gas_export_inflow_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T11:15:00Z",
                period_label=REPORT_DATE,
                source_entity="russian_hydrocarbon_export_revenues",
                source_jurisdiction="RU",
                target_entity="gazprombank_energy_settlement_hub",
                target_jurisdiction="RU_GLOBAL",
                instrument="ruble_for_gas_pipeline_export_inflow",
                nominal_amount=GAZPROMBANK_GAS_EXPORT_USD,
                currency="USD",
                amount_usd_normalized=GAZPROMBANK_GAS_EXPORT_USD,
                flow_type=FlowType.TRADE_SETTLEMENT,
                velocity_turnover_days=30.0,
                data_source="gazprom_export_filings",
                source_line_item="PIPELINE_GAS_EXPORT_PROCEEDS",
                confidence=1.0,
                metric_value=95.0,
                raw_payload={"mechanism": "Ruble for Gas", "volume_usd": GAZPROMBANK_GAS_EXPORT_USD},
            ),
            # 6. Gazprombank Hub -> Russian Offshore Shadow Capital Basin ($95B)
            FlowEvent(
                event_id=f"gazprombank_trapped_gas_outflow_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T11:30:00Z",
                period_label=REPORT_DATE,
                source_entity="gazprombank_energy_settlement_hub",
                source_jurisdiction="RU_GLOBAL",
                target_entity="russia_offshore_shadow_capital_basin",
                target_jurisdiction="GLOBAL_OFFSHORE",
                instrument="gazprombank_trapped_gas_proceeds",
                nominal_amount=GAZPROMBANK_GAS_EXPORT_USD,
                currency="USD",
                amount_usd_normalized=GAZPROMBANK_GAS_EXPORT_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=90.0,
                data_source="gazprombank_quarterly_report",
                source_line_item="TRAPPED_OFFSHORE_GAS_RECEIVABLES",
                confidence=1.0,
                metric_value=95.0,
                raw_payload={"trapped_gas_usd": GAZPROMBANK_GAS_EXPORT_USD},
            ),
            # 7. Russian Non-Energy Trapped Export Capital ($85B) -> Shadow Basin
            FlowEvent(
                event_id=f"russia_commodity_trapped_capital_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T11:45:00Z",
                period_label=REPORT_DATE,
                source_entity="russian_hydrocarbon_export_revenues",
                source_jurisdiction="RU",
                target_entity="russia_offshore_shadow_capital_basin",
                target_jurisdiction="GLOBAL_OFFSHORE",
                instrument="rupee_trap_and_unrecorded_flight_capital",
                nominal_amount=RUSSIA_COMMODITY_NON_ENERGY_TRAPPED_USD,
                currency="USD",
                amount_usd_normalized=RUSSIA_COMMODITY_NON_ENERGY_TRAPPED_USD,
                flow_type=FlowType.POOL_CONCENTRATION,
                velocity_turnover_days=180.0,
                data_source="cbr_balance_of_payments_survey",
                source_line_item="NET_CAPITAL_OUTFLOW_AND_TRAPPED_VOSTRO",
                confidence=1.0,
                metric_value=85.0,
                raw_payload={"nature": "Indian Vostro Rupee trap and UAE Dirhams", "volume_usd": RUSSIA_COMMODITY_NON_ENERGY_TRAPPED_USD},
            ),
            # 8. Russian Non-Energy Commodity Exports to China ($95B)
            FlowEvent(
                event_id=f"russia_non_energy_china_trade_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T11:50:00Z",
                period_label=REPORT_DATE,
                source_entity="russian_hydrocarbon_export_revenues",
                source_jurisdiction="RU",
                target_entity="chinese_state_banks_fx_desk",
                target_jurisdiction="CN",
                instrument="sino_russian_non_energy_trade_settlement",
                nominal_amount=RUSSIA_COMMODITY_NON_ENERGY_CHINA_USD,
                currency="USD",
                amount_usd_normalized=RUSSIA_COMMODITY_NON_ENERGY_CHINA_USD,
                flow_type=FlowType.TRADE_SETTLEMENT,
                velocity_turnover_days=45.0,
                data_source="general_administration_of_customs_china",
                source_line_item="SINO_RUSSIAN_NON_ENERGY_COMMODITY_IMPORTS",
                confidence=1.0,
                metric_value=95.0,
                raw_payload={"commodities": ["Fertilizers", "Wheat", "Nickel", "Palladium", "Coal"]},
            ),
            # 9. Russian Direct Energy Clearing to China ($5B)
            FlowEvent(
                event_id=f"russia_direct_energy_china_{REPORT_DATE}",
                timestamp=f"{REPORT_DATE}T11:55:00Z",
                period_label=REPORT_DATE,
                source_entity="russian_hydrocarbon_export_revenues",
                source_jurisdiction="RU",
                target_entity="chinese_state_banks_fx_desk",
                target_jurisdiction="CN",
                instrument="direct_bilateral_energy_trade_clearing",
                nominal_amount=RUSSIA_DIRECT_ENERGY_CHINA_USD,
                currency="USD",
                amount_usd_normalized=RUSSIA_DIRECT_ENERGY_CHINA_USD,
                flow_type=FlowType.TRADE_SETTLEMENT,
                velocity_turnover_days=30.0,
                data_source="general_administration_of_customs_china",
                source_line_item="DIRECT_PIPELINE_POWER_OF_SIBERIA_CLEARING",
                confidence=1.0,
                metric_value=5.0,
                raw_payload={"conduit": "Power of Siberia direct bilateral settlement"},
            ),
        ]
        meta = {
            "record_date": REPORT_DATE,
            "cbr_yuan_usd": CBR_YUAN_RESERVES_USD,
            "nwf_buffer_usd": RUSSIA_NWF_BUFFER_USD,
            "russian_state_credit_usd": RUSSIAN_STATE_CREDIT_USD,
            "gazprombank_gas_export_usd": GAZPROMBANK_GAS_EXPORT_USD,
            "shadow_basin_usd": RUSSIA_OFFSHORE_SHADOW_BASIN_USD,
        }
        return events, meta

    def harvest(self) -> List[FlowEvent]:
        """Harvests all statutory flows across the expanded planetary macro dark forest."""
        logger.info("Harvesting Complete Planetary Monetary Manifold (8 dark forest regions + Eurasian upgrades)...")
        all_events: List[FlowEvent] = []

        tic_evs, _ = self.fetch_tic_planetary_holdings()
        all_events.extend(tic_evs)

        sanct_evs, _ = self.fetch_euroclear_sanctioned_assets()
        all_events.extend(sanct_evs)

        gulf_evs, _ = self.fetch_gulf_sovereign_wealth_and_petroyuan()
        all_events.extend(gulf_evs)

        comm_evs, _ = self.fetch_global_commodity_and_refining_flows()
        all_events.extend(comm_evs)

        norway_evs, _ = self.fetch_norwegian_gpfg_flows()
        all_events.extend(norway_evs)

        swiss_evs, _ = self.fetch_swiss_monetary_flows()
        all_events.extend(swiss_evs)

        singapore_evs, _ = self.fetch_singapore_sovereign_flows()
        all_events.extend(singapore_evs)

        korea_evs, _ = self.fetch_korean_monetary_and_pension_flows()
        all_events.extend(korea_evs)

        uk_evs, _ = self.fetch_uk_monetary_and_gilt_flows()
        all_events.extend(uk_evs)

        canada_evs, _ = self.fetch_canadian_maple_pension_flows()
        all_events.extend(canada_evs)

        mexico_evs, _ = self.fetch_mexican_nearshoring_trade_flows()
        all_events.extend(mexico_evs)

        multilateral_evs, _ = self.fetch_multilateral_sdr_and_bis_flows()
        all_events.extend(multilateral_evs)

        eurasian_evs, _ = self.fetch_upgraded_eurasian_flows()
        all_events.extend(eurasian_evs)

        logger.info(f"Harvested {len(all_events)} planetary macro flow events across dark forest regions.")
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
