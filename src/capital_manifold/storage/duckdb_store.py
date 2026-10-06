from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import List, Optional
import duckdb
from capital_manifold.core.schema import FlowEvent, MacroStressSnapshot

logger = logging.getLogger("capital_manifold.storage")

class ManifoldStore:
    """High-throughput DuckDB & Parquet storage engine for normalized FlowEvents."""

    def __init__(self, db_path: Path = Path("/home/ubuntu/repos/capital-manifold/data/cache/manifold.duckdb")):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._init_tables()

    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS flow_events (
                event_id VARCHAR PRIMARY KEY,
                timestamp VARCHAR,
                period_label VARCHAR,
                source_entity VARCHAR,
                source_jurisdiction VARCHAR,
                target_entity VARCHAR,
                target_jurisdiction VARCHAR,
                instrument VARCHAR,
                nominal_amount DOUBLE,
                currency VARCHAR,
                amount_usd_normalized DOUBLE,
                flow_type VARCHAR,
                velocity_turnover_days DOUBLE,
                data_source VARCHAR,
                source_line_item VARCHAR,
                confidence DOUBLE,
                metric_value DOUBLE,
                raw_payload_json VARCHAR,
                ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS macro_stress_snapshots (
                snapshot_id VARCHAR PRIMARY KEY,
                timestamp VARCHAR,
                jurisdiction VARCHAR,
                oat_10y_yield DOUBLE,
                bund_10y_yield DOUBLE,
                oat_bund_spread_bp DOUBLE,
                target2_net_position_eur DOUBLE,
                maastricht_debt_nominal_eur DOUBLE,
                maastricht_debt_pct_gdp DOUBLE,
                latest_monthly_trade_deficit_eur DOUBLE,
                net_liquidity_pressure_score DOUBLE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    def insert_flow_events(self, events: List[FlowEvent]) -> int:
        records = [
            (
                e.event_id,
                e.timestamp,
                e.period_label,
                e.source_entity,
                e.source_jurisdiction,
                e.target_entity,
                e.target_jurisdiction,
                e.instrument,
                e.nominal_amount,
                e.currency,
                e.amount_usd_normalized,
                e.flow_type.value,
                e.velocity_turnover_days,
                e.data_source,
                e.source_line_item,
                e.confidence,
                e.metric_value,
                json.dumps(e.raw_payload),
            )
            for e in events
        ]
        
        self.conn.executemany("""
            INSERT OR REPLACE INTO flow_events (
                event_id, timestamp, period_label, source_entity, source_jurisdiction,
                target_entity, target_jurisdiction, instrument, nominal_amount, currency,
                amount_usd_normalized, flow_type, velocity_turnover_days, data_source,
                source_line_item, confidence, metric_value, raw_payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, records)
        logger.info(f"Upserted {len(records)} flow records into DuckDB ({self.db_path}).")
        return len(records)

    def insert_stress_snapshot(self, s: MacroStressSnapshot) -> str:
        snapshot_id = f"stress_{s.jurisdiction}_{s.timestamp.replace(':', '_')}"
        self.conn.execute("""
            INSERT OR REPLACE INTO macro_stress_snapshots (
                snapshot_id, timestamp, jurisdiction, oat_10y_yield, bund_10y_yield,
                oat_bund_spread_bp, target2_net_position_eur, maastricht_debt_nominal_eur,
                maastricht_debt_pct_gdp, latest_monthly_trade_deficit_eur, net_liquidity_pressure_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            snapshot_id, s.timestamp, s.jurisdiction, s.oat_10y_yield, s.bund_10y_yield,
            s.oat_bund_spread_bp, s.target2_net_position_eur, s.maastricht_debt_nominal_eur,
            s.maastricht_debt_pct_gdp, s.latest_monthly_trade_deficit_eur, s.net_liquidity_pressure_score
        ))
        logger.info(f"Recorded macro stress snapshot: score={s.net_liquidity_pressure_score} for {s.jurisdiction}")
        return snapshot_id

    def export_parquet(self, output_dir: Path = Path("/home/ubuntu/repos/capital-manifold/data/processed")):
        output_dir.mkdir(parents=True, exist_ok=True)
        parquet_events = output_dir / "flow_events.parquet"
        parquet_snapshots = output_dir / "stress_snapshots.parquet"
        
        self.conn.execute(f"COPY flow_events TO '{parquet_events}' (FORMAT PARQUET);")
        self.conn.execute(f"COPY macro_stress_snapshots TO '{parquet_snapshots}' (FORMAT PARQUET);")
        logger.info(f"Exported Parquet partitions to {output_dir}")

    def query_df(self, query: str):
        return self.conn.execute(query).df()

    def close(self):
        self.conn.close()
