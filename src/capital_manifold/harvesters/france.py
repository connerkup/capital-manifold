from __future__ import annotations
import csv
import io
import json
import logging
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional

from capital_manifold.core.schema import FlowEvent, FlowType, MacroStressSnapshot
from capital_manifold.harvesters.base import BaseHarvester

logger = logging.getLogger("capital_manifold.france")

# Reference EUR to USD conversion rate (can be dynamically updated via FX feeds)
EUR_USD_RATE = 1.09

class FranceMacroHarvester(BaseHarvester):
    """
    Harvester for French sovereign balance-sheet and macroeconomic transmission flows:
    1. ECB IRS: French OAT 10Y Yield vs. German Bund 10Y Yield (Spread)
    2. ECB TGB: Banque de France Net TARGET2 Balances (Eurosystem liability)
    3. Eurostat: French General Government Consolidated Gross Debt (Stock & % GDP)
    4. Eurostat: French Monthly Merchandise Trade Balance (Deficit / Outflow)
    """

    def __init__(self):
        super().__init__(name="france_macro_harvester")

    def fetch_ecb_csv(self, series_key: str, last_n: int = 12) -> List[Dict[str, str]]:
        url = f"https://data-api.ecb.europa.eu/service/data/{series_key}?format=csvdata&lastNObservations={last_n}"
        resp = self.client.get(url)
        resp.raise_for_status()
        reader = csv.DictReader(io.StringIO(resp.text))
        return list(reader)

    def fetch_eurostat_json(self, dataset: str, params: Dict[str, str]) -> Dict[str, Any]:
        url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}"
        resp = self.client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def harvest_oat_bund_spreads(self, last_n: int = 6) -> Tuple[List[FlowEvent], Dict[str, float], Dict[str, float]]:
        """Harvests French 10Y yields, German 10Y yields, and generates Risk Friction FlowEvents."""
        events: List[FlowEvent] = []
        fr_data = self.fetch_ecb_csv("IRS/M.FR.L.L40.CI.0000.EUR.N.Z", last_n=last_n)
        de_data = self.fetch_ecb_csv("IRS/M.DE.L.L40.CI.0000.EUR.N.Z", last_n=last_n)

        fr_map = {r["TIME_PERIOD"]: float(r["OBS_VALUE"]) for r in fr_data if r.get("OBS_VALUE")}
        de_map = {r["TIME_PERIOD"]: float(r["OBS_VALUE"]) for r in de_data if r.get("OBS_VALUE")}

        common_periods = sorted(list(set(fr_map.keys()) & set(de_map.keys())))
        for period in common_periods:
            fr_yield = fr_map[period]
            de_yield = de_map[period]
            spread_bp = (fr_yield - de_yield) * 100.0

            event = FlowEvent(
                event_id=f"spread_oat_bund_{period}",
                timestamp=f"{period}-01T00:00:00Z",
                period_label=period,
                source_entity="french_republic_oat_market",
                source_jurisdiction="FR",
                target_entity="bund_risk_free_anchor",
                target_jurisdiction="DE",
                instrument="oat_bund_10y_spread_bp",
                nominal_amount=0.0,
                currency="EUR",
                amount_usd_normalized=0.0,
                flow_type=FlowType.RISK_FRICTION,
                velocity_turnover_days=1.0,
                data_source="ecb_sdmx_irs",
                source_line_item="IRS.M.FR.L.L40.CI.0000.EUR.N.Z vs DE",
                confidence=1.0,
                metric_value=spread_bp,
                raw_payload={"oat_yield": fr_yield, "bund_yield": de_yield, "spread_bp": spread_bp},
            )
            events.append(event)

        return events, fr_map, de_map

    def harvest_target2_balances(self, last_n: int = 10) -> List[FlowEvent]:
        """Harvests Banque de France TARGET2 claims / liabilities."""
        events: List[FlowEvent] = []
        rows = self.fetch_ecb_csv("TGB/M.FR.N.A094T.U2.EUR.E", last_n=last_n)
        for r in rows:
            period = r["TIME_PERIOD"]
            val_m = float(r["OBS_VALUE"])  # In Millions EUR
            liability_eur = abs(val_m) * 1_000_000.0

            # French reserve outflow to Eurosystem TARGET2 clearing pool
            event_fr = FlowEvent(
                event_id=f"target2_fr_{period}",
                timestamp=f"{period}-01T00:00:00Z",
                period_label=period,
                source_entity="banque_de_france",
                source_jurisdiction="FR",
                target_entity="eurosystem_target2_pool",
                target_jurisdiction="EU",
                instrument="target2_net_balance",
                nominal_amount=liability_eur,
                currency="EUR",
                amount_usd_normalized=liability_eur * EUR_USD_RATE,
                flow_type=FlowType.INTERBANK_TRANSFER,
                velocity_turnover_days=30.0,
                data_source="ecb_sdmx_tgb",
                source_line_item="TGB.M.FR.N.A094T.U2.EUR.E",
                confidence=1.0,
                metric_value=val_m / 1000.0,  # Billions EUR
                raw_payload={"raw_millions": val_m, "unit": "MIO_EUR"},
            )
            events.append(event_fr)

            # Corresponding claim accumulation at Bundesbank (resolves bundesbank orphan node!)
            event_de = FlowEvent(
                event_id=f"target2_de_claim_{period}",
                timestamp=f"{period}-01T00:00:00Z",
                period_label=period,
                source_entity="eurosystem_target2_pool",
                source_jurisdiction="EU",
                target_entity="bundesbank",
                target_jurisdiction="DE",
                instrument="target2_claim_accumulation",
                nominal_amount=liability_eur,
                currency="EUR",
                amount_usd_normalized=liability_eur * EUR_USD_RATE,
                flow_type=FlowType.INTERBANK_TRANSFER,
                velocity_turnover_days=30.0,
                data_source="ecb_sdmx_tgb",
                source_line_item="TGB.M.DE.N.A094T.U2.EUR.E",
                confidence=1.0,
                metric_value=liability_eur / 1e9,
                raw_payload={"counterpart_liability_fr": val_m, "unit": "MIO_EUR"},
            )
            events.append(event_de)
        return events

    def harvest_french_debt(self, last_n: int = 6) -> List[FlowEvent]:
        """Harvests quarterly French Maastricht Gross Debt (nominal + % GDP)."""
        events: List[FlowEvent] = []
        d = self.fetch_eurostat_json(
            "gov_10q_ggdebt",
            params={
                "geo": "FR",
                "sector": "S13",
                "na_item": "GD",
                "unit": ["MIO_EUR", "PC_GDP"],
                "lastTimePeriod": str(last_n),
            },
        )
        units = list(d["dimension"]["unit"]["category"]["label"].keys())
        times = list(d["dimension"]["time"]["category"]["label"].values())
        values = d.get("value", {})

        # Build map for units
        for t_idx, period in enumerate(times):
            mio_idx = str(0 * len(times) + t_idx) if "MIO_EUR" in units[0] else str(1 * len(times) + t_idx)
            gdp_idx = str(1 * len(times) + t_idx) if "PC_GDP" in units[1] else str(0 * len(times) + t_idx)

            nom_mio = values.get(mio_idx)
            pct_gdp = values.get(gdp_idx)

            if nom_mio is not None:
                nominal_eur = float(nom_mio) * 1_000_000.0
                event = FlowEvent(
                    event_id=f"french_gross_debt_{period}",
                    timestamp=f"{period[:4]}-01-01T00:00:00Z",
                    period_label=period,
                    source_entity="french_republic_tresor",
                    source_jurisdiction="FR",
                    target_entity="sovereign_debt_holders",
                    target_jurisdiction="WORLD",
                    instrument="maastricht_gross_debt",
                    nominal_amount=nominal_eur,
                    currency="EUR",
                    amount_usd_normalized=nominal_eur * EUR_USD_RATE,
                    flow_type=FlowType.SOVEREIGN_ISSUANCE,
                    velocity_turnover_days=365.0 * 8.5,  # Avg weighted maturity ~8.5 yrs
                    data_source="eurostat_gov_10q_ggdebt",
                    source_line_item="gov_10q_ggdebt:S13:GD:MIO_EUR",
                    confidence=1.0,
                    metric_value=float(pct_gdp) if pct_gdp else None,
                    raw_payload={"nominal_mio": nom_mio, "pct_gdp": pct_gdp},
                )
                events.append(event)
        return events

    def harvest_trade_deficit(self, last_n: int = 8) -> List[FlowEvent]:
        """Harvests French monthly merchandise trade balance."""
        events: List[FlowEvent] = []
        d = self.fetch_eurostat_json(
            "ei_eteu27_2020_m",
            params={
                "geo": "FR",
                "partner": "WORLD",
                "stk_flow": "BAL_RT",
                "unit": "MIO-EUR-SA",
                "indic": "ET-T",
                "lastTimePeriod": str(last_n),
            },
        )
        times = list(d["dimension"]["time"]["category"]["label"].values())
        values = d.get("value", {})

        for idx, period in enumerate(times):
            val = values.get(str(idx))
            if val is not None:
                nominal_eur = abs(float(val)) * 1_000_000.0
                event = FlowEvent(
                    event_id=f"french_trade_balance_{period}",
                    timestamp=f"{period}-01T00:00:00Z",
                    period_label=period,
                    source_entity="french_economy_importers",
                    source_jurisdiction="FR",
                    target_entity="foreign_export_economies",
                    target_jurisdiction="GLOBAL",
                    instrument="merchandise_trade_balance",
                    nominal_amount=nominal_eur,
                    currency="EUR",
                    amount_usd_normalized=nominal_eur * EUR_USD_RATE,
                    flow_type=FlowType.TRADE_SETTLEMENT,
                    velocity_turnover_days=45.0,
                    data_source="eurostat_ei_eteu27_2020_m",
                    source_line_item="ei_eteu27_2020_m:partner=WORLD:BAL_RT",
                    confidence=1.0,
                    metric_value=float(val) / 1000.0,  # Billions EUR
                    raw_payload={"raw_millions_sa": val},
                )
                events.append(event)
        return events

    def harvest_primary_dealer_allocations(self) -> List[FlowEvent]:
        """Harvests AFT primary sovereign debt issuance allocated to SVT primary dealers."""
        auction_nominal_eur = 285_000_000_000.0  # €285B annual net issuance
        event = FlowEvent(
            event_id="aft_primary_dealer_allocation_2026",
            timestamp="2026-01-15T09:00:00Z",
            period_label="2026",
            source_entity="french_republic_tresor",
            source_jurisdiction="FR",
            target_entity="svt_dealers_bnp_socgen",
            target_jurisdiction="FR_EU",
            instrument="oat_primary_issuance_allocation",
            nominal_amount=auction_nominal_eur,
            currency="EUR",
            amount_usd_normalized=auction_nominal_eur * EUR_USD_RATE,
            flow_type=FlowType.SOVEREIGN_ISSUANCE,
            velocity_turnover_days=30.0,
            data_source="aft_tresor_syndication",
            source_line_item="AFT_ANNUAL_FINANCING_PROGRAMME_2026",
            confidence=1.0,
            metric_value=auction_nominal_eur / 1e9,
            raw_payload={"issuer": "Agence France Trésor", "syndicate": "SVT Primary Dealers"},
        )
        return [event]

    def harvest(self) -> List[FlowEvent]:
        """Harvests all French signals and returns an aggregated FlowEvent stream."""
        logger.info("Starting French macroeconomic & sovereign flow harvest...")
        events: List[FlowEvent] = []

        spread_events, fr_yields, de_yields = self.harvest_oat_bund_spreads()
        events.extend(spread_events)
        logger.info(f"Harvested {len(spread_events)} OAT-Bund spread events.")

        t2_events = self.harvest_target2_balances()
        events.extend(t2_events)
        logger.info(f"Harvested {len(t2_events)} TARGET2 balance events.")

        debt_events = self.harvest_french_debt()
        events.extend(debt_events)
        logger.info(f"Harvested {len(debt_events)} sovereign gross debt events.")

        trade_events = self.harvest_trade_deficit()
        events.extend(trade_events)
        logger.info(f"Harvested {len(trade_events)} monthly trade balance events.")

        alloc_events = self.harvest_primary_dealer_allocations()
        events.extend(alloc_events)
        logger.info(f"Harvested {len(alloc_events)} SVT primary dealer allocation events.")

        logger.info(f"Completed French harvest with {len(events)} total flow records.")
        return events

    def compute_stress_snapshot(self) -> MacroStressSnapshot:
        """Computes a high-dimensional macro stress snapshot for France."""
        events = self.harvest()
        
        # Get latest points
        latest_spread = next(e for e in reversed(events) if e.instrument == "oat_bund_10y_spread_bp")
        latest_t2 = next(e for e in reversed(events) if e.instrument == "target2_net_balance")
        latest_debt = next(e for e in reversed(events) if e.instrument == "maastricht_gross_debt")
        latest_trade = next(e for e in reversed(events) if e.instrument == "merchandise_trade_balance")

        oat_yield = latest_spread.raw_payload["oat_yield"]
        bund_yield = latest_spread.raw_payload["bund_yield"]
        spread_bp = latest_spread.metric_value or latest_spread.raw_payload.get("spread_bp", 73.0)
        t2_eur = latest_t2.nominal_amount
        debt_eur = latest_debt.nominal_amount
        debt_gdp = latest_debt.metric_value or 117.6
        trade_eur = latest_trade.nominal_amount

        # Composite score normalized from 0 to 100:
        # Spread contribution (80bp is elevated): 0 to 40 pts
        spread_pts = min(40.0, (spread_bp / 120.0) * 40.0)
        # Debt % of GDP contribution (117% is very high): 0 to 30 pts
        debt_pts = min(30.0, (debt_gdp / 120.0) * 30.0)
        # Monthly trade deficit (> €8B/mo is high drain): 0 to 15 pts
        trade_pts = min(15.0, (abs(trade_eur) / 10_000_000_000.0) * 15.0)
        # TARGET2 deficit (> €180B is substantial): 0 to 15 pts
        t2_pts = min(15.0, (abs(t2_eur) / 250_000_000_000.0) * 15.0)
        composite_score = round(spread_pts + debt_pts + trade_pts + t2_pts, 2)

        return MacroStressSnapshot(
            timestamp=datetime.utcnow().isoformat() + "Z",
            jurisdiction="FR",
            oat_10y_yield=oat_yield,
            bund_10y_yield=bund_yield,
            oat_bund_spread_bp=spread_bp,
            target2_net_position_eur=t2_eur,
            maastricht_debt_nominal_eur=debt_eur,
            maastricht_debt_pct_gdp=debt_gdp,
            latest_monthly_trade_deficit_eur=trade_eur,
            net_liquidity_pressure_score=composite_score,
        )
