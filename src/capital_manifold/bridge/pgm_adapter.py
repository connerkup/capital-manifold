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
    # Dark Forest Ring 2: The QT Burn Chamber, Evaporating RRP Buffer, and Offshore Eurodollar Sinks
    "fed_soma_qt_burn_chamber": {
        "tier": MonetaryTier.SINK,
        "name": "Federal Reserve SOMA QT Money Burn Chamber",
        "sector": "qt_burn_chamber",
        "jurisdiction": "US",
        "description": "Literal destruction of central bank base money via maturing bond runoff ($2.157T burned).",
    },
    "fed_on_rrp_buffer_sink": {
        "tier": MonetaryTier.SINK,
        "name": "Fed Overnight Reverse Repo (ON RRP) Liquidity Buffer",
        "sector": "fed_rrp_facility",
        "jurisdiction": "US",
        "description": "Fed facility for non-bank cash parking, depleted 85% from $2.55T peak down to $361.88B.",
    },
    "offshore_cayman_hedge_pool": {
        "tier": MonetaryTier.SINK,
        "name": "Cayman Islands Offshore Hedge Fund Collateral Basin",
        "sector": "offshore_hedge_pool",
        "jurisdiction": "GLOBAL_OFFSHORE",
        "description": "Offshore shadow banking liquidity and Treasury collateral sink ($285.3B TIC).",
    },
    "london_eurodollar_pool": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "London Eurodollar Cross-Border Treasury Nexus",
        "sector": "london_eurodollar_nexus",
        "jurisdiction": "UK",
        "description": "London interbank and wholesale Eurodollar financing conduit holding $668.3B US Treasuries.",
    },
    "fed_ecb_liquidity_swap_line": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Federal Reserve / ECB Central Bank Liquidity Swap Line",
        "sector": "central_bank_swap_facility",
        "jurisdiction": "TRANSATLANTIC",
        "description": "Standing reciprocal currency arrangement serving as emergency dollar backstop ($207M active).",
    },
    # Global Liquidity Triangle: Yen Carry Faucet, Corporate Buyback Sink, Petrodollar Recycling
    "japan_mof_boj_carry_faucet": {
        "tier": MonetaryTier.GENESIS,
        "name": "Japan Ministry of Finance & Bank of Japan Zero-Rate Faucet",
        "sector": "japan_carry_faucet",
        "jurisdiction": "JP",
        "description": "Genesis provider of zero/ultra-low cost JPY liquidity anchoring $1.104T in US Treasuries.",
    },
    "japan_institutional_carry_desk": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Japanese Institutional Carry Desks (Norinchukin / Japan Post / Lifers)",
        "sector": "institutional_carry_desk",
        "jurisdiction": "JP",
        "description": "Institutional conduits executing cross-currency FX basis swaps to fund USD repo and sovereign debt.",
    },
    "apple_bigtech_treasury_vault": {
        "tier": MonetaryTier.SINK,
        "name": "Apple Big Tech Enterprise Treasury Cash Hoard",
        "sector": "corporate_treasury_vault",
        "jurisdiction": "US",
        "description": "Corporate cash and marketable securities hoard ($62.40B) absorbing commercial paper and T-bills.",
    },
    "corporate_share_buyback_burn_chamber": {
        "tier": MonetaryTier.SINK,
        "name": "Corporate Share Buyback Equity Retirement Burn Chamber",
        "sector": "corporate_buyback_burn",
        "jurisdiction": "US",
        "description": "Permanent equity capital retirement destroying liquid corporate cash flow ($62.09B buyback burn).",
    },
    "gulf_petrodollar_sovereign_wealth_basin": {
        "tier": MonetaryTier.SINK,
        "name": "Gulf GCC Sovereign Wealth Fund Energy Surplus Basin (ADIA / PIF / QIA)",
        "sector": "petrodollar_wealth_basin",
        "jurisdiction": "MIDDLE_EAST",
        "description": "Petrodollar accumulation pool recycling $85B+ energy trade surpluses into Western sovereign assets.",
    },
    # Planetary Monetary Manifold (7 Global Regions)
    "pboc_safe_foreign_reserves": {
        "tier": MonetaryTier.GENESIS,
        "name": "People's Bank of China & SAFE Foreign Exchange Reserves",
        "sector": "sovereign_fx_vault",
        "jurisdiction": "CN",
        "description": "Sovereign foreign exchange reserve vault ($3.24T reserves, $859.4B US Treasuries anchor).",
    },
    "chinese_state_banks_fx_desk": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Chinese Big 4 State Banks FX & Interbank Trading Desks (ICBC/CCB/BoC/ABC)",
        "sector": "state_commercial_bank",
        "jurisdiction": "CN",
        "description": "State commercial bank FX trading conduits clearing cross-border trade and managing onshore liquidity.",
    },
    "offshore_cnh_hong_kong_hub": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "Hong Kong Offshore Renminbi (CNH) Clearing Hub",
        "sector": "offshore_cnh_hub",
        "jurisdiction": "HK",
        "description": "Offshore CNH interbank liquidity pool and debt issuance center ($250B daily turnover).",
    },
    "taiwan_central_bank_tsmc_semiconductor_sink": {
        "tier": MonetaryTier.SINK,
        "name": "Taiwan Central Bank & TSMC Advanced Silicon Capital Sink",
        "sector": "semiconductor_hardware",
        "jurisdiction": "TW",
        "description": "Advanced semiconductor manufacturing hardware revenues ($120B) and foreign reserves ($234.6B TIC).",
    },
    "saudi_sama_pif_nexus": {
        "tier": MonetaryTier.SINK,
        "name": "Saudi Central Bank SAMA & Public Investment Fund (PIF) Nexus",
        "sector": "sovereign_wealth_fund",
        "jurisdiction": "SA",
        "description": "Saudi sovereign energy surplus and strategic wealth fund ($925B AUM) channeling petro-revenues.",
    },
    "uae_adia_mubadala_basin": {
        "tier": MonetaryTier.SINK,
        "name": "UAE Sovereign Wealth Basin (ADIA & Mubadala Investment)",
        "sector": "sovereign_wealth_basin",
        "jurisdiction": "AE",
        "description": "Abu Dhabi and UAE global asset accumulation pool ($1.15T AUM) recycling trade surpluses.",
    },
    "petro_yuan_bilateral_settlement_bridge": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Petro-Yuan Bilateral Non-USD Energy Settlement Bridge",
        "sector": "bilateral_clearing",
        "jurisdiction": "GLOBAL_OFFSHORE",
        "description": "Bilateral clearing corridor for crude oil trade settling in CNH/Renminbi bypassing SWIFT/USD.",
    },
    "bank_of_russia_cbr_vault": {
        "tier": MonetaryTier.GENESIS,
        "name": "Bank of Russia (CBR) Sovereign Vault & Foreign Reserves",
        "sector": "sanctioned_central_bank",
        "jurisdiction": "RU",
        "description": "Sanctioned central bank vault with $300B frozen Western reserves, pivoting to $185B gold and $115B CNY.",
    },
    "shadow_tanker_energy_arbitrage": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Maritime Shadow Tanker Fleet Crude Oil Arbitrage Conduit",
        "sector": "maritime_energy_arbitrage",
        "jurisdiction": "GLOBAL_MARITIME",
        "description": "Non-G7 insured shadow tanker maritime transit carrying $140B Russian crude evading Western price caps.",
    },
    "brazil_banco_central_agri_faucet": {
        "tier": MonetaryTier.GENESIS,
        "name": "Banco Central do Brasil & Agricultural Export Faucet",
        "sector": "commodity_central_bank",
        "jurisdiction": "BR",
        "description": "Agricultural commodity surplus anchor ($110B soy/iron ore) holding $214.0B in US Treasuries.",
    },
    "reserve_bank_of_australia_commodity_faucet": {
        "tier": MonetaryTier.GENESIS,
        "name": "Reserve Bank of Australia & Pacific Resources Commodity Faucet",
        "sector": "commodity_central_bank",
        "jurisdiction": "AU",
        "description": "Pacific raw material supplier ($180B iron ore/LNG) powering Asian industrial processors.",
    },
    "reserve_bank_of_india_refining_hub": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Reserve Bank of India & Jamnagar Crude Refining Hub",
        "sector": "energy_refining_hub",
        "jurisdiction": "IN",
        "description": "Refining hub importing discounted Russian crude and re-exporting $55B in refined diesel/jet fuel to Europe.",
    },
    "africa_critical_minerals_debt_conduit": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "African Critical Minerals Concession & Debt Servicing Conduit",
        "sector": "frontier_mineral_conduit",
        "jurisdiction": "AFRICA",
        "description": "DRC/Zambia cobalt and copper mining concessions servicing $45B in sovereign loans to Chinese state lenders.",
    },
    # Phase 3 Topology Resilience & Dark Matter Architecture
    "ficc_sponsored_repo_clearing": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "DTCC FICC Sponsored Repo Clearing Platform",
        "sector": "clearinghouse_repo",
        "jurisdiction": "US",
        "description": "FICC sponsored DVP repo platform ($1.2T daily clearing) providing centralized netting and bypassing triparty broker-dealers.",
    },
    "fed_standing_repo_facility": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Federal Reserve Standing Repo Facility (SRF)",
        "sector": "central_bank_liquidity_backstop",
        "jurisdiction": "US",
        "description": "Federal Reserve standing facility ($500B capacity) offering daily overnight repo backstop against Treasury collateral.",
    },
    "ca_cib_natixis_dealer_syndicate": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Crédit Agricole CIB & Natixis Secondary SVT Syndicate",
        "sector": "primary_dealer_syndicate",
        "jurisdiction": "FR_EU",
        "description": "Secondary French primary dealer syndication syndicate providing issuance clearance resilience and FX swap facilities.",
    },
    "bis_otc_derivatives_pool": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "BIS Global OTC Derivatives Clearing Pool",
        "sector": "macro_dark_matter",
        "jurisdiction": "GLOBAL_OFFSHORE",
        "description": "Offshore global OTC derivatives market ($25T gross market value, $600T gross notional) dominating interest rate and FX swap risk.",
    },
    "dtcc_treasury_basis_trade_clearing": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "DTCC Treasury Cash-Futures Basis Trade Clearing",
        "sector": "macro_dark_matter",
        "jurisdiction": "US",
        "description": "Hedge fund Treasury cash-futures basis trade clearing pool ($800B repo leverage) absorbing duration risk via bilateral repo.",
    },
    "pboc_bilateral_swap_network": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "PBOC Bilateral Currency Swap Agreement Network",
        "sector": "macro_dark_matter",
        "jurisdiction": "CN_GLOBAL",
        "description": "People's Bank of China network of 40+ bilateral local currency swap lines ($550B total capacity) bypassing USD correspondent banking.",
    },
    "imf_errors_and_omissions_pool": {
        "tier": MonetaryTier.SINK,
        "name": "IMF Global Balance of Payments Net Errors & Omissions Pool",
        "sector": "macro_dark_matter",
        "jurisdiction": "GLOBAL",
        "description": "Global statistical discrepancy and unrecorded capital flight sink ($175B annual) capturing dark matter cross-border flows.",
    },
    # Desk Master Multi-Domain Governance Hierarchy (Private Asset Portfolios & Principal Holdings)
    "conner_principal_vault": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "Conner Principal Sovereign Vault",
        "sector": "apex_family_office",
        "jurisdiction": "US",
        "description": "Layer 0 Apex decision architecture, sovereign capital, T-bill cash reserves, and multi-domain liquidity allocation.",
    },
    "launchfizz_treasury_vault": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "LaunchFizz Commercial Studio Treasury",
        "sector": "operating_venture",
        "jurisdiction": "US",
        "description": "Layer 1 Studio commercial cashflow, agency wholesale operating accounts, and vendor payroll conduit.",
    },
    "vesperspatial_actuarial_reserves": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "VesperSpatial Actuarial Catastrophe Reserves",
        "sector": "catastrophe_underwriting",
        "jurisdiction": "US",
        "description": "Layer 1 Delphi-1.0 catastrophe risk underwriting liquidity, PML spatial accumulation collateral, and reinsurance escrow.",
    },
    "silvera_renewable_packaging": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "Silvera Renewable Packaging Co.",
        "sector": "clean_manufacturing",
        "jurisdiction": "US",
        "description": "Layer 1 Molded-fiber Capex, bio-resin equipment financing conduit, and ag residue feedstock working capital.",
    },
    "scientific_fleet_compute_pool": {
        "tier": MonetaryTier.TRAVERSAL,
        "name": "Scientific Fleet Distributed Compute Pool",
        "sector": "scientific_compute",
        "jurisdiction": "US",
        "description": "Layer 2B TWE / Jarvis / Kinetic compute budget, GPU cluster allocations, and prediction market calibration funds.",
    },
    "valle_rd_asset_ledger": {
        "tier": MonetaryTier.SINK,
        "name": "Valle Road Real Estate Asset Ledger",
        "sector": "private_real_estate",
        "jurisdiction": "US",
        "description": "Long-term background real estate holding, mortgage amortizations, and equity collateral cushion.",
    },
    "family_office_principal_endowment": {
        "tier": MonetaryTier.GENESIS,
        "name": "Family Office Principal Sovereign Capital Endowment",
        "sector": "apex_family_office",
        "jurisdiction": "US",
        "description": "Sovereign capital equity reserve providing foundational liquidity endowments to the apex principal vault.",
    },
    "us_treasuries_custody": {
        "tier": MonetaryTier.SINK,
        "name": "US Treasuries Statutory Custodial Escrow",
        "sector": "custodial_escrow",
        "jurisdiction": "US",
        "description": "Statutory custodial escrow holding pledged Treasury bill collateral backing Delphi reinsurance underwriting capacity.",
    },
    "agency_operating_payroll_and_vendors": {
        "tier": MonetaryTier.SINK,
        "name": "Agency Operating Payroll & Production Vendors",
        "sector": "commercial_vendors",
        "jurisdiction": "US",
        "description": "Wholesale commercial vendor disbursements and creative production payroll settlement.",
    },
    "commercial_cloud_and_saas_vendors": {
        "tier": MonetaryTier.SINK,
        "name": "Commercial Cloud, SaaS & IT Infrastructure Vendors",
        "sector": "technology_vendors",
        "jurisdiction": "US",
        "description": "Enterprise cloud services, operational software subscriptions, and developer toolchain disbursements.",
    },
    "catastrophe_reinsurance_cedants": {
        "tier": MonetaryTier.GENESIS,
        "name": "Global Catastrophe Reinsurance Cedants & Syndicates",
        "sector": "reinsurance_market",
        "jurisdiction": "GLOBAL",
        "description": "Primary insurance carriers and Lloyd's syndicates ceding catastrophe risk premiums into VesperSpatial Delphi reserves.",
    },
    "molded_fiber_tooling_and_feedstock_vendors": {
        "tier": MonetaryTier.SINK,
        "name": "Molded-Fiber Tooling & Ag Feedstock Suppliers",
        "sector": "industrial_supply",
        "jurisdiction": "US",
        "description": "Machinery manufacturers, tooling fabricators, and agricultural residue feedstock suppliers.",
    },
    "valle_rd_property_equity_escrow": {
        "tier": MonetaryTier.SINK,
        "name": "Valle Road Property Retained Equity & Escrow Cushion",
        "sector": "real_estate_equity",
        "jurisdiction": "US",
        "description": "Unlevered equity value cushion and long-term capital improvement reserve for background real estate holdings.",
    },
    "us_corporate_and_household_borrowers": {
        "tier": MonetaryTier.SINK,
        "name": "US Corporate & Household Commercial Bank Borrowers",
        "sector": "commercial_borrowers",
        "jurisdiction": "US",
        "description": "Domestic non-financial business and consumer credit sink absorbing commercial bank credit creation.",
    },
    "us_commercial_bank_credit_pool": {
        "tier": MonetaryTier.TRANSMISSION,
        "name": "US Commercial Banking Credit & Revolving Facility Pool",
        "sector": "commercial_bank",
        "jurisdiction": "US",
        "description": "Domestic banking system commercial credit creation, credit line revolving facilities, and mortgage underwriting nexus.",
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
            # Dark Forest Ring 2: QT Burn, RRP Drain & Offshore Eurodollar Sinks
            "rrp_cash_parking",
            "tga_debt_issuance_absorption",
            "qt_redemption_money_burn",
            "eurodollar_syndication",
            "cayman_shadow_capital_flight",
            "emergency_fx_swap_activation",
            "central_bank_dollar_injection",
            # Global Liquidity Triangle: Yen Carry, Corporate Buybacks, Petrodollars
            "jpy_zero_interest_liquidity_provision",
            "yen_carry_dollar_treasury_absorption",
            "corporate_commercial_paper_and_t_bill_placement",
            "equity_share_retirement_buyback_burn",
            "petrodollar_energy_surplus_accumulation",
            "sovereign_wealth_oat_diversification",
            "global_enterprise_tech_inflow",
            # Planetary Monetary Manifold (7 Global Regions)
            "petro_yuan_crude_invoicing",
            "cnh_cross_border_liquidity_settlement",
            "onshore_offshore_cnh_repatriation",
            "sovereign_fx_reserve_accumulation",
            "direct_petro_yuan_clearing",
            "shadow_tanker_crude_export",
            "discounted_crude_refining_intake",
            "refined_diesel_european_reexport",
            "global_product_fuel_distribution",
            "australian_iron_ore_lng_settlement",
            "brazilian_agri_resource_settlement",
            "cross_strait_electronics_demand",
            "advanced_semiconductor_hardware_shipment",
            "resource_concession_debt_servicing",
            "belt_and_road_infrastructure_lending",
            "gulf_sovereign_euro_debt_placement",
            "saudi_capital_diversification_oat",
            "immobilized_euroclear_reserve_claim",
            # Phase 3 Topology Resilience & Dark Matter Relations
            "sponsored_repo_clearing_injection",
            "sponsored_dvp_repo_settlement",
            "srf_backstop_liquidity_injection",
            "oat_secondary_syndication_auction",
            "syndicate_reserve_clearing",
            "syndicate_usd_fx_swap",
            "basis_trade_leverage_absorption",
            "otc_derivatives_collateral_drain",
            "pboc_bilateral_swap_activation",
            "imf_errors_and_omissions_absorption",
            "syndicate_sponsored_repo_conduit",
            "fx_swap_sponsored_repo_conduit",
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
            # Dark Forest Ring 2 sectors
            "qt_burn_chamber": 59,
            "fed_rrp_facility": 57,
            "offshore_hedge_pool": 55,
            "london_eurodollar_nexus": 49,
            "central_bank_swap_facility": 46,
            # Global Liquidity Triangle sectors
            "japan_carry_faucet": 37,
            "institutional_carry_desk": 45,
            "corporate_treasury_vault": 54,
            "corporate_buyback_burn": 58,
            "petrodollar_wealth_basin": 56,
            # Planetary Monetary Manifold sectors
            "sovereign_fx_vault": 33,
            "state_commercial_bank": 39,
            "offshore_cnh_hub": 47,
            "semiconductor_hardware": 53,
            "sovereign_wealth_fund": 56,
            "sovereign_wealth_basin": 57,
            "bilateral_clearing": 43,
            "sanctioned_central_bank": 35,
            "maritime_energy_arbitrage": 41,
            "commodity_central_bank": 38,
            "energy_refining_hub": 51,
            "frontier_mineral_conduit": 45,
            # Phase 3 sectors
            "clearinghouse_repo": 40,
            "central_bank_liquidity_backstop": 44,
            "primary_dealer_syndicate": 40,
            "macro_dark_matter": 48,
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
            if "CN" in meta["jurisdiction"]:
                vec[35] += 0.8
            if "RU" in meta["jurisdiction"]:
                vec[36] += 0.8
            if "SA" in meta["jurisdiction"] or "AE" in meta["jurisdiction"]:
                vec[37] += 0.8
            if "AU" in meta["jurisdiction"]:
                vec[38] += 0.8
            if "BR" in meta["jurisdiction"]:
                vec[39] += 0.8
            if "IN" in meta["jurisdiction"]:
                vec[40] += 0.8
            if "TW" in meta["jurisdiction"]:
                vec[41] += 0.8
            if "HK" in meta["jurisdiction"]:
                vec[42] += 0.8
            if "AFRICA" in meta["jurisdiction"]:
                vec[43] += 0.8
            if "GLOBAL" in meta["jurisdiction"] or "WORLD" in meta["jurisdiction"]:
                vec[35] += 0.8
            if "US" in meta["jurisdiction"]:
                vec[35] += 1.2
            if "OFFSHORE" in meta["jurisdiction"]:
                vec[34] += 0.9
            if "UK" in meta["jurisdiction"]:
                vec[33] += 0.9
            if "TRANSATLANTIC" in meta["jurisdiction"]:
                vec[34] += 0.8
                vec[35] += 0.8
            if "JP" in meta["jurisdiction"]:
                vec[35] += 0.9
            if "MIDDLE_EAST" in meta["jurisdiction"]:
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
            # Dark Forest Ring 2
            elif eid == "fed_soma_qt_burn_chamber":
                vec[120:128] = np.array([1.5, 0.4, 0.9, 1.8, 0.2, 0.6, 1.3, 1.0], dtype=np.float32)
            elif eid == "fed_on_rrp_buffer_sink":
                vec[120:128] = np.array([0.3, 0.6, 1.2, 1.1, 0.1, 0.8, 1.0, 0.7], dtype=np.float32)
            elif eid == "offshore_cayman_hedge_pool":
                vec[120:128] = np.array([0.4, 0.7, 1.3, 1.2, 0.3, 0.9, 1.1, 0.8], dtype=np.float32)
            elif eid == "london_eurodollar_pool":
                vec[112:120] = np.array([0.5, 0.9, 1.4, 1.3, 0.4, 1.0, 0.8, 0.6], dtype=np.float32)
            elif eid == "fed_ecb_liquidity_swap_line":
                vec[104:112] = np.array([spread_norm * 1.6, pressure_norm * 1.2, 1.4, 1.0, 0.8, 0.6, 0.5, 0.4], dtype=np.float32)
            # Global Liquidity Triangle
            elif eid == "japan_mof_boj_carry_faucet":
                vec[96:104] = np.array([0.1, 0.2, 0.4, 0.9, 1.5, 1.2, 0.8, 0.6], dtype=np.float32)
            elif eid == "japan_institutional_carry_desk":
                vec[104:112] = np.array([spread_norm * 0.8, 0.7, 1.3, 1.1, 0.6, 0.8, 0.4, 0.5], dtype=np.float32)
            elif eid == "apple_bigtech_treasury_vault":
                vec[120:128] = np.array([0.1, 0.4, 1.6, 1.5, 0.2, 0.8, 1.2, 0.9], dtype=np.float32)
            elif eid == "corporate_share_buyback_burn_chamber":
                vec[120:128] = np.array([1.8, 0.2, 0.8, 1.6, 0.1, 0.5, 1.4, 1.1], dtype=np.float32)
            elif eid == "gulf_petrodollar_sovereign_wealth_basin":
                vec[120:128] = np.array([0.3, 0.5, 1.4, 1.2, 0.7, 1.0, 0.9, 0.8], dtype=np.float32)
            # Planetary Monetary Manifold (7 Global Regions)
            elif eid == "pboc_safe_foreign_reserves":
                vec[96:104] = np.array([0.9, 0.8, 1.5, 1.8, 1.2, 0.7, 1.4, 1.1], dtype=np.float32)
            elif eid == "chinese_state_banks_fx_desk":
                vec[104:112] = np.array([0.8, 1.4, 1.2, 0.9, 0.8, 1.0, 0.6, 0.7], dtype=np.float32)
            elif eid == "offshore_cnh_hong_kong_hub":
                vec[112:120] = np.array([0.7, 1.3, 1.1, 1.5, 0.5, 0.9, 1.0, 0.8], dtype=np.float32)
            elif eid == "taiwan_central_bank_tsmc_semiconductor_sink":
                vec[120:128] = np.array([0.4, 0.6, 1.5, 1.7, 0.3, 0.8, 1.3, 1.0], dtype=np.float32)
            elif eid == "saudi_sama_pif_nexus":
                vec[120:128] = np.array([0.5, 0.4, 1.8, 1.6, 0.2, 0.9, 1.1, 0.7], dtype=np.float32)
            elif eid == "uae_adia_mubadala_basin":
                vec[120:128] = np.array([0.4, 0.5, 1.7, 1.5, 0.3, 0.8, 1.2, 0.9], dtype=np.float32)
            elif eid == "petro_yuan_bilateral_settlement_bridge":
                vec[104:112] = np.array([0.6, 1.2, 0.8, 1.4, 0.5, 1.1, 0.7, 0.9], dtype=np.float32)
            elif eid == "bank_of_russia_cbr_vault":
                vec[96:104] = np.array([1.8, 0.2, 0.5, 1.4, 1.6, 0.3, 1.2, 0.9], dtype=np.float32)
            elif eid == "shadow_tanker_energy_arbitrage":
                vec[104:112] = np.array([1.4, 0.8, 1.1, 0.9, 0.4, 1.3, 0.8, 0.5], dtype=np.float32)
            elif eid == "brazil_banco_central_agri_faucet":
                vec[96:104] = np.array([0.3, 0.4, 0.9, 1.3, 1.1, 0.8, 0.7, 0.6], dtype=np.float32)
            elif eid == "reserve_bank_of_australia_commodity_faucet":
                vec[96:104] = np.array([0.4, 0.5, 0.8, 1.5, 1.2, 0.9, 0.6, 0.7], dtype=np.float32)
            elif eid == "reserve_bank_of_india_refining_hub":
                vec[104:112] = np.array([0.7, 1.1, 1.3, 1.0, 0.6, 0.9, 0.8, 0.5], dtype=np.float32)
            elif eid == "africa_critical_minerals_debt_conduit":
                vec[104:112] = np.array([1.2, 0.6, 0.9, 0.7, 0.3, 1.0, 0.5, 0.8], dtype=np.float32)
            # Phase 3 Entity Embeddings
            elif eid == "ficc_sponsored_repo_clearing":
                vec[104:112] = np.array([0.5, 0.9, 1.7, 1.4, 0.3, 1.0, 1.1, 0.8], dtype=np.float32)
            elif eid == "fed_standing_repo_facility":
                vec[104:112] = np.array([0.2, 0.4, 1.8, 1.6, 0.1, 0.9, 1.3, 1.0], dtype=np.float32)
            elif eid == "ca_cib_natixis_dealer_syndicate":
                vec[104:112] = np.array([spread_norm * 0.75, pressure_norm * 0.65, 0.7, 0.6, t2_norm * 0.4, 0.5, 0.4, 0.3], dtype=np.float32)
            elif eid == "bis_otc_derivatives_pool":
                vec[112:120] = np.array([1.9, 1.1, 1.6, 1.8, 1.4, 1.2, 1.5, 1.3], dtype=np.float32)
            elif eid == "dtcc_treasury_basis_trade_clearing":
                vec[104:112] = np.array([1.2, 0.8, 1.5, 1.4, 0.9, 1.1, 0.7, 1.0], dtype=np.float32)
            elif eid == "pboc_bilateral_swap_network":
                vec[104:112] = np.array([0.8, 1.0, 1.2, 1.3, 0.9, 0.7, 1.1, 0.6], dtype=np.float32)
            elif eid == "imf_errors_and_omissions_pool":
                vec[120:128] = np.array([1.1, 0.9, 0.7, 1.4, 1.2, 0.8, 1.0, 1.3], dtype=np.float32)

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
        velocity_turnover_days: Optional[float] = None,
    ) -> float:
        """Calculates edge weight directly proportional to risk friction and inversely to flow volume.

        Formula:
            Weight (impedance) = W_base * (1 + kappa * risk_friction) / (1 + gamma * log10(1 + V_B))
            where V_B is normalized volume in Billions EUR (annualized if velocity_turnover_days provided).
        Domestic reinvestment incurs amplified impedance when sovereign risk friction spreads widen.
        """
        if velocity_turnover_days is not None and velocity_turnover_days > 0.0:
            effective_vol = flow_volume_eur * (365.0 / max(float(velocity_turnover_days), 1.0))
        else:
            effective_vol = flow_volume_eur

        vol_b = max(0.0, abs(effective_vol) / 1e9)
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
            base_weight=2.40,
            flow_volume_eur=285.0e9,
            risk_friction=spread_friction,
            is_domestic_retention=False,
            velocity_turnover_days=30.0,
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

        # Corridor 6: Dark Forest Ring 2: QT Burn Chamber, Evaporating RRP Buffer, and Offshore Eurodollar Sinks
        # A) Prime MMF Basin -> Fed ON RRP Buffer Sink ($361.88B remaining, 85% depleted)
        w_rrp = self.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=361.883e9,
            risk_friction=spread_friction * 0.4,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="us_prime_mmf_basin",
            target_id="fed_on_rrp_buffer_sink",
            relation="rrp_cash_parking",
            weight=w_rrp,
            rel_embedding=self.relation_embeddings["rrp_cash_parking"],
            metadata={"rrp_balance_usd": 361.883e9, "depletion_pct": 85.8, "tier_step": "3->3"},
        )

        # B) Triparty Repo -> US Treasury TGA -> Fed SOMA QT Burn Chamber (The literal money burn)
        w_repo_tga = self.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=984.046e9,
            risk_friction=spread_friction * 0.6,
            is_domestic_retention=True,
        )
        self.substrate.add_relation(
            source_id="us_triparty_repo_pool",
            target_id="us_treasury_tga",
            relation="tga_debt_issuance_absorption",
            weight=w_repo_tga,
            rel_embedding=self.relation_embeddings["tga_debt_issuance_absorption"],
            metadata={"tga_absorption_usd": 984.046e9, "tier_step": "2->3"},
        )

        w_qt_burn = self.compute_edge_weight(
            base_weight=1.20,
            flow_volume_eur=2156.969e9,
            risk_friction=spread_friction * 0.8,
            is_domestic_retention=True,
        )
        self.substrate.add_relation(
            source_id="us_treasury_tga",
            target_id="fed_soma_qt_burn_chamber",
            relation="qt_redemption_money_burn",
            weight=w_qt_burn,
            rel_embedding=self.relation_embeddings["qt_redemption_money_burn"],
            metadata={"cumulative_qt_burn_usd": 2156.969e9, "tier_step": "3->3"},
        )

        # C) Offshore FX Swap Desk -> London Eurodollar Pool -> Offshore Cayman Hedge Pool
        w_eurodollar = self.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=668.3e9,
            risk_friction=spread_friction * 1.2,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="offshore_fx_swap_desk",
            target_id="london_eurodollar_pool",
            relation="eurodollar_syndication",
            weight=w_eurodollar,
            rel_embedding=self.relation_embeddings["eurodollar_syndication"],
            metadata={"uk_eurodollar_holding_usd": 668.3e9, "tier_step": "1->2"},
        )

        w_cayman = self.compute_edge_weight(
            base_weight=1.15,
            flow_volume_eur=285.3e9,
            risk_friction=spread_friction * 1.4,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="london_eurodollar_pool",
            target_id="offshore_cayman_hedge_pool",
            relation="cayman_shadow_capital_flight",
            weight=w_cayman,
            rel_embedding=self.relation_embeddings["cayman_shadow_capital_flight"],
            metadata={"cayman_holding_usd": 285.3e9, "tier_step": "2->3"},
        )

        # D) Banque de France -> Fed/ECB Liquidity Swap Line -> Offshore FX Swap Desk
        w_emergency_swap = self.compute_edge_weight(
            base_weight=1.30,
            flow_volume_eur=207e6,
            risk_friction=spread_friction * 2.0,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="banque_de_france",
            target_id="fed_ecb_liquidity_swap_line",
            relation="emergency_fx_swap_activation",
            weight=w_emergency_swap,
            rel_embedding=self.relation_embeddings["emergency_fx_swap_activation"],
            metadata={"active_swaps_usd": 207e6, "emergency_valve": True, "tier_step": "1->1"},
        )
        self.substrate.add_relation(
            source_id="fed_ecb_liquidity_swap_line",
            target_id="offshore_fx_swap_desk",
            relation="central_bank_dollar_injection",
            weight=w_emergency_swap * 0.9,
            rel_embedding=self.relation_embeddings["central_bank_dollar_injection"],
            metadata={"dollar_injection": True, "tier_step": "1->1"},
        )

        # Corridor 7: The Global Liquidity Triangle (Transpacific Yen Carry, Corporate Buybacks, Petrodollars)
        # A) Japan Carry Faucet -> Japanese Institutional Desks -> US Triparty Repo
        w_jpy_faucet = self.compute_edge_weight(
            base_weight=0.90,
            flow_volume_eur=1104.4e9,
            risk_friction=0.10,  # Zero interest rate policy anchor
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="japan_mof_boj_carry_faucet",
            target_id="japan_institutional_carry_desk",
            relation="jpy_zero_interest_liquidity_provision",
            weight=w_jpy_faucet,
            rel_embedding=self.relation_embeddings["jpy_zero_interest_liquidity_provision"],
            metadata={"japan_tic_usd": 1104.4e9, "tier_step": "0->1"},
        )

        w_yen_carry = self.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=800.0e9,
            risk_friction=spread_friction * 0.9,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="japan_institutional_carry_desk",
            target_id="us_triparty_repo_pool",
            relation="yen_carry_dollar_treasury_absorption",
            weight=w_yen_carry,
            rel_embedding=self.relation_embeddings["yen_carry_dollar_treasury_absorption"],
            metadata={"fx_carry_usd": 800.0e9, "tier_step": "1->2"},
        )

        # B) Corporate Cash Flow & Buyback Burn:
        # Prime MMF Basin -> Apple Treasury Vault -> Corporate Share Buyback Burn Chamber
        # And Real Economy Exporters -> Apple Treasury Vault
        w_corp_paper = self.compute_edge_weight(
            base_weight=0.95,
            flow_volume_eur=62.4e9,
            risk_friction=0.20,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="us_prime_mmf_basin",
            target_id="apple_bigtech_treasury_vault",
            relation="corporate_commercial_paper_and_t_bill_placement",
            weight=w_corp_paper,
            rel_embedding=self.relation_embeddings["corporate_commercial_paper_and_t_bill_placement"],
            metadata={"liquid_hoard_usd": 62.4e9, "tier_step": "3->3"},
        )

        w_tech_inflow = self.compute_edge_weight(
            base_weight=1.00,
            flow_volume_eur=100.0e9,
            risk_friction=0.30,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="foreign_export_economies",
            target_id="apple_bigtech_treasury_vault",
            relation="global_enterprise_tech_inflow",
            weight=w_tech_inflow,
            rel_embedding=self.relation_embeddings["global_enterprise_tech_inflow"],
            metadata={"enterprise_tech_sales_usd": 100.0e9, "tier_step": "3->3"},
        )

        w_buyback_burn = self.compute_edge_weight(
            base_weight=1.15,
            flow_volume_eur=62.094e9,
            risk_friction=0.25,
            is_domestic_retention=True,
        )
        self.substrate.add_relation(
            source_id="apple_bigtech_treasury_vault",
            target_id="corporate_share_buyback_burn_chamber",
            relation="equity_share_retirement_buyback_burn",
            weight=w_buyback_burn,
            rel_embedding=self.relation_embeddings["equity_share_retirement_buyback_burn"],
            metadata={"apple_buybacks_usd": 62.094e9, "tier_step": "3->3"},
        )

        # C) Petrodollar Recycling Loop:
        # Exporters -> Gulf Petrodollar Basin -> SVT Dealers
        w_petro_accum = self.compute_edge_weight(
            base_weight=0.95,
            flow_volume_eur=85.0e9,
            risk_friction=0.20,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="foreign_export_economies",
            target_id="gulf_petrodollar_sovereign_wealth_basin",
            relation="petrodollar_energy_surplus_accumulation",
            weight=w_petro_accum,
            rel_embedding=self.relation_embeddings["petrodollar_energy_surplus_accumulation"],
            metadata={"petrodollar_recycling_usd": 85.0e9, "tier_step": "3->3"},
        )

        w_petro_recycle = self.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=40.0e9,
            risk_friction=spread_friction * 1.1,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="gulf_petrodollar_sovereign_wealth_basin",
            target_id="svt_dealers_bnp_socgen",
            relation="sovereign_wealth_oat_diversification",
            weight=w_petro_recycle,
            rel_embedding=self.relation_embeddings["sovereign_wealth_oat_diversification"],
            metadata={"oat_diversification_usd": 40.0e9, "tier_step": "3->1"},
        )

        # Corridor 8: The Planetary Monetary Manifold (7 Global Macro Regions)
        # A) Sino-Gulf Petro-Yuan Bilateral Clearing Corridor:
        w_py_invoice = self.compute_edge_weight(
            base_weight=0.90,
            flow_volume_eur=65.0e9,
            risk_friction=0.15,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="saudi_sama_pif_nexus",
            target_id="petro_yuan_bilateral_settlement_bridge",
            relation="petro_yuan_crude_invoicing",
            weight=w_py_invoice,
            rel_embedding=self.relation_embeddings["petro_yuan_crude_invoicing"],
            metadata={"petro_yuan_crude_usd": 65.0e9, "tier_step": "3->1"},
        )

        w_cnh_settle = self.compute_edge_weight(
            base_weight=0.85,
            flow_volume_eur=65.0e9,
            risk_friction=0.15,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="petro_yuan_bilateral_settlement_bridge",
            target_id="offshore_cnh_hong_kong_hub",
            relation="cnh_cross_border_liquidity_settlement",
            weight=w_cnh_settle,
            rel_embedding=self.relation_embeddings["cnh_cross_border_liquidity_settlement"],
            metadata={"cnh_clearing_usd": 65.0e9, "tier_step": "1->2"},
        )

        w_cnh_repatriate = self.compute_edge_weight(
            base_weight=0.85,
            flow_volume_eur=250.0e9,
            risk_friction=0.10,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="offshore_cnh_hong_kong_hub",
            target_id="chinese_state_banks_fx_desk",
            relation="onshore_offshore_cnh_repatriation",
            weight=w_cnh_repatriate,
            rel_embedding=self.relation_embeddings["onshore_offshore_cnh_repatriation"],
            metadata={"cnh_turnover_usd": 250.0e9, "tier_step": "2->1"},
        )

        w_pboc_accum = self.compute_edge_weight(
            base_weight=0.80,
            flow_volume_eur=859.4e9,
            risk_friction=0.10,
            is_domestic_retention=True,
        )
        self.substrate.add_relation(
            source_id="chinese_state_banks_fx_desk",
            target_id="pboc_safe_foreign_reserves",
            relation="sovereign_fx_reserve_accumulation",
            weight=w_pboc_accum,
            rel_embedding=self.relation_embeddings["sovereign_fx_reserve_accumulation"],
            metadata={"pboc_reserves_usd": 3240.0e9, "tier_step": "1->0"},
        )

        self.substrate.add_relation(
            source_id="petro_yuan_bilateral_settlement_bridge",
            target_id="chinese_state_banks_fx_desk",
            relation="direct_petro_yuan_clearing",
            weight=w_cnh_settle * 1.05,
            rel_embedding=self.relation_embeddings["direct_petro_yuan_clearing"],
            metadata={"direct_clearing": True, "tier_step": "1->1"},
        )

        # B) Shadow Energy Refining Loop:
        w_shadow_export = self.compute_edge_weight(
            base_weight=1.15,
            flow_volume_eur=140.0e9,
            risk_friction=0.40,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="bank_of_russia_cbr_vault",
            target_id="shadow_tanker_energy_arbitrage",
            relation="shadow_tanker_crude_export",
            weight=w_shadow_export,
            rel_embedding=self.relation_embeddings["shadow_tanker_crude_export"],
            metadata={"urals_crude_usd": 140.0e9, "tier_step": "0->1"},
        )

        w_refining_intake = self.compute_edge_weight(
            base_weight=0.90,
            flow_volume_eur=55.0e9,
            risk_friction=0.20,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="shadow_tanker_energy_arbitrage",
            target_id="reserve_bank_of_india_refining_hub",
            relation="discounted_crude_refining_intake",
            weight=w_refining_intake,
            rel_embedding=self.relation_embeddings["discounted_crude_refining_intake"],
            metadata={"refining_margin_usd": 55.0e9, "tier_step": "1->1"},
        )

        w_diesel_reexport = self.compute_edge_weight(
            base_weight=0.95,
            flow_volume_eur=55.0e9,
            risk_friction=0.25,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="reserve_bank_of_india_refining_hub",
            target_id="french_economy_importers",
            relation="refined_diesel_european_reexport",
            weight=w_diesel_reexport,
            rel_embedding=self.relation_embeddings["refined_diesel_european_reexport"],
            metadata={"refined_fuel_usd": 55.0e9, "tier_step": "1->3"},
        )

        self.substrate.add_relation(
            source_id="reserve_bank_of_india_refining_hub",
            target_id="foreign_export_economies",
            relation="global_product_fuel_distribution",
            weight=w_diesel_reexport * 1.05,
            rel_embedding=self.relation_embeddings["global_product_fuel_distribution"],
            metadata={"fuel_distribution": True, "tier_step": "1->3"},
        )

        # C) Pacific Hardware & Commodity Loop:
        w_aus_settle = self.compute_edge_weight(
            base_weight=0.90,
            flow_volume_eur=180.0e9,
            risk_friction=0.15,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="reserve_bank_of_australia_commodity_faucet",
            target_id="chinese_state_banks_fx_desk",
            relation="australian_iron_ore_lng_settlement",
            weight=w_aus_settle,
            rel_embedding=self.relation_embeddings["australian_iron_ore_lng_settlement"],
            metadata={"australia_commodity_usd": 180.0e9, "tier_step": "0->1"},
        )

        w_brazil_settle = self.compute_edge_weight(
            base_weight=0.90,
            flow_volume_eur=110.0e9,
            risk_friction=0.15,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="brazil_banco_central_agri_faucet",
            target_id="chinese_state_banks_fx_desk",
            relation="brazilian_agri_resource_settlement",
            weight=w_brazil_settle,
            rel_embedding=self.relation_embeddings["brazilian_agri_resource_settlement"],
            metadata={"brazil_agri_usd": 110.0e9, "tier_step": "0->1"},
        )

        w_cross_strait = self.compute_edge_weight(
            base_weight=0.95,
            flow_volume_eur=120.0e9,
            risk_friction=0.20,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="chinese_state_banks_fx_desk",
            target_id="taiwan_central_bank_tsmc_semiconductor_sink",
            relation="cross_strait_electronics_demand",
            weight=w_cross_strait,
            rel_embedding=self.relation_embeddings["cross_strait_electronics_demand"],
            metadata={"cross_strait_trade_usd": 120.0e9, "tier_step": "1->3"},
        )

        w_tsmc_hardware = self.compute_edge_weight(
            base_weight=0.90,
            flow_volume_eur=120.0e9,
            risk_friction=0.15,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="taiwan_central_bank_tsmc_semiconductor_sink",
            target_id="apple_bigtech_treasury_vault",
            relation="advanced_semiconductor_hardware_shipment",
            weight=w_tsmc_hardware,
            rel_embedding=self.relation_embeddings["advanced_semiconductor_hardware_shipment"],
            metadata={"semiconductor_hardware_usd": 120.0e9, "tier_step": "3->3"},
        )

        # D) African Critical Minerals & Debt Servicing:
        w_africa_debt = self.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=45.0e9,
            risk_friction=0.30,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="africa_critical_minerals_debt_conduit",
            target_id="chinese_state_banks_fx_desk",
            relation="resource_concession_debt_servicing",
            weight=w_africa_debt,
            rel_embedding=self.relation_embeddings["resource_concession_debt_servicing"],
            metadata={"mineral_debt_service_usd": 45.0e9, "tier_step": "1->1"},
        )

        self.substrate.add_relation(
            source_id="pboc_safe_foreign_reserves",
            target_id="africa_critical_minerals_debt_conduit",
            relation="belt_and_road_infrastructure_lending",
            weight=w_africa_debt * 0.95,
            rel_embedding=self.relation_embeddings["belt_and_road_infrastructure_lending"],
            metadata={"belt_and_road_lending_usd": 45.0e9, "tier_step": "0->1"},
        )

        # E) UAE Sovereign Wealth & Immobilized Russian Claim:
        w_uae_placement = self.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=50.0e9,
            risk_friction=spread_friction * 1.1,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="uae_adia_mubadala_basin",
            target_id="svt_dealers_bnp_socgen",
            relation="gulf_sovereign_euro_debt_placement",
            weight=w_uae_placement,
            rel_embedding=self.relation_embeddings["gulf_sovereign_euro_debt_placement"],
            metadata={"uae_placement_usd": 50.0e9, "tier_step": "3->1"},
        )

        self.substrate.add_relation(
            source_id="saudi_sama_pif_nexus",
            target_id="svt_dealers_bnp_socgen",
            relation="saudi_capital_diversification_oat",
            weight=w_uae_placement * 1.05,
            rel_embedding=self.relation_embeddings["saudi_capital_diversification_oat"],
            metadata={"saudi_diversification_usd": 40.0e9, "tier_step": "3->1"},
        )

        w_frozen = self.compute_edge_weight(
            base_weight=2.50,
            flow_volume_eur=300.0e9,
            risk_friction=3.5,
            is_domestic_retention=False,
        )
        self.substrate.add_relation(
            source_id="bank_of_russia_cbr_vault",
            target_id="eurosystem_target2_pool",
            relation="immobilized_euroclear_reserve_claim",
            weight=w_frozen,
            rel_embedding=self.relation_embeddings["immobilized_euroclear_reserve_claim"],
            metadata={"frozen_reserves_usd": 300.0e9, "tier_step": "0->2"},
        )

        # ---------------------------------------------------------------------
        # CORRIDOR 9: Phase 3 SPOF Mitigation & Dark Matter Architecture
        # ---------------------------------------------------------------------
        # A) DTCC FICC Sponsored Repo & Fed SRF Backstop (Mitigating us_triparty_repo_pool SPOF)
        w_ficc_sponsored = self.compute_edge_weight(
            base_weight=1.04,
            flow_volume_eur=1200.0e9,
            risk_friction=0.08,
            is_domestic_retention=False,
            velocity_turnover_days=1.0,
        )
        self.substrate.add_relation(
            source_id="japan_institutional_carry_desk",
            target_id="ficc_sponsored_repo_clearing",
            relation="sponsored_repo_clearing_injection",
            weight=w_ficc_sponsored * 1.05,
            rel_embedding=self.relation_embeddings["sponsored_repo_clearing_injection"],
            metadata={"bypass": True, "sponsored_repo_volume_usd": 800.0e9, "tier_step": "1->1"},
        )
        self.substrate.add_relation(
            source_id="offshore_fx_swap_desk",
            target_id="ficc_sponsored_repo_clearing",
            relation="fx_swap_sponsored_repo_conduit",
            weight=w_ficc_sponsored * 1.08,
            rel_embedding=self.relation_embeddings["fx_swap_sponsored_repo_conduit"],
            metadata={"bypass": True, "sponsored_repo_volume_usd": 250.0e9, "tier_step": "1->1"},
        )
        self.substrate.add_relation(
            source_id="us_prime_mmf_basin",
            target_id="ficc_sponsored_repo_clearing",
            relation="sponsored_repo_clearing_injection",
            weight=w_ficc_sponsored * 1.02,
            rel_embedding=self.relation_embeddings["sponsored_repo_clearing_injection"],
            metadata={"bypass": True, "sponsored_repo_volume_usd": 150.0e9, "tier_step": "1->1"},
        )
        self.substrate.add_relation(
            source_id="ficc_sponsored_repo_clearing",
            target_id="us_treasuries_custody",
            relation="sponsored_dvp_repo_settlement",
            weight=w_ficc_sponsored * 0.98,
            rel_embedding=self.relation_embeddings["sponsored_dvp_repo_settlement"],
            metadata={"bypass": True, "dvp_clearing_usd": 1200.0e9, "tier_step": "1->2"},
        )
        self.substrate.add_relation(
            source_id="ficc_sponsored_repo_clearing",
            target_id="us_treasury_tga",
            relation="sponsored_dvp_repo_settlement",
            weight=w_ficc_sponsored,
            rel_embedding=self.relation_embeddings["sponsored_dvp_repo_settlement"],
            metadata={"bypass": True, "dvp_clearing_usd": 1200.0e9, "tier_step": "1->3"},
        )
        w_srf = self.compute_edge_weight(
            base_weight=1.12,
            flow_volume_eur=500.0e9,
            risk_friction=0.05,
            is_domestic_retention=False,
            velocity_turnover_days=1.0,
        )
        self.substrate.add_relation(
            source_id="fed_standing_repo_facility",
            target_id="us_treasury_tga",
            relation="srf_backstop_liquidity_injection",
            weight=w_srf,
            rel_embedding=self.relation_embeddings["srf_backstop_liquidity_injection"],
            metadata={"srf_capacity_usd": 500.0e9, "tier_step": "1->3"},
        )

        # B) Crédit Agricole CIB & Natixis Dealer Syndicate Bypass (Mitigating svt_dealers_bnp_socgen SPOF)
        w_syndicate = self.compute_edge_weight(
            base_weight=1.00,
            flow_volume_eur=35.0e9,
            risk_friction=spread_friction * 1.20,
            is_domestic_retention=False,
            velocity_turnover_days=30.0,
        )
        self.substrate.add_relation(
            source_id="french_republic_tresor",
            target_id="ca_cib_natixis_dealer_syndicate",
            relation="oat_secondary_syndication_auction",
            weight=w_syndicate,
            rel_embedding=self.relation_embeddings["oat_secondary_syndication_auction"],
            metadata={"bypass": True, "syndicate_volume_eur": 35.0e9, "tier_step": "0->1"},
        )
        self.substrate.add_relation(
            source_id="ca_cib_natixis_dealer_syndicate",
            target_id="banque_de_france",
            relation="syndicate_reserve_clearing",
            weight=w_syndicate * 0.95,
            rel_embedding=self.relation_embeddings["syndicate_reserve_clearing"],
            metadata={"bypass": True, "tier_step": "1->1"},
        )
        self.substrate.add_relation(
            source_id="ca_cib_natixis_dealer_syndicate",
            target_id="offshore_fx_swap_desk",
            relation="syndicate_usd_fx_swap",
            weight=w_syndicate * 1.05,
            rel_embedding=self.relation_embeddings["syndicate_usd_fx_swap"],
            metadata={"bypass": True, "tier_step": "1->1"},
        )
        self.substrate.add_relation(
            source_id="ca_cib_natixis_dealer_syndicate",
            target_id="french_republic_oat_market",
            relation="secondary_market_distribution",
            weight=w_syndicate * 1.05,
            rel_embedding=self.relation_embeddings["secondary_market_distribution"],
            metadata={"bypass": True, "tier_step": "1->0"},
        )

        # C) Dark Matter Entities Wiring
        w_dark_matter = self.compute_edge_weight(
            base_weight=1.00,
            flow_volume_eur=800.0e9,
            risk_friction=0.15,
            is_domestic_retention=False,
            velocity_turnover_days=1.0,
        )
        self.substrate.add_relation(
            source_id="dtcc_treasury_basis_trade_clearing",
            target_id="us_treasuries_custody",
            relation="basis_trade_leverage_absorption",
            weight=w_dark_matter,
            rel_embedding=self.relation_embeddings["basis_trade_leverage_absorption"],
            metadata={"dark_matter_usd": 800.0e9, "tier_step": "1->2"},
        )
        w_bis = self.compute_edge_weight(
            base_weight=1.05,
            flow_volume_eur=25000.0e9,
            risk_friction=0.10,
            is_domestic_retention=False,
            velocity_turnover_days=90.0,
        )
        self.substrate.add_relation(
            source_id="bis_otc_derivatives_pool",
            target_id="offshore_fx_swap_desk",
            relation="otc_derivatives_collateral_drain",
            weight=w_bis,
            rel_embedding=self.relation_embeddings["otc_derivatives_collateral_drain"],
            metadata={"dark_matter_usd": 25000.0e9, "tier_step": "2->1"},
        )
        w_pboc_swap = self.compute_edge_weight(
            base_weight=1.08,
            flow_volume_eur=550.0e9,
            risk_friction=0.18,
            is_domestic_retention=False,
            velocity_turnover_days=365.0,
        )
        self.substrate.add_relation(
            source_id="pboc_safe_foreign_reserves",
            target_id="pboc_bilateral_swap_network",
            relation="pboc_bilateral_swap_activation",
            weight=w_pboc_swap,
            rel_embedding=self.relation_embeddings["pboc_bilateral_swap_activation"],
            metadata={"dark_matter_usd": 550.0e9, "tier_step": "0->1"},
        )
        w_imf_eo = self.compute_edge_weight(
            base_weight=1.10,
            flow_volume_eur=175.0e9,
            risk_friction=0.25,
            is_domestic_retention=False,
            velocity_turnover_days=365.0,
        )
        self.substrate.add_relation(
            source_id="imf_errors_and_omissions_pool",
            target_id="us_triparty_repo_pool",
            relation="imf_errors_and_omissions_absorption",
            weight=w_imf_eo,
            rel_embedding=self.relation_embeddings["imf_errors_and_omissions_absorption"],
            metadata={"dark_matter_usd": 175.0e9, "tier_step": "3->2"},
        )

    def initialize_landmarks(self) -> None:
        """Builds coarse landmark clusters strictly aligned with the 4 monetary tiers."""
        lm = self.engine.landmark_graph
        sub = self.substrate
        lm.num_clusters = 4
        lm.cluster_to_entities.clear()
        lm.entity_to_cluster.clear()

        # Group entities strictly by monetary tier
        tier_embeddings = {0: [], 1: [], 2: [], 3: []}
        for eid, meta in FINANCIAL_ENTITIES.items():
            if eid not in sub.entities:
                continue
            tier_int = int(meta["tier"])
            emb = sub.entities[eid].embedding
            tier_embeddings[tier_int].append(emb)
            lm.entity_to_cluster[eid] = tier_int
            lm.cluster_to_entities[tier_int].add(eid)
            sub.entities[eid].cluster_id = tier_int

        # Calculate unit-normalized centroid per monetary tier
        lm.centroids = np.zeros((4, self.node_dim), dtype=np.float32)
        for t in range(4):
            embs = np.array(tier_embeddings[t], dtype=np.float32)
            mean_v = np.mean(embs, axis=0)
            lm.centroids[t] = mean_v / (np.linalg.norm(mean_v) + 1e-9)

        # Build coarse adjacency from substrate relationships
        lm.cluster_adjacency.clear()
        for src_id, targets in sub.adjacency.items():
            src_cluster = lm.entity_to_cluster.get(src_id)
            if src_cluster is None:
                continue
            for tgt_id in targets.keys():
                tgt_cluster = lm.entity_to_cluster.get(tgt_id)
                if tgt_cluster is not None:
                    lm.cluster_adjacency[src_cluster].add(tgt_cluster)
                    lm.cluster_adjacency[tgt_cluster].add(src_cluster)

        logger.info(
            f"Initialized Global Landmark Graph with {lm.num_clusters} tier-aligned clusters. "
            f"Adjacency: {dict(lm.cluster_adjacency)}"
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
        tgt_cayman = "offshore_cayman_hedge_pool"
        tgt_burn = "fed_soma_qt_burn_chamber"

        res_t2 = self.materialize_liquidity_path(src, tgt_t2)
        res_bund = self.materialize_liquidity_path(src, tgt_bund)
        res_trade = self.materialize_liquidity_path(src, tgt_trade)
        res_mmf = self.materialize_liquidity_path(src, tgt_mmf)
        res_cayman = self.materialize_liquidity_path(src, tgt_cayman)
        res_burn = self.materialize_liquidity_path(tgt_mmf, tgt_burn)
        res_carry = self.materialize_liquidity_path("japan_mof_boj_carry_faucet", "us_treasury_tga")
        res_buyback = self.materialize_liquidity_path(src, "corporate_share_buyback_burn_chamber")
        res_petro = self.materialize_liquidity_path(src, "gulf_petrodollar_sovereign_wealth_basin")
        # Planetary Corridors
        res_petroyuan = self.materialize_liquidity_path("saudi_sama_pif_nexus", "pboc_safe_foreign_reserves")
        res_shadow_energy = self.materialize_liquidity_path("bank_of_russia_cbr_vault", "french_economy_importers")
        res_pacific_loop = self.materialize_liquidity_path("reserve_bank_of_australia_commodity_faucet", "corporate_share_buyback_burn_chamber")

        all_bridge_entities = set()
        for res in [res_t2, res_bund, res_trade, res_mmf, res_cayman, res_burn, res_carry, res_buyback, res_petro, res_petroyuan, res_shadow_energy, res_pacific_loop]:
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
            "cayman_capital_flight_reachability": res_cayman.success,
            "qt_money_burn_reachability": res_burn.success,
            "transpacific_carry_reachability": res_carry.success,
            "corporate_buyback_reachability": res_buyback.success,
            "petrodollar_reachability": res_petro.success,
            "petro_yuan_sino_gulf_reachability": res_petroyuan.success,
            "shadow_energy_refining_reachability": res_shadow_energy.success,
            "pacific_hardware_commodity_reachability": res_pacific_loop.success,
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
                "cayman_offshore_capital_flight": {
                    "success": res_cayman.success,
                    "nodes": res_cayman.path_nodes,
                    "edges": [e.relation for e in res_cayman.path_edges],
                    "total_cost": res_cayman.total_cost,
                    "iterations": res_cayman.iterations,
                    "expanded_nodes": res_cayman.expanded_nodes,
                },
                "fed_soma_qt_money_burn": {
                    "success": res_burn.success,
                    "nodes": res_burn.path_nodes,
                    "edges": [e.relation for e in res_burn.path_edges],
                    "total_cost": res_burn.total_cost,
                    "iterations": res_burn.iterations,
                    "expanded_nodes": res_burn.expanded_nodes,
                },
                "transpacific_yen_carry": {
                    "success": res_carry.success,
                    "nodes": res_carry.path_nodes,
                    "edges": [e.relation for e in res_carry.path_edges],
                    "total_cost": res_carry.total_cost,
                    "iterations": res_carry.iterations,
                    "expanded_nodes": res_carry.expanded_nodes,
                },
                "corporate_share_buyback_burn": {
                    "success": res_buyback.success,
                    "nodes": res_buyback.path_nodes,
                    "edges": [e.relation for e in res_buyback.path_edges],
                    "total_cost": res_buyback.total_cost,
                    "iterations": res_buyback.iterations,
                    "expanded_nodes": res_buyback.expanded_nodes,
                },
                "petrodollar_recycling_loop": {
                    "success": res_petro.success,
                    "nodes": res_petro.path_nodes,
                    "edges": [e.relation for e in res_petro.path_edges],
                    "total_cost": res_petro.total_cost,
                    "iterations": res_petro.iterations,
                    "expanded_nodes": res_petro.expanded_nodes,
                },
                "petro_yuan_sino_gulf": {
                    "success": res_petroyuan.success,
                    "nodes": res_petroyuan.path_nodes,
                    "edges": [e.relation for e in res_petroyuan.path_edges],
                    "total_cost": res_petroyuan.total_cost,
                    "iterations": res_petroyuan.iterations,
                    "expanded_nodes": res_petroyuan.expanded_nodes,
                },
                "shadow_energy_refining_loop": {
                    "success": res_shadow_energy.success,
                    "nodes": res_shadow_energy.path_nodes,
                    "edges": [e.relation for e in res_shadow_energy.path_edges],
                    "total_cost": res_shadow_energy.total_cost,
                    "iterations": res_shadow_energy.iterations,
                    "expanded_nodes": res_shadow_energy.expanded_nodes,
                },
                "pacific_hardware_commodity_loop": {
                    "success": res_pacific_loop.success,
                    "nodes": res_pacific_loop.path_nodes,
                    "edges": [e.relation for e in res_pacific_loop.path_edges],
                    "total_cost": res_pacific_loop.total_cost,
                    "iterations": res_pacific_loop.iterations,
                    "expanded_nodes": res_pacific_loop.expanded_nodes,
                },
            },
            "bridge_entities": sorted(list(all_bridge_entities)),
            "buffer_stats": telemetry,
            "macro_stress": self.stress_snapshot.model_dump() if self.stress_snapshot else {},
            "invariants_verified": all(invariants.values()),
            "invariant_details": invariants,
        }
