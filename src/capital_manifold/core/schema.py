from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator

class FlowType(str, Enum):
    GENESIS_CREDIT = "genesis_credit"           # Central bank QE / commercial bank loan creation
    SOVEREIGN_ISSUANCE = "sovereign_issuance"   # Government bond auction / debt increase
    TAX_ABSORPTION = "tax_absorption"           # Cash drained from private banks to Treasury
    QT_BURN = "qt_burn"                         # Balance sheet runoff / money destroyed
    INTERBANK_TRANSFER = "interbank_transfer"   # Fedwire, TARGET2, CHIPS settlement
    REPO_COLLATERAL = "repo_collateral"         # Cash lent against collateral
    TRADE_SETTLEMENT = "trade_settlement"       # Import/Export payment drain or inflow
    POOL_CONCENTRATION = "pool_concentration"   # Capital accumulating in MMF / Corporate cash
    RISK_FRICTION = "risk_friction"             # Spread / potential gradient indicator
    SYNTHETIC_DERIVATIVE = "synthetic_derivative" # OTC interest rate / FX derivatives
    BILATERAL_SWAP = "bilateral_swap"           # Cross-currency central bank swap lines
    REINVESTMENT_ALLOCATION = "reinvestment_allocation" # Corporate cash reinvestment in T-bills/MMF
    MARITIME_LOGISTICS_MARGIN = "maritime_logistics_margin" # Freight, dark tanker insurance & trading margin

class FlowEvent(BaseModel):
    event_id: str
    timestamp: str                              # ISO 8601 string (e.g. 2026-08-01T00:00:00Z)
    period_label: str                           # e.g. "2026-08", "2026-Q1"
    
    # Counterparties & Jurisdictions
    source_entity: str                          # e.g. "french_republic_tresor", "banque_de_france"
    source_jurisdiction: str                    # "FR", "EU", "DE", "US", "WORLD"
    target_entity: str                          # e.g. "eurosystem_target2_pool", "primary_dealers"
    target_jurisdiction: str                    # "EU", "DE", "WORLD"
    
    # Financial quantities
    instrument: str                             # "oat_10y_spread", "target2_liability", "maastricht_debt", "trade_deficit"
    nominal_amount: float                       # In native currency
    currency: str                               # "EUR", "USD"
    amount_usd_normalized: float                # At EUR/USD reference rate (~1.09)
    
    flow_type: FlowType
    velocity_turnover_days: Optional[float] = None
    
    # Provenance
    data_source: str                            # "ecb_sdmx", "eurostat_dissemination", "banque_de_france"
    source_line_item: str                       # e.g. "TGB.M.FR.N.A094T.U2.EUR.E"
    confidence: float = 1.0
    metric_value: Optional[float] = None        # Secondary scalar (e.g. yield %, debt % of GDP)
    raw_payload: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_flow_invariants(self) -> FlowEvent:
        if self.nominal_amount < 0.0:
            raise ValueError(f"nominal_amount must be >= 0.0 for directed flow events, got {self.nominal_amount}")
        if self.amount_usd_normalized < 0.0:
            raise ValueError(f"amount_usd_normalized must be >= 0.0 for directed flow events, got {self.amount_usd_normalized}")

        is_spread_metric = (
            self.flow_type == FlowType.RISK_FRICTION
            or (self.instrument and self.instrument.endswith("_bp"))
        )
        if is_spread_metric:
            if self.nominal_amount != 0.0 or self.amount_usd_normalized != 0.0:
                raise ValueError(
                    f"Flow events with RISK_FRICTION or instrument ending in '_bp' must have nominal_amount == 0.0 "
                    f"and amount_usd_normalized == 0.0, storing the basis point value strictly in metric_value. "
                    f"Got nominal_amount={self.nominal_amount}, amount_usd_normalized={self.amount_usd_normalized}"
                )
        return self

class MacroStressSnapshot(BaseModel):
    timestamp: str
    jurisdiction: str
    oat_10y_yield: float
    bund_10y_yield: float
    oat_bund_spread_bp: float
    target2_net_position_eur: float
    maastricht_debt_nominal_eur: float
    maastricht_debt_pct_gdp: float
    latest_monthly_trade_deficit_eur: float
    net_liquidity_pressure_score: float         # Normalized stress index (0 to 100)
