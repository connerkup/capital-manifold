"""Adversarial and Negative Control Substrate Generator.

Constructs an 80+ node high-dimensional financial balance-sheet network:
1. Authentic Agence France Trésor (AFT) SVT Primary Dealer registry (15 banks).
2. 65+ Decoy/Distractor entities across 5 deceptive categories:
   - Regional retail savings banks & credit unions (large assets, retail focus, NO SVT mandate).
   - Municipal utilities & state-backed corporates (high French state ownership, NO interbank clearing).
   - Real estate SCPIs & domestic property funds (superficial French domestic exposure).
   - Retail mortgage brokers & consumer fintechs (sub-clearing credit conduits).
   - Empty offshore SPVs & unregulated funds (superficial cross-border tags, disconnected from RTGS).
3. 16 continuous normalized balance-sheet metrics projected into unit-norm d=128
   via continuous harmonic multi-frequency projection (no manual coordinate slicing).
4. Strictly governed institutional balance-sheet mechanics (no handcoded shortcuts).
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from pgm_engine.engine import ProceduralGraphEngine
from pgm_engine.memory.l3_substrate import L3LatentSubstrate
from pgm_engine.types import EdgeRelation, EntityNode

logger = logging.getLogger("capital_manifold.adversarial")


class EntityCategory(str, Enum):
    SOVEREIGN_ISSUER = "sovereign_issuer"
    CENTRAL_BANK = "central_bank"
    SVT_PRIMARY_DEALER = "svt_primary_dealer"
    INTERBANK_CLEARING = "interbank_clearing"
    SAFE_HAVEN_ANCHOR = "safe_haven_anchor"
    REAL_ECONOMY_TRADE = "real_economy_trade"
    DECOY_REGIONAL_SAVINGS = "decoy_regional_savings"
    DECOY_MUNICIPAL_UTILITY = "decoy_municipal_utility"
    DECOY_REAL_ESTATE_SCPI = "decoy_real_estate_scpi"
    DECOY_CONSUMER_FINTECH = "decoy_consumer_fintech"
    DECOY_OFFSHORE_SPV = "decoy_offshore_spv"
    DARK_FOREST_TRANSATLANTIC = "dark_forest_transatlantic"
    DARK_FOREST_RING2 = "dark_forest_ring2"
    GLOBAL_TRIANGLE = "global_triangle"
    PLANETARY_MANIFOLD = "planetary_manifold"


@dataclass
class BalanceSheetMetrics:
    """16 continuous normalized balance-sheet fundamentals for financial institutions."""
    log_total_assets: float             # Log10(Assets EUR) / 13.0 (0.0 to 1.0)
    leverage_ratio: float               # Tier 1 Capital / Total Assets (0.02 to 0.30)
    cash_reserves_ratio: float          # Cash & Central Bank Reserves / Assets (0.001 to 0.40)
    svt_dealer_mandate: float           # 1.0 if official AFT primary dealer license, 0.0 otherwise
    target2_direct_participant: float   # 1.0 if direct RTGS participant with reserve account, 0.0 otherwise
    wholesale_repo_volume: float        # Normalized interbank repo trading capacity (0.0 to 1.0)
    cross_border_liability_ratio: float # Ratio of foreign/cross-border claims (0.0 to 1.0)
    duration_sensitivity: float         # Sensitivity to OAT/Bund yield curves (0.0 to 1.5)
    state_ownership_pct: float          # Direct French Republic / public equity (0.0 to 1.0)
    npl_ratio: float                    # Non-performing loan ratio (0.005 to 0.20)
    deposit_funded_ratio: float         # Proportion of retail deposits in liabilities (0.0 to 0.95)
    interbank_lending_ratio: float      # Interbank assets / total balance sheet (0.0 to 0.50)
    trade_finance_exposure: float       # Letters of credit / commercial trade finance (0.0 to 1.0)
    sovereign_holding_ratio: float      # Sovereign debt stock / assets (0.0 to 0.60)
    central_bank_refi_access: float     # 1.0 if access to Eurosystem MRO/LTRO refi, 0.0 otherwise
    regulatory_tier_rank: float         # 1.0: G-SIB / Sovereign, 0.6: O-SII, 0.1: Unregulated

    def to_vector(self) -> np.ndarray:
        return np.array([
            self.log_total_assets,
            self.leverage_ratio,
            self.cash_reserves_ratio,
            self.svt_dealer_mandate,
            self.target2_direct_participant,
            self.wholesale_repo_volume,
            self.cross_border_liability_ratio,
            self.duration_sensitivity,
            self.state_ownership_pct,
            self.npl_ratio,
            self.deposit_funded_ratio,
            self.interbank_lending_ratio,
            self.trade_finance_exposure,
            self.sovereign_holding_ratio,
            self.central_bank_refi_access,
            self.regulatory_tier_rank,
        ], dtype=np.float32)


class HarmonicBalanceSheetProjector:
    """Continuous Multi-Frequency Harmonic Projector: maps R^16 fundamentals to unit-norm R^128.

    Eliminates manual coordinate slicing. Distance mathematically reflects institutional
    balance-sheet topology:
        z = [sin(W^T x + B), cos(W^T x + B)] / ||z||_2
    """

    def __init__(self, in_features: int = 16, out_dim: int = 128, frequency_scale: float = 6.0, seed: int = 42):
        self.in_features = in_features
        self.out_dim = out_dim
        self.frequency_scale = frequency_scale
        half_dim = out_dim // 2
        rng = np.random.RandomState(seed)
        # Orthonormal Gaussian frequency projection: shape (in_features, half_dim)
        W_raw = rng.randn(half_dim, in_features).astype(np.float32)
        q, _ = np.linalg.qr(W_raw)
        self.W = q.T.astype(np.float32)  # Shape: (in_features, half_dim)
        self.B = (rng.uniform(0.0, 2.0 * math.pi, size=half_dim)).astype(np.float32)

    def project(self, x: np.ndarray) -> np.ndarray:
        """Projects continuous 16-d fundamentals into unit-norm 128-d latent vector."""
        linear = self.frequency_scale * np.dot(x, self.W) + self.B
        z_sin = np.sin(linear)
        z_cos = np.cos(linear)
        z = np.concatenate([z_sin, z_cos], axis=0).astype(np.float32)
        norm = np.linalg.norm(z)
        if norm > 1e-9:
            z /= norm
        return z


class AdversarialSubstrateBuilder:
    """Builds a realistic 80+ node balance sheet network containing authentic AFT SVTs and deceptive decoys."""

    def __init__(self, node_dim: int = 128, rel_dim: int = 32, seed: int = 42):
        self.node_dim = node_dim
        self.rel_dim = rel_dim
        self.projector = HarmonicBalanceSheetProjector(in_features=16, out_dim=node_dim, seed=seed)
        self.entity_metrics: Dict[str, BalanceSheetMetrics] = {}
        self.entity_categories: Dict[str, EntityCategory] = {}
        self.relation_embeddings: Dict[str, np.ndarray] = {}
        self._init_relation_embeddings()

    def _init_relation_embeddings(self) -> None:
        """Generates normalized 32-d relation embeddings for institutional edge types."""
        rel_types = [
            "oat_primary_issuance",
            "secondary_market_distribution",
            "dealer_reserve_clearing",
            "target2_liability_drain",
            "target2_claim_accumulation",
            "safe_haven_monetary_sink",
            "spread_friction_flight",
            "fiscal_stimulus_import_demand",
            "trade_deficit_drain",
            "trade_surplus_repatriation",
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
            "global_enterprise_tech_inflow",
            "equity_share_retirement_buyback_burn",
            "petrodollar_energy_surplus_accumulation",
            "sovereign_wealth_oat_diversification",
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
            "retail_mortgage_amortization_recirculation",
            "instant_credit_repayment_recirculation",
            "social_housing_rent_recirculation",
            "fx_swap_sponsored_repo_conduit",
            # Decoy edge types
            "retail_deposit_aggregation",
            "utility_corporate_financing",
            "property_mortgage_syndication",
            "fintech_loan_brokering",
            "offshore_subordinated_transfer",
        ]
        for idx, r_name in enumerate(rel_types):
            vec = np.zeros(self.rel_dim, dtype=np.float32)
            slot = (idx * 2) % self.rel_dim
            vec[slot] = 1.0
            vec[(slot + 1) % self.rel_dim] = 0.5
            for k in range(self.rel_dim):
                vec[k] += 0.2 * math.cos(2.0 * math.pi * (idx + 1) * (k + 1) / self.rel_dim)
            norm = np.linalg.norm(vec)
            if norm > 1e-9:
                vec /= norm
            self.relation_embeddings[r_name] = vec

    def _register(self, eid: str, cat: EntityCategory, metrics: BalanceSheetMetrics) -> None:
        self.entity_metrics[eid] = metrics
        self.entity_categories[eid] = cat

    def _define_entities(self) -> None:
        """Instantiates authentic core nodes and 65+ decoys across 5 deceptive categories."""

        # 1. Core Sovereign & Central Banking Nodes
        self._register("french_republic_tresor", EntityCategory.SOVEREIGN_ISSUER, BalanceSheetMetrics(
            log_total_assets=0.98, leverage_ratio=0.04, cash_reserves_ratio=0.08, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.90, cross_border_liability_ratio=0.55,
            duration_sensitivity=1.40, state_ownership_pct=1.00, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.05, trade_finance_exposure=0.10, sovereign_holding_ratio=0.00,
            central_bank_refi_access=0.0, regulatory_tier_rank=1.0,
        ))
        self._register("french_republic_oat_market", EntityCategory.SOVEREIGN_ISSUER, BalanceSheetMetrics(
            log_total_assets=0.95, leverage_ratio=0.05, cash_reserves_ratio=0.05, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.85, cross_border_liability_ratio=0.50,
            duration_sensitivity=1.50, state_ownership_pct=0.90, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.10, trade_finance_exposure=0.05, sovereign_holding_ratio=0.45,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.95,
        ))
        self._register("banque_de_france", EntityCategory.CENTRAL_BANK, BalanceSheetMetrics(
            log_total_assets=0.96, leverage_ratio=0.03, cash_reserves_ratio=0.40, svt_dealer_mandate=0.0,
            target2_direct_participant=1.0, wholesale_repo_volume=0.95, cross_border_liability_ratio=0.75,
            duration_sensitivity=0.60, state_ownership_pct=1.00, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.40, trade_finance_exposure=0.05, sovereign_holding_ratio=0.35,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))
        self._register("eurosystem_target2_pool", EntityCategory.INTERBANK_CLEARING, BalanceSheetMetrics(
            log_total_assets=0.99, leverage_ratio=0.02, cash_reserves_ratio=0.35, svt_dealer_mandate=0.0,
            target2_direct_participant=1.0, wholesale_repo_volume=0.90, cross_border_liability_ratio=0.95,
            duration_sensitivity=0.20, state_ownership_pct=0.80, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.50, trade_finance_exposure=0.20, sovereign_holding_ratio=0.10,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))
        self._register("bundesbank", EntityCategory.CENTRAL_BANK, BalanceSheetMetrics(
            log_total_assets=0.97, leverage_ratio=0.03, cash_reserves_ratio=0.38, svt_dealer_mandate=0.0,
            target2_direct_participant=1.0, wholesale_repo_volume=0.95, cross_border_liability_ratio=0.80,
            duration_sensitivity=0.50, state_ownership_pct=1.00, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.40, trade_finance_exposure=0.10, sovereign_holding_ratio=0.30,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))
        self._register("bund_risk_free_anchor", EntityCategory.SAFE_HAVEN_ANCHOR, BalanceSheetMetrics(
            log_total_assets=0.98, leverage_ratio=0.06, cash_reserves_ratio=0.10, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.90, cross_border_liability_ratio=0.85,
            duration_sensitivity=1.35, state_ownership_pct=1.00, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.05, trade_finance_exposure=0.05, sovereign_holding_ratio=0.00,
            central_bank_refi_access=0.0, regulatory_tier_rank=1.0,
        ))
        self._register("french_economy_importers", EntityCategory.REAL_ECONOMY_TRADE, BalanceSheetMetrics(
            log_total_assets=0.82, leverage_ratio=0.15, cash_reserves_ratio=0.05, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.20, cross_border_liability_ratio=0.60,
            duration_sensitivity=0.10, state_ownership_pct=0.10, npl_ratio=0.02, deposit_funded_ratio=0.10,
            interbank_lending_ratio=0.02, trade_finance_exposure=0.85, sovereign_holding_ratio=0.02,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.40,
        ))
        self._register("foreign_export_economies", EntityCategory.REAL_ECONOMY_TRADE, BalanceSheetMetrics(
            log_total_assets=0.88, leverage_ratio=0.18, cash_reserves_ratio=0.08, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.30, cross_border_liability_ratio=0.75,
            duration_sensitivity=0.10, state_ownership_pct=0.05, npl_ratio=0.015, deposit_funded_ratio=0.15,
            interbank_lending_ratio=0.05, trade_finance_exposure=0.90, sovereign_holding_ratio=0.05,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.50,
        ))
        self._register("sovereign_debt_holders", EntityCategory.SAFE_HAVEN_ANCHOR, BalanceSheetMetrics(
            log_total_assets=0.92, leverage_ratio=0.12, cash_reserves_ratio=0.04, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.60, cross_border_liability_ratio=0.45,
            duration_sensitivity=1.20, state_ownership_pct=0.00, npl_ratio=0.01, deposit_funded_ratio=0.05,
            interbank_lending_ratio=0.10, trade_finance_exposure=0.05, sovereign_holding_ratio=0.55,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.70,
        ))

        # 2. Authentic Agence France Trésor (AFT) SVT Primary Dealers (15 major banks)
        aft_svts = [
            ("svt_bnp_paribas", 0.94, 0.045, 0.16, 0.92),
            ("svt_societe_generale", 0.92, 0.043, 0.14, 0.90),
            ("svt_credit_agricole_cib", 0.93, 0.048, 0.15, 0.88),
            ("svt_natixis_bpce", 0.91, 0.051, 0.13, 0.85),
            ("svt_deutsche_bank_paris", 0.92, 0.042, 0.14, 0.89),
            ("svt_barclays_france", 0.90, 0.044, 0.12, 0.84),
            ("svt_citigroup_markets", 0.91, 0.047, 0.15, 0.87),
            ("svt_goldman_sachs_paris", 0.90, 0.052, 0.14, 0.86),
            ("svt_morgan_stanley_europe", 0.89, 0.050, 0.13, 0.85),
            ("svt_hsbc_continental_europe", 0.89, 0.046, 0.12, 0.82),
            ("svt_jpmorgan_se", 0.92, 0.049, 0.16, 0.91),
            ("svt_bofa_europe", 0.90, 0.048, 0.14, 0.86),
            ("svt_nomura_europe", 0.86, 0.054, 0.11, 0.80),
            ("svt_santander", 0.91, 0.046, 0.13, 0.83),
            ("svt_ubs_europe", 0.90, 0.047, 0.14, 0.85),
        ]
        for eid, log_a, lev, cash, repo in aft_svts:
            self._register(eid, EntityCategory.SVT_PRIMARY_DEALER, BalanceSheetMetrics(
                log_total_assets=log_a, leverage_ratio=lev, cash_reserves_ratio=cash,
                svt_dealer_mandate=1.0,           # Licensed SVT
                target2_direct_participant=1.0,   # Direct TARGET2 RTGS participant
                wholesale_repo_volume=repo, cross_border_liability_ratio=0.65,
                duration_sensitivity=1.10, state_ownership_pct=0.00, npl_ratio=0.015,
                deposit_funded_ratio=0.35, interbank_lending_ratio=0.30, trade_finance_exposure=0.25,
                sovereign_holding_ratio=0.22, central_bank_refi_access=1.0, regulatory_tier_rank=0.90,
            ))

        # 3. Decoys Category A: Regional retail savings banks & credit unions (15 entities)
        # Deception: Massive assets (€40B-€150B), French jurisdiction, high deposit volume,
        # BUT strictly NO primary dealer mandate, no market-making in sovereign auctions.
        regional_banks = [
            "caisse_epargne_idf", "caisse_epargne_rhone_alpes", "caisse_epargne_bretagne",
            "banque_populaire_rives_paris", "banque_populaire_aura", "banque_populaire_alsace",
            "credit_agricole_idf_regional", "credit_agricole_nord_de_france", "credit_agricole_aquitaine",
            "credit_agricole_centre_est", "credit_mutuel_arkea", "credit_mutuel_nord_europe",
            "credit_mutuel_dauphine", "banque_postale_retail", "credit_cooperatif_regional",
        ]
        for idx, eid in enumerate(regional_banks):
            self._register(eid, EntityCategory.DECOY_REGIONAL_SAVINGS, BalanceSheetMetrics(
                log_total_assets=0.86 + (idx % 5) * 0.015, leverage_ratio=0.075, cash_reserves_ratio=0.05,
                svt_dealer_mandate=0.0,           # NO SVT LICENSE
                target2_direct_participant=0.0,   # Settles indirectly via parent central bodies
                wholesale_repo_volume=0.15, cross_border_liability_ratio=0.05,
                duration_sensitivity=0.30, state_ownership_pct=0.00, npl_ratio=0.025,
                deposit_funded_ratio=0.85, interbank_lending_ratio=0.08, trade_finance_exposure=0.05,
                sovereign_holding_ratio=0.06, central_bank_refi_access=0.0, regulatory_tier_rank=0.55,
            ))

        # 4. Decoys Category B: Municipal utilities & state-backed corporates (15 entities)
        # Deception: Extreme state ownership (100%), massive asset footprint, high correlation with French state,
        # BUT commercial corporations, completely disconnected from interbank RTGS clearing.
        municipal_utilities = [
            "edf_electricite_de_france", "sncf_reseau_transport", "sncf_voyageurs", "ratp_transport_paris",
            "eau_de_paris_municipal", "aeroports_de_paris_group", "la_poste_groupe_corporate",
            "engie_energy_holding", "cea_nucleaire_recherche", "bpi_france_regions",
            "voies_navigables_france", "societe_du_grand_paris", "grand_port_marseille",
            "semapa_amenagement_paris", "paris_habitat_hlm",
        ]
        for idx, eid in enumerate(municipal_utilities):
            self._register(eid, EntityCategory.DECOY_MUNICIPAL_UTILITY, BalanceSheetMetrics(
                log_total_assets=0.88 + (idx % 6) * 0.015, leverage_ratio=0.18, cash_reserves_ratio=0.02,
                svt_dealer_mandate=0.0,           # NON-BANK CORPORATE
                target2_direct_participant=0.0,   # NO RTGS ACCESS
                wholesale_repo_volume=0.05, cross_border_liability_ratio=0.15,
                duration_sensitivity=0.25, state_ownership_pct=0.85 + (idx % 4) * 0.05,
                npl_ratio=0.01, deposit_funded_ratio=0.00, interbank_lending_ratio=0.00,
                trade_finance_exposure=0.40, sovereign_holding_ratio=0.00, central_bank_refi_access=0.0,
                regulatory_tier_rank=0.45,
            ))

        # 5. Decoys Category C: Real estate SCPIs & domestic property funds (12 entities)
        # Deception: Superficial French domestic asset tags, real asset yield exposure,
        # completely outside the banking circuit.
        property_funds = [
            "scpi_primovie_fonciere", "scpi_immorente_commerciale", "scpi_corum_origin_fonciere",
            "scpi_epargne_pierre_retail", "scpi_rivoli_avenir_patrimoine", "scpi_pf_grand_paris",
            "opci_diversipierre_fund", "fonciere_des_regions_holding", "gecina_reit_paris",
            "klepierre_retail_property", "unibail_rodamco_corporate", "covivio_real_estate",
        ]
        for idx, eid in enumerate(property_funds):
            self._register(eid, EntityCategory.DECOY_REAL_ESTATE_SCPI, BalanceSheetMetrics(
                log_total_assets=0.74 + (idx % 4) * 0.02, leverage_ratio=0.45, cash_reserves_ratio=0.01,
                svt_dealer_mandate=0.0, target2_direct_participant=0.0, wholesale_repo_volume=0.00,
                cross_border_liability_ratio=0.10, duration_sensitivity=0.40, state_ownership_pct=0.00,
                npl_ratio=0.01, deposit_funded_ratio=0.00, interbank_lending_ratio=0.00,
                trade_finance_exposure=0.00, sovereign_holding_ratio=0.00, central_bank_refi_access=0.0,
                regulatory_tier_rank=0.25,
            ))

        # 6. Decoys Category D: Retail mortgage brokers & consumer fintechs (12 entities)
        # Deception: Active consumer loan originators, retail credit tech, low cash buffers.
        fintechs = [
            "meilleurtaux_courtage_broker", "pretto_digital_mortgage", "cafpi_credit_immobilier",
            "younited_credit_consumer", "floa_bank_instant_credit", "cofidis_france_consumer",
            "cetelem_france_retail", "sofinco_credit_conso", "franco_suisse_courtage",
            "finfrog_micro_credit", "lynk_payment_fintech", "lydia_solutions_fintech",
        ]
        for idx, eid in enumerate(fintechs):
            self._register(eid, EntityCategory.DECOY_CONSUMER_FINTECH, BalanceSheetMetrics(
                log_total_assets=0.68 + (idx % 4) * 0.02, leverage_ratio=0.15, cash_reserves_ratio=0.02,
                svt_dealer_mandate=0.0, target2_direct_participant=0.0, wholesale_repo_volume=0.05,
                cross_border_liability_ratio=0.05, duration_sensitivity=0.10, state_ownership_pct=0.00,
                npl_ratio=0.04, deposit_funded_ratio=0.20, interbank_lending_ratio=0.00,
                trade_finance_exposure=0.00, sovereign_holding_ratio=0.00, central_bank_refi_access=0.0,
                regulatory_tier_rank=0.30,
            ))

        # 7. Decoys Category E: Empty offshore SPVs & unregulated funds (12 entities)
        # Deception: Superficial cross-border tags, Cayman/Luxembourg flags, hedge tags,
        # but zero access to central bank reserves and disconnected from TARGET2.
        offshore_spvs = [
            "lux_spv_capital_alpha", "lux_spv_sovereign_yield_beta", "cayman_macro_opportunistic_fund",
            "jersey_conduit_finance_spv", "dublin_structured_investments_spv", "delaware_treasury_arbitrage_llc",
            "panama_global_arbitrage_fund", "malta_european_yield_sicav", "curacao_reinvestment_spv",
            "cyprus_merchant_holdings_spv", "marshall_islands_maritime_fund", "gibraltar_crossborder_spv",
        ]
        for idx, eid in enumerate(offshore_spvs):
            self._register(eid, EntityCategory.DECOY_OFFSHORE_SPV, BalanceSheetMetrics(
                log_total_assets=0.60 + (idx % 5) * 0.03, leverage_ratio=0.60, cash_reserves_ratio=0.005,
                svt_dealer_mandate=0.0, target2_direct_participant=0.0, wholesale_repo_volume=0.10,
                cross_border_liability_ratio=0.90, duration_sensitivity=0.20, state_ownership_pct=0.00,
                npl_ratio=0.08, deposit_funded_ratio=0.00, interbank_lending_ratio=0.00,
                trade_finance_exposure=0.10, sovereign_holding_ratio=0.05, central_bank_refi_access=0.0,
                regulatory_tier_rank=0.10,
            ))

        # 8. Dark Forest Ring 1: Transatlantic Dollar Conduit & Repo Nexus (4 nodes)
        self._register("offshore_fx_swap_desk", EntityCategory.DARK_FOREST_TRANSATLANTIC, BalanceSheetMetrics(
            log_total_assets=0.90, leverage_ratio=0.04, cash_reserves_ratio=0.06, svt_dealer_mandate=0.0,
            target2_direct_participant=1.0, wholesale_repo_volume=0.95, cross_border_liability_ratio=0.95,
            duration_sensitivity=0.80, state_ownership_pct=0.00, npl_ratio=0.015, deposit_funded_ratio=0.10,
            interbank_lending_ratio=0.35, trade_finance_exposure=0.30, sovereign_holding_ratio=0.20,
            central_bank_refi_access=1.0, regulatory_tier_rank=0.90,
        ))
        self._register("us_triparty_repo_pool", EntityCategory.DARK_FOREST_TRANSATLANTIC, BalanceSheetMetrics(
            log_total_assets=0.99, leverage_ratio=0.02, cash_reserves_ratio=0.20, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=1.00, cross_border_liability_ratio=0.70,
            duration_sensitivity=0.20, state_ownership_pct=0.00, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.50, trade_finance_exposure=0.20, sovereign_holding_ratio=0.10,
            central_bank_refi_access=0.0, regulatory_tier_rank=1.0,
        ))
        self._register("us_prime_mmf_basin", EntityCategory.DARK_FOREST_TRANSATLANTIC, BalanceSheetMetrics(
            log_total_assets=0.97, leverage_ratio=0.95, cash_reserves_ratio=0.30, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.90, cross_border_liability_ratio=0.40,
            duration_sensitivity=0.10, state_ownership_pct=0.00, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.00, trade_finance_exposure=0.05, sovereign_holding_ratio=0.15,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.80,
        ))
        self._register("us_treasury_tga", EntityCategory.DARK_FOREST_TRANSATLANTIC, BalanceSheetMetrics(
            log_total_assets=0.92, leverage_ratio=0.05, cash_reserves_ratio=0.90, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.00, cross_border_liability_ratio=0.20,
            duration_sensitivity=0.50, state_ownership_pct=1.00, npl_ratio=0.005, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.00, trade_finance_exposure=0.00, sovereign_holding_ratio=0.00,
            central_bank_refi_access=0.0, regulatory_tier_rank=1.0,
        ))

        # 9. Dark Forest Ring 2: The QT Burn Chamber, Evaporating RRP Buffer, and Offshore Eurodollar Sinks (5 nodes)
        self._register("fed_soma_qt_burn_chamber", EntityCategory.DARK_FOREST_RING2, BalanceSheetMetrics(
            log_total_assets=0.98, leverage_ratio=0.01, cash_reserves_ratio=0.01, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.00, cross_border_liability_ratio=0.10,
            duration_sensitivity=0.90, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.00, trade_finance_exposure=0.00, sovereign_holding_ratio=0.95,
            central_bank_refi_access=0.0, regulatory_tier_rank=1.0,
        ))
        self._register("fed_on_rrp_buffer_sink", EntityCategory.DARK_FOREST_RING2, BalanceSheetMetrics(
            log_total_assets=0.95, leverage_ratio=0.01, cash_reserves_ratio=0.90, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.85, cross_border_liability_ratio=0.10,
            duration_sensitivity=0.01, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.00, trade_finance_exposure=0.00, sovereign_holding_ratio=0.90,
            central_bank_refi_access=0.0, regulatory_tier_rank=1.0,
        ))
        self._register("offshore_cayman_hedge_pool", EntityCategory.DARK_FOREST_RING2, BalanceSheetMetrics(
            log_total_assets=0.88, leverage_ratio=0.20, cash_reserves_ratio=0.15, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.90, cross_border_liability_ratio=0.95,
            duration_sensitivity=0.75, state_ownership_pct=0.00, npl_ratio=0.020, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.20, trade_finance_exposure=0.00, sovereign_holding_ratio=0.35,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.40,
        ))
        self._register("london_eurodollar_pool", EntityCategory.DARK_FOREST_RING2, BalanceSheetMetrics(
            log_total_assets=0.92, leverage_ratio=0.05, cash_reserves_ratio=0.20, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.95, cross_border_liability_ratio=0.90,
            duration_sensitivity=0.50, state_ownership_pct=0.00, npl_ratio=0.010, deposit_funded_ratio=0.20,
            interbank_lending_ratio=0.60, trade_finance_exposure=0.40, sovereign_holding_ratio=0.40,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.85,
        ))
        self._register("fed_ecb_liquidity_swap_line", EntityCategory.DARK_FOREST_RING2, BalanceSheetMetrics(
            log_total_assets=0.90, leverage_ratio=0.01, cash_reserves_ratio=0.80, svt_dealer_mandate=0.0,
            target2_direct_participant=1.0, wholesale_repo_volume=0.50, cross_border_liability_ratio=0.99,
            duration_sensitivity=0.10, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.90, trade_finance_exposure=0.00, sovereign_holding_ratio=0.00,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))

        # 10. Global Liquidity Triangle: Yen Carry, Corporate Buyback Sink, Petrodollar Recycling (5 nodes)
        self._register("japan_mof_boj_carry_faucet", EntityCategory.GLOBAL_TRIANGLE, BalanceSheetMetrics(
            log_total_assets=0.99, leverage_ratio=0.01, cash_reserves_ratio=0.50, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.90, cross_border_liability_ratio=0.85,
            duration_sensitivity=0.80, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.70, trade_finance_exposure=0.00, sovereign_holding_ratio=0.99,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))
        self._register("japan_institutional_carry_desk", EntityCategory.GLOBAL_TRIANGLE, BalanceSheetMetrics(
            log_total_assets=0.94, leverage_ratio=0.04, cash_reserves_ratio=0.15, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.95, cross_border_liability_ratio=0.90,
            duration_sensitivity=0.70, state_ownership_pct=0.10, npl_ratio=0.008, deposit_funded_ratio=0.40,
            interbank_lending_ratio=0.50, trade_finance_exposure=0.10, sovereign_holding_ratio=0.60,
            central_bank_refi_access=1.0, regulatory_tier_rank=0.85,
        ))
        self._register("apple_bigtech_treasury_vault", EntityCategory.GLOBAL_TRIANGLE, BalanceSheetMetrics(
            log_total_assets=0.86, leverage_ratio=0.30, cash_reserves_ratio=0.40, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.40, cross_border_liability_ratio=0.60,
            duration_sensitivity=0.15, state_ownership_pct=0.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.00, trade_finance_exposure=0.10, sovereign_holding_ratio=0.30,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.70,
        ))
        self._register("corporate_share_buyback_burn_chamber", EntityCategory.GLOBAL_TRIANGLE, BalanceSheetMetrics(
            log_total_assets=0.85, leverage_ratio=0.01, cash_reserves_ratio=0.01, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.00, cross_border_liability_ratio=0.10,
            duration_sensitivity=0.00, state_ownership_pct=0.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.00, trade_finance_exposure=0.00, sovereign_holding_ratio=0.00,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.50,
        ))
        self._register("gulf_petrodollar_sovereign_wealth_basin", EntityCategory.GLOBAL_TRIANGLE, BalanceSheetMetrics(
            log_total_assets=0.96, leverage_ratio=0.90, cash_reserves_ratio=0.35, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.70, cross_border_liability_ratio=0.95,
            duration_sensitivity=0.40, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.20, trade_finance_exposure=0.30, sovereign_holding_ratio=0.50,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.95,
        ))

        # 11. Planetary Monetary Manifold (7 Global Regions) (13 nodes)
        self._register("pboc_safe_foreign_reserves", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=1.00, leverage_ratio=0.01, cash_reserves_ratio=0.85, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.80, cross_border_liability_ratio=0.80,
            duration_sensitivity=0.60, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.40, trade_finance_exposure=0.20, sovereign_holding_ratio=0.95,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))
        self._register("chinese_state_banks_fx_desk", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.99, leverage_ratio=0.08, cash_reserves_ratio=0.15, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.95, cross_border_liability_ratio=0.70,
            duration_sensitivity=0.40, state_ownership_pct=0.90, npl_ratio=0.012, deposit_funded_ratio=0.65,
            interbank_lending_ratio=0.30, trade_finance_exposure=0.60, sovereign_holding_ratio=0.45,
            central_bank_refi_access=1.0, regulatory_tier_rank=0.95,
        ))
        self._register("offshore_cnh_hong_kong_hub", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.92, leverage_ratio=0.06, cash_reserves_ratio=0.25, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.90, cross_border_liability_ratio=0.95,
            duration_sensitivity=0.30, state_ownership_pct=0.30, npl_ratio=0.005, deposit_funded_ratio=0.30,
            interbank_lending_ratio=0.50, trade_finance_exposure=0.50, sovereign_holding_ratio=0.35,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.85,
        ))
        self._register("taiwan_central_bank_tsmc_semiconductor_sink", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.90, leverage_ratio=0.35, cash_reserves_ratio=0.45, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.30, cross_border_liability_ratio=0.85,
            duration_sensitivity=0.10, state_ownership_pct=0.10, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.05, trade_finance_exposure=0.70, sovereign_holding_ratio=0.40,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.80,
        ))
        self._register("saudi_sama_pif_nexus", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.97, leverage_ratio=0.85, cash_reserves_ratio=0.40, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.60, cross_border_liability_ratio=0.90,
            duration_sensitivity=0.35, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.15, trade_finance_exposure=0.40, sovereign_holding_ratio=0.50,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.95,
        ))
        self._register("uae_adia_mubadala_basin", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.98, leverage_ratio=0.90, cash_reserves_ratio=0.35, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.70, cross_border_liability_ratio=0.95,
            duration_sensitivity=0.40, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.20, trade_finance_exposure=0.30, sovereign_holding_ratio=0.50,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.95,
        ))
        self._register("petro_yuan_bilateral_settlement_bridge", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.88, leverage_ratio=0.05, cash_reserves_ratio=0.30, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.80, cross_border_liability_ratio=0.95,
            duration_sensitivity=0.20, state_ownership_pct=0.50, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.40, trade_finance_exposure=0.90, sovereign_holding_ratio=0.20,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.80,
        ))
        self._register("bank_of_russia_cbr_vault", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.95, leverage_ratio=0.01, cash_reserves_ratio=0.90, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.10, cross_border_liability_ratio=0.60,
            duration_sensitivity=0.70, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.10, trade_finance_exposure=0.10, sovereign_holding_ratio=0.85,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))
        self._register("shadow_tanker_energy_arbitrage", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.87, leverage_ratio=0.15, cash_reserves_ratio=0.10, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.50, cross_border_liability_ratio=0.99,
            duration_sensitivity=0.15, state_ownership_pct=0.20, npl_ratio=0.020, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.05, trade_finance_exposure=0.95, sovereign_holding_ratio=0.05,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.40,
        ))
        self._register("brazil_banco_central_agri_faucet", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.92, leverage_ratio=0.02, cash_reserves_ratio=0.60, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.50, cross_border_liability_ratio=0.70,
            duration_sensitivity=0.50, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.20, trade_finance_exposure=0.40, sovereign_holding_ratio=0.75,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))
        self._register("reserve_bank_of_australia_commodity_faucet", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.93, leverage_ratio=0.02, cash_reserves_ratio=0.65, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.60, cross_border_liability_ratio=0.80,
            duration_sensitivity=0.45, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.25, trade_finance_exposure=0.50, sovereign_holding_ratio=0.80,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.0,
        ))
        self._register("reserve_bank_of_india_refining_hub", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.94, leverage_ratio=0.06, cash_reserves_ratio=0.45, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.70, cross_border_liability_ratio=0.75,
            duration_sensitivity=0.35, state_ownership_pct=0.60, npl_ratio=0.010, deposit_funded_ratio=0.20,
            interbank_lending_ratio=0.20, trade_finance_exposure=0.80, sovereign_holding_ratio=0.60,
            central_bank_refi_access=1.0, regulatory_tier_rank=0.90,
        ))
        self._register("africa_critical_minerals_debt_conduit", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.82, leverage_ratio=0.20, cash_reserves_ratio=0.05, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.20, cross_border_liability_ratio=0.90,
            duration_sensitivity=0.25, state_ownership_pct=0.40, npl_ratio=0.050, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.00, trade_finance_exposure=0.85, sovereign_holding_ratio=0.10,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.40,
        ))
        # Phase 3 Topology Resilience & Dark Matter Entities
        self._register("ficc_sponsored_repo_clearing", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.98, leverage_ratio=0.01, cash_reserves_ratio=0.20, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.99, cross_border_liability_ratio=0.85,
            duration_sensitivity=0.10, state_ownership_pct=0.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.95, trade_finance_exposure=0.10, sovereign_holding_ratio=0.95,
            central_bank_refi_access=1.0, regulatory_tier_rank=0.98,
        ))
        self._register("fed_standing_repo_facility", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.96, leverage_ratio=0.00, cash_reserves_ratio=0.95, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.95, cross_border_liability_ratio=0.50,
            duration_sensitivity=0.05, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.90, trade_finance_exposure=0.00, sovereign_holding_ratio=1.00,
            central_bank_refi_access=1.0, regulatory_tier_rank=1.00,
        ))
        self._register("ca_cib_natixis_dealer_syndicate", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.95, leverage_ratio=0.05, cash_reserves_ratio=0.35, svt_dealer_mandate=0.9,
            target2_direct_participant=1.0, wholesale_repo_volume=0.88, cross_border_liability_ratio=0.75,
            duration_sensitivity=0.45, state_ownership_pct=0.05, npl_ratio=0.012, deposit_funded_ratio=0.45,
            interbank_lending_ratio=0.60, trade_finance_exposure=0.55, sovereign_holding_ratio=0.80,
            central_bank_refi_access=1.0, regulatory_tier_rank=0.95,
        ))
        self._register("bis_otc_derivatives_pool", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=1.00, leverage_ratio=0.15, cash_reserves_ratio=0.10, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.95, cross_border_liability_ratio=0.95,
            duration_sensitivity=0.90, state_ownership_pct=0.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.85, trade_finance_exposure=0.70, sovereign_holding_ratio=0.60,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.80,
        ))
        self._register("dtcc_treasury_basis_trade_clearing", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.95, leverage_ratio=0.25, cash_reserves_ratio=0.05, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.98, cross_border_liability_ratio=0.60,
            duration_sensitivity=0.85, state_ownership_pct=0.00, npl_ratio=0.001, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.90, trade_finance_exposure=0.10, sovereign_holding_ratio=0.95,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.75,
        ))
        self._register("pboc_bilateral_swap_network", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.94, leverage_ratio=0.01, cash_reserves_ratio=0.70, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.40, cross_border_liability_ratio=0.85,
            duration_sensitivity=0.20, state_ownership_pct=1.00, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.75, trade_finance_exposure=0.90, sovereign_holding_ratio=0.80,
            central_bank_refi_access=1.0, regulatory_tier_rank=0.95,
        ))
        self._register("imf_errors_and_omissions_pool", EntityCategory.PLANETARY_MANIFOLD, BalanceSheetMetrics(
            log_total_assets=0.88, leverage_ratio=0.00, cash_reserves_ratio=0.50, svt_dealer_mandate=0.0,
            target2_direct_participant=0.0, wholesale_repo_volume=0.10, cross_border_liability_ratio=0.99,
            duration_sensitivity=0.10, state_ownership_pct=0.50, npl_ratio=0.000, deposit_funded_ratio=0.00,
            interbank_lending_ratio=0.10, trade_finance_exposure=0.90, sovereign_holding_ratio=0.50,
            central_bank_refi_access=0.0, regulatory_tier_rank=0.50,
        ))

    def build_adversarial_substrate(self) -> Tuple[L3LatentSubstrate, Dict[str, BalanceSheetMetrics]]:
        """Constructs L3 substrate with 80+ entities and dynamically synthesized institutional edges."""
        self._define_entities()
        sub = L3LatentSubstrate(node_dim=self.node_dim, rel_dim=self.rel_dim)

        # 1. Register all Entity Nodes with continuous harmonic embeddings
        for eid, metrics in self.entity_metrics.items():
            raw_v = metrics.to_vector()
            emb = self.projector.project(raw_v)
            sub.add_entity(
                entity_id=eid,
                embedding=emb,
                cluster_id=-1,
                metadata={
                    "category": self.entity_categories[eid].value,
                    "metrics": metrics.__dict__,
                },
            )

        # 2. Strict Institutional Edge Synthesis
        # A) Sovereign Primary Issuance: French Treasury -> Authentic AFT SVTs
        aft_dealers = [eid for eid, cat in self.entity_categories.items() if cat == EntityCategory.SVT_PRIMARY_DEALER]
        for svt_id in aft_dealers:
            sub.add_relation(
                source_id="french_republic_tresor",
                target_id=svt_id,
                relation="oat_primary_issuance",
                weight=1.15,
                rel_embedding=self.relation_embeddings["oat_primary_issuance"],
                metadata={"mandate_verified": True},
            )

        # Deceptive state funding edge to municipal utility (decoy trap for greedy search)
        sub.add_relation(
            source_id="french_republic_tresor",
            target_id="edf_electricite_de_france",
            relation="state_equity_endowment",
            weight=0.85,
            rel_embedding=self.relation_embeddings["utility_corporate_financing"],
            metadata={"is_decoy_distractor": True, "state_backed": True},
        )

        # B) SVT Dealers -> Central Bank Reserve Clearing & Secondary Market
        for svt_id in aft_dealers:
            sub.add_relation(
                source_id=svt_id,
                target_id="banque_de_france",
                relation="dealer_reserve_clearing",
                weight=1.10,
                rel_embedding=self.relation_embeddings["dealer_reserve_clearing"],
                metadata={"rtgs_participant": True},
            )
            sub.add_relation(
                source_id=svt_id,
                target_id="french_republic_oat_market",
                relation="secondary_market_distribution",
                weight=0.85,
                rel_embedding=self.relation_embeddings["secondary_market_distribution"],
            )

        # C) Interbank Cross-Border Settlement Corridor
        sub.add_relation(
            source_id="banque_de_france",
            target_id="eurosystem_target2_pool",
            relation="target2_liability_drain",
            weight=1.00,
            rel_embedding=self.relation_embeddings["target2_liability_drain"],
        )
        sub.add_relation(
            source_id="eurosystem_target2_pool",
            target_id="bundesbank",
            relation="target2_claim_accumulation",
            weight=1.00,
            rel_embedding=self.relation_embeddings["target2_claim_accumulation"],
        )
        sub.add_relation(
            source_id="bundesbank",
            target_id="bund_risk_free_anchor",
            relation="safe_haven_monetary_sink",
            weight=0.95,
            rel_embedding=self.relation_embeddings["safe_haven_monetary_sink"],
        )
        sub.add_relation(
            source_id="french_republic_oat_market",
            target_id="bund_risk_free_anchor",
            relation="spread_friction_flight",
            weight=1.25,
            rel_embedding=self.relation_embeddings["spread_friction_flight"],
        )

        # D) Real Economy Trade Bleed Corridor
        sub.add_relation(
            source_id="french_republic_tresor",
            target_id="french_economy_importers",
            relation="fiscal_stimulus_import_demand",
            weight=0.90,
            rel_embedding=self.relation_embeddings["fiscal_stimulus_import_demand"],
        )
        sub.add_relation(
            source_id="french_economy_importers",
            target_id="foreign_export_economies",
            relation="trade_deficit_drain",
            weight=1.00,
            rel_embedding=self.relation_embeddings["trade_deficit_drain"],
        )
        sub.add_relation(
            source_id="foreign_export_economies",
            target_id="bundesbank",
            relation="trade_surplus_repatriation",
            weight=0.95,
            rel_embedding=self.relation_embeddings["trade_surplus_repatriation"],
        )
        sub.add_relation(
            source_id="french_republic_oat_market",
            target_id="sovereign_debt_holders",
            relation="secondary_market_distribution",
            weight=0.80,
            rel_embedding=self.relation_embeddings["secondary_market_distribution"],
        )

        # E) Dark Forest Ring 1: Transatlantic Dollar Conduit & Repo Nexus
        for svt_id in aft_dealers:
            sub.add_relation(
                source_id=svt_id,
                target_id="offshore_fx_swap_desk",
                relation="synthetic_usd_fx_swap",
                weight=1.10,
                rel_embedding=self.relation_embeddings["synthetic_usd_fx_swap"],
                metadata={"transatlantic_conduit": True},
            )

        sub.add_relation(
            source_id="offshore_fx_swap_desk",
            target_id="us_triparty_repo_pool",
            relation="repo_dollar_financing",
            weight=1.05,
            rel_embedding=self.relation_embeddings["repo_dollar_financing"],
            metadata={"sofr_turnover_usd": 3007e9},
        )
        sub.add_relation(
            source_id="us_triparty_repo_pool",
            target_id="us_prime_mmf_basin",
            relation="repo_liquidity_absorption",
            weight=0.95,
            rel_embedding=self.relation_embeddings["repo_liquidity_absorption"],
            metadata={"prime_mmf_basin": True},
        )
        sub.add_relation(
            source_id="us_prime_mmf_basin",
            target_id="us_triparty_repo_pool",
            relation="mmf_cash_repo_lending",
            weight=0.95,
            rel_embedding=self.relation_embeddings["mmf_cash_repo_lending"],
        )
        sub.add_relation(
            source_id="us_treasury_tga",
            target_id="us_triparty_repo_pool",
            relation="tga_reserve_absorption_drain",
            weight=1.35,
            rel_embedding=self.relation_embeddings["tga_reserve_absorption_drain"],
            metadata={"tga_closing_usd": 883.335e9, "net_drain_usd": 12.154e9},
        )

        # F) Dark Forest Ring 2: QT Burn Chamber, Evaporating RRP Buffer, and Offshore Eurodollar Sinks
        sub.add_relation(
            source_id="us_prime_mmf_basin",
            target_id="fed_on_rrp_buffer_sink",
            relation="rrp_cash_parking",
            weight=1.05,
            rel_embedding=self.relation_embeddings["rrp_cash_parking"],
            metadata={"on_rrp_balance_usd": 361.883e9},
        )
        sub.add_relation(
            source_id="us_triparty_repo_pool",
            target_id="us_treasury_tga",
            relation="tga_debt_issuance_absorption",
            weight=1.10,
            rel_embedding=self.relation_embeddings["tga_debt_issuance_absorption"],
            metadata={"tga_absorption_usd": 984.046e9},
        )
        sub.add_relation(
            source_id="us_treasury_tga",
            target_id="fed_soma_qt_burn_chamber",
            relation="qt_redemption_money_burn",
            weight=1.20,
            rel_embedding=self.relation_embeddings["qt_redemption_money_burn"],
            metadata={"cumulative_qt_burn_usd": 2156.969e9},
        )
        sub.add_relation(
            source_id="offshore_fx_swap_desk",
            target_id="london_eurodollar_pool",
            relation="eurodollar_syndication",
            weight=1.10,
            rel_embedding=self.relation_embeddings["eurodollar_syndication"],
            metadata={"uk_eurodollar_holding_usd": 668.3e9},
        )
        sub.add_relation(
            source_id="london_eurodollar_pool",
            target_id="offshore_cayman_hedge_pool",
            relation="cayman_shadow_capital_flight",
            weight=1.15,
            rel_embedding=self.relation_embeddings["cayman_shadow_capital_flight"],
            metadata={"cayman_holding_usd": 285.3e9},
        )
        sub.add_relation(
            source_id="banque_de_france",
            target_id="fed_ecb_liquidity_swap_line",
            relation="emergency_fx_swap_activation",
            weight=1.30,
            rel_embedding=self.relation_embeddings["emergency_fx_swap_activation"],
            metadata={"active_swaps_usd": 207e6},
        )
        sub.add_relation(
            source_id="fed_ecb_liquidity_swap_line",
            target_id="offshore_fx_swap_desk",
            relation="central_bank_dollar_injection",
            weight=1.15,
            rel_embedding=self.relation_embeddings["central_bank_dollar_injection"],
            metadata={"emergency_valve": True},
        )

        # G) Global Liquidity Triangle: Yen Carry, Corporate Buybacks, Petrodollars
        sub.add_relation(
            source_id="japan_mof_boj_carry_faucet",
            target_id="japan_institutional_carry_desk",
            relation="jpy_zero_interest_liquidity_provision",
            weight=0.90,
            rel_embedding=self.relation_embeddings["jpy_zero_interest_liquidity_provision"],
            metadata={"japan_tic_usd": 1104.4e9},
        )
        sub.add_relation(
            source_id="japan_institutional_carry_desk",
            target_id="us_triparty_repo_pool",
            relation="yen_carry_dollar_treasury_absorption",
            weight=1.05,
            rel_embedding=self.relation_embeddings["yen_carry_dollar_treasury_absorption"],
            metadata={"fx_carry_usd": 800.0e9},
        )
        sub.add_relation(
            source_id="us_prime_mmf_basin",
            target_id="apple_bigtech_treasury_vault",
            relation="corporate_commercial_paper_and_t_bill_placement",
            weight=0.95,
            rel_embedding=self.relation_embeddings["corporate_commercial_paper_and_t_bill_placement"],
            metadata={"liquid_hoard_usd": 62.4e9},
        )
        sub.add_relation(
            source_id="foreign_export_economies",
            target_id="apple_bigtech_treasury_vault",
            relation="global_enterprise_tech_inflow",
            weight=1.00,
            rel_embedding=self.relation_embeddings["global_enterprise_tech_inflow"],
            metadata={"enterprise_sales_usd": 100.0e9},
        )
        sub.add_relation(
            source_id="apple_bigtech_treasury_vault",
            target_id="corporate_share_buyback_burn_chamber",
            relation="equity_share_retirement_buyback_burn",
            weight=1.15,
            rel_embedding=self.relation_embeddings["equity_share_retirement_buyback_burn"],
            metadata={"apple_buybacks_usd": 62.094e9},
        )
        sub.add_relation(
            source_id="foreign_export_economies",
            target_id="gulf_petrodollar_sovereign_wealth_basin",
            relation="petrodollar_energy_surplus_accumulation",
            weight=0.95,
            rel_embedding=self.relation_embeddings["petrodollar_energy_surplus_accumulation"],
            metadata={"petrodollar_recycling_usd": 85.0e9},
        )
        sub.add_relation(
            source_id="gulf_petrodollar_sovereign_wealth_basin",
            target_id="svt_dealers_bnp_socgen",
            relation="sovereign_wealth_oat_diversification",
            weight=1.10,
            rel_embedding=self.relation_embeddings["sovereign_wealth_oat_diversification"],
            metadata={"oat_diversification_usd": 40.0e9},
        )

        # H) Planetary Monetary Manifold (7 Global Macro Regions)
        # Petro-Yuan Bilateral Energy Clearing
        sub.add_relation(
            source_id="saudi_sama_pif_nexus",
            target_id="petro_yuan_bilateral_settlement_bridge",
            relation="petro_yuan_crude_invoicing",
            weight=0.90,
            rel_embedding=self.relation_embeddings["petro_yuan_crude_invoicing"],
            metadata={"petro_yuan_crude_usd": 65.0e9},
        )
        sub.add_relation(
            source_id="petro_yuan_bilateral_settlement_bridge",
            target_id="offshore_cnh_hong_kong_hub",
            relation="cnh_cross_border_liquidity_settlement",
            weight=0.85,
            rel_embedding=self.relation_embeddings["cnh_cross_border_liquidity_settlement"],
            metadata={"cnh_clearing_usd": 65.0e9},
        )
        sub.add_relation(
            source_id="offshore_cnh_hong_kong_hub",
            target_id="chinese_state_banks_fx_desk",
            relation="onshore_offshore_cnh_repatriation",
            weight=0.85,
            rel_embedding=self.relation_embeddings["onshore_offshore_cnh_repatriation"],
            metadata={"cnh_turnover_usd": 250.0e9},
        )
        sub.add_relation(
            source_id="chinese_state_banks_fx_desk",
            target_id="pboc_safe_foreign_reserves",
            relation="sovereign_fx_reserve_accumulation",
            weight=0.80,
            rel_embedding=self.relation_embeddings["sovereign_fx_reserve_accumulation"],
            metadata={"pboc_reserves_usd": 3240.0e9},
        )
        sub.add_relation(
            source_id="petro_yuan_bilateral_settlement_bridge",
            target_id="chinese_state_banks_fx_desk",
            relation="direct_petro_yuan_clearing",
            weight=0.90,
            rel_embedding=self.relation_embeddings["direct_petro_yuan_clearing"],
        )

        # Shadow Energy Refining Arbitrage
        sub.add_relation(
            source_id="bank_of_russia_cbr_vault",
            target_id="shadow_tanker_energy_arbitrage",
            relation="shadow_tanker_crude_export",
            weight=1.15,
            rel_embedding=self.relation_embeddings["shadow_tanker_crude_export"],
            metadata={"urals_crude_usd": 140.0e9},
        )
        sub.add_relation(
            source_id="shadow_tanker_energy_arbitrage",
            target_id="reserve_bank_of_india_refining_hub",
            relation="discounted_crude_refining_intake",
            weight=0.90,
            rel_embedding=self.relation_embeddings["discounted_crude_refining_intake"],
            metadata={"refining_margin_usd": 55.0e9},
        )
        sub.add_relation(
            source_id="reserve_bank_of_india_refining_hub",
            target_id="french_economy_importers",
            relation="refined_diesel_european_reexport",
            weight=0.95,
            rel_embedding=self.relation_embeddings["refined_diesel_european_reexport"],
            metadata={"refined_fuel_usd": 55.0e9},
        )
        sub.add_relation(
            source_id="reserve_bank_of_india_refining_hub",
            target_id="foreign_export_economies",
            relation="global_product_fuel_distribution",
            weight=1.00,
            rel_embedding=self.relation_embeddings["global_product_fuel_distribution"],
        )

        # Pacific Hardware & Commodity Loop
        sub.add_relation(
            source_id="reserve_bank_of_australia_commodity_faucet",
            target_id="chinese_state_banks_fx_desk",
            relation="australian_iron_ore_lng_settlement",
            weight=0.90,
            rel_embedding=self.relation_embeddings["australian_iron_ore_lng_settlement"],
            metadata={"australia_commodity_usd": 180.0e9},
        )
        sub.add_relation(
            source_id="brazil_banco_central_agri_faucet",
            target_id="chinese_state_banks_fx_desk",
            relation="brazilian_agri_resource_settlement",
            weight=0.90,
            rel_embedding=self.relation_embeddings["brazilian_agri_resource_settlement"],
            metadata={"brazil_agri_usd": 110.0e9},
        )
        sub.add_relation(
            source_id="chinese_state_banks_fx_desk",
            target_id="taiwan_central_bank_tsmc_semiconductor_sink",
            relation="cross_strait_electronics_demand",
            weight=0.95,
            rel_embedding=self.relation_embeddings["cross_strait_electronics_demand"],
            metadata={"cross_strait_trade_usd": 120.0e9},
        )
        sub.add_relation(
            source_id="taiwan_central_bank_tsmc_semiconductor_sink",
            target_id="apple_bigtech_treasury_vault",
            relation="advanced_semiconductor_hardware_shipment",
            weight=0.90,
            rel_embedding=self.relation_embeddings["advanced_semiconductor_hardware_shipment"],
            metadata={"semiconductor_hardware_usd": 120.0e9},
        )

        # African Concessions & Infrastructure Lending
        sub.add_relation(
            source_id="africa_critical_minerals_debt_conduit",
            target_id="chinese_state_banks_fx_desk",
            relation="resource_concession_debt_servicing",
            weight=1.05,
            rel_embedding=self.relation_embeddings["resource_concession_debt_servicing"],
            metadata={"mineral_debt_service_usd": 45.0e9},
        )
        sub.add_relation(
            source_id="pboc_safe_foreign_reserves",
            target_id="africa_critical_minerals_debt_conduit",
            relation="belt_and_road_infrastructure_lending",
            weight=1.00,
            rel_embedding=self.relation_embeddings["belt_and_road_infrastructure_lending"],
            metadata={"belt_and_road_lending_usd": 45.0e9},
        )

        # UAE Wealth & Frozen CBR Assets
        sub.add_relation(
            source_id="uae_adia_mubadala_basin",
            target_id="svt_dealers_bnp_socgen",
            relation="gulf_sovereign_euro_debt_placement",
            weight=1.10,
            rel_embedding=self.relation_embeddings["gulf_sovereign_euro_debt_placement"],
            metadata={"uae_placement_usd": 50.0e9},
        )
        sub.add_relation(
            source_id="saudi_sama_pif_nexus",
            target_id="svt_dealers_bnp_socgen",
            relation="saudi_capital_diversification_oat",
            weight=1.15,
            rel_embedding=self.relation_embeddings["saudi_capital_diversification_oat"],
            metadata={"saudi_diversification_usd": 40.0e9},
        )
        sub.add_relation(
            source_id="bank_of_russia_cbr_vault",
            target_id="eurosystem_target2_pool",
            relation="immobilized_euroclear_reserve_claim",
            weight=2.50,
            rel_embedding=self.relation_embeddings["immobilized_euroclear_reserve_claim"],
            metadata={"frozen_reserves_usd": 300.0e9},
        )

        # I) Deceptive Local Commercial Edges for Decoy Nodes
        # Regional banks connect to consumer fintechs (retail deposit aggregation)
        reg_banks = [eid for eid, cat in self.entity_categories.items() if cat == EntityCategory.DECOY_REGIONAL_SAVINGS]
        fintech_list = [eid for eid, cat in self.entity_categories.items() if cat == EntityCategory.DECOY_CONSUMER_FINTECH]
        for i, rb in enumerate(reg_banks):
            ft = fintech_list[i % len(fintech_list)]
            sub.add_relation(
                source_id=rb,
                target_id=ft,
                relation="retail_deposit_aggregation",
                weight=0.60,
                rel_embedding=self.relation_embeddings["retail_deposit_aggregation"],
            )

        # Municipal utilities connect among themselves and real economy corporate accounts
        utilities = [eid for eid, cat in self.entity_categories.items() if cat == EntityCategory.DECOY_MUNICIPAL_UTILITY]
        for i in range(len(utilities) - 1):
            sub.add_relation(
                source_id=utilities[i],
                target_id=utilities[i + 1],
                relation="utility_corporate_financing",
                weight=0.50,
                rel_embedding=self.relation_embeddings["utility_corporate_financing"],
            )

        # Property SCPIs connect to regional banks for mortgage financing
        scpis = [eid for eid, cat in self.entity_categories.items() if cat == EntityCategory.DECOY_REAL_ESTATE_SCPI]
        for i, sc in enumerate(scpis):
            rb = reg_banks[i % len(reg_banks)]
            sub.add_relation(
                source_id=sc,
                target_id=rb,
                relation="property_mortgage_syndication",
                weight=0.45,
                rel_embedding=self.relation_embeddings["property_mortgage_syndication"],
            )

        # Offshore SPVs form an isolated closed ring
        spvs = [eid for eid, cat in self.entity_categories.items() if cat == EntityCategory.DECOY_OFFSHORE_SPV]
        for i in range(len(spvs)):
            next_spv = spvs[(i + 1) % len(spvs)]
            sub.add_relation(
                source_id=spvs[i],
                target_id=next_spv,
                relation="offshore_subordinated_transfer",
                weight=0.30,
                rel_embedding=self.relation_embeddings["offshore_subordinated_transfer"],
            )

        # ---------------------------------------------------------------------
        # Phase 3 Topology Resilience & Dark Matter Architecture
        # ---------------------------------------------------------------------
        # DTCC FICC Sponsored Repo & Fed SRF Backstop (Mitigating us_triparty_repo_pool SPOF)
        sub.add_relation(
            source_id="japan_institutional_carry_desk",
            target_id="ficc_sponsored_repo_clearing",
            relation="sponsored_repo_clearing_injection",
            weight=1.05,
            rel_embedding=self.relation_embeddings["sponsored_repo_clearing_injection"],
        )
        sub.add_relation(
            source_id="offshore_fx_swap_desk",
            target_id="ficc_sponsored_repo_clearing",
            relation="fx_swap_sponsored_repo_conduit",
            weight=1.08,
            rel_embedding=self.relation_embeddings["fx_swap_sponsored_repo_conduit"],
        )
        sub.add_relation(
            source_id="ficc_sponsored_repo_clearing",
            target_id="us_treasuries_custody",
            relation="sponsored_dvp_repo_settlement",
            weight=0.98,
            rel_embedding=self.relation_embeddings["sponsored_dvp_repo_settlement"],
        )
        sub.add_relation(
            source_id="ficc_sponsored_repo_clearing",
            target_id="us_treasury_tga",
            relation="sponsored_dvp_repo_settlement",
            weight=1.02,
            rel_embedding=self.relation_embeddings["sponsored_dvp_repo_settlement"],
        )
        sub.add_relation(
            source_id="fed_standing_repo_facility",
            target_id="us_treasury_tga",
            relation="srf_backstop_liquidity_injection",
            weight=1.15,
            rel_embedding=self.relation_embeddings["srf_backstop_liquidity_injection"],
        )

        # Crédit Agricole CIB & Natixis Dealer Syndicate Bypass (Mitigating svt_dealers_bnp_socgen SPOF)
        sub.add_relation(
            source_id="french_republic_tresor",
            target_id="ca_cib_natixis_dealer_syndicate",
            relation="oat_secondary_syndication_auction",
            weight=1.25,
            rel_embedding=self.relation_embeddings["oat_secondary_syndication_auction"],
        )
        sub.add_relation(
            source_id="ca_cib_natixis_dealer_syndicate",
            target_id="banque_de_france",
            relation="syndicate_reserve_clearing",
            weight=1.18,
            rel_embedding=self.relation_embeddings["syndicate_reserve_clearing"],
        )
        sub.add_relation(
            source_id="ca_cib_natixis_dealer_syndicate",
            target_id="offshore_fx_swap_desk",
            relation="syndicate_usd_fx_swap",
            weight=1.20,
            rel_embedding=self.relation_embeddings["syndicate_usd_fx_swap"],
        )

        # Dark Matter Entities
        sub.add_relation(
            source_id="dtcc_treasury_basis_trade_clearing",
            target_id="us_treasuries_custody",
            relation="basis_trade_leverage_absorption",
            weight=1.00,
            rel_embedding=self.relation_embeddings["basis_trade_leverage_absorption"],
        )
        sub.add_relation(
            source_id="bis_otc_derivatives_pool",
            target_id="offshore_fx_swap_desk",
            relation="otc_derivatives_collateral_drain",
            weight=1.05,
            rel_embedding=self.relation_embeddings["otc_derivatives_collateral_drain"],
        )
        sub.add_relation(
            source_id="pboc_safe_foreign_reserves",
            target_id="pboc_bilateral_swap_network",
            relation="pboc_bilateral_swap_activation",
            weight=1.08,
            rel_embedding=self.relation_embeddings["pboc_bilateral_swap_activation"],
        )
        sub.add_relation(
            source_id="imf_errors_and_omissions_pool",
            target_id="us_triparty_repo_pool",
            relation="imf_errors_and_omissions_absorption",
            weight=1.10,
            rel_embedding=self.relation_embeddings["imf_errors_and_omissions_absorption"],
        )

        # Decoy Sink Trap Mitigation: Retag fintechs/housing as pass-through and recirculate repayments
        for decoy_id in ["pretto_digital_mortgage", "floa_bank_instant_credit", "paris_habitat_hlm"]:
            if decoy_id in sub.entities:
                sub.entities[decoy_id].metadata["is_pass_through"] = True
                sub.entities[decoy_id].metadata["absorbing_sink"] = False

        if "pretto_digital_mortgage" in sub.entities and "caisse_epargne_idf" in sub.entities:
            sub.add_relation(
                source_id="pretto_digital_mortgage",
                target_id="caisse_epargne_idf",
                relation="retail_mortgage_amortization_recirculation",
                weight=0.85,
                rel_embedding=self.relation_embeddings["retail_mortgage_amortization_recirculation"],
            )
        if "floa_bank_instant_credit" in sub.entities and "svt_dealers_bnp_socgen" in sub.entities:
            sub.add_relation(
                source_id="floa_bank_instant_credit",
                target_id="svt_dealers_bnp_socgen",
                relation="instant_credit_repayment_recirculation",
                weight=0.85,
                rel_embedding=self.relation_embeddings["instant_credit_repayment_recirculation"],
            )
        if "paris_habitat_hlm" in sub.entities and "banque_populaire_val_de_france" in sub.entities:
            sub.add_relation(
                source_id="paris_habitat_hlm",
                target_id="banque_populaire_val_de_france",
                relation="social_housing_rent_recirculation",
                weight=0.85,
                rel_embedding=self.relation_embeddings["social_housing_rent_recirculation"],
            )

        logger.info(
            f"Synthesized adversarial substrate: {len(sub.entities)} nodes, "
            f"{sum(len(t) for t in sub.adjacency.values())} outgoing edge endpoints."
        )
        return sub, self.entity_metrics

    def build_adversarial_engine(
        self,
        max_nodes_k: int = 128,
        max_edges_m: int = 512,
        num_landmark_clusters: int = 8,
        latent_epsilon: float = 0.10,
    ) -> Tuple[ProceduralGraphEngine, L3LatentSubstrate]:
        """Initializes ProceduralGraphEngine backed by the adversarial substrate."""
        sub, _ = self.build_adversarial_substrate()
        engine = ProceduralGraphEngine(
            max_nodes_k=max_nodes_k,
            max_edges_m=max_edges_m,
            node_dim=self.node_dim,
            rel_dim=self.rel_dim,
            num_landmark_clusters=num_landmark_clusters,
            latent_epsilon=latent_epsilon,
            substrate=sub,
        )
        engine.corridor_materializer.bidirectional.latent_epsilon = latent_epsilon
        engine.initialize_landmarks()
        return engine, sub


def greedy_nearest_neighbor_search(
    source_id: str,
    target_id: str,
    substrate: L3LatentSubstrate,
    max_hops: int = 15,
) -> Tuple[bool, List[str], str]:
    """Simulates naive greedy 1-hop nearest-neighbor traversal.

    At each hop u, evaluates all immediate outgoing neighbors v in Out(u),
    and greedily picks v* = argmax_{v} cos(z_v, z_target).
    Demonstrates vulnerability to deceptive high-similarity distractors.

    Returns:
        Tuple of (success: bool, path_nodes: List[str], failure_reason: str).
    """
    tgt_node = substrate.get_entity(target_id)
    if not tgt_node:
        return False, [], "Target entity not found in substrate"
    tgt_emb = tgt_node.embedding

    curr = source_id
    visited = [curr]
    for _ in range(max_hops):
        if curr == target_id:
            return True, visited, "Target reached"
        neighbors = [nbr for nbr, _ in substrate.expand_procedural_neighbors(curr, "out")]
        if not neighbors:
            return False, visited, "Dead end: no outgoing edges"
        cands = [n for n in neighbors if n.entity_id not in visited]
        if not cands:
            return False, visited, "Cycle trapped: all neighbors already visited"
        # Greedily pick neighbor with highest cosine similarity to target
        sims = [(n.entity_id, float(np.dot(n.embedding, tgt_emb))) for n in cands]
        sims.sort(key=lambda x: x[1], reverse=True)
        best_next, _ = sims[0]
        visited.append(best_next)
        curr = best_next
    return False, visited, "Max hops exceeded without reaching target"

