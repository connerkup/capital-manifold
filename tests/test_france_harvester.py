import pytest
from pathlib import Path
import sys

src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from capital_manifold.core.schema import FlowEvent, FlowType
from capital_manifold.harvesters.france import FranceMacroHarvester
from capital_manifold.storage.duckdb_store import ManifoldStore

def test_france_harvester_instantiation():
    harvester = FranceMacroHarvester()
    assert harvester.name == "france_macro_harvester"
    harvester.close()

def test_duckdb_storage_roundtrip(tmp_path):
    db_file = tmp_path / "test_manifold.duckdb"
    store = ManifoldStore(db_path=db_file)
    
    event = FlowEvent(
        event_id="test_ev_1",
        timestamp="2026-08-01T00:00:00Z",
        period_label="2026-08",
        source_entity="banque_de_france",
        source_jurisdiction="FR",
        target_entity="eurosystem_target2_pool",
        target_jurisdiction="EU",
        instrument="target2_net_balance",
        nominal_amount=-181336520000.0,
        currency="EUR",
        amount_usd_normalized=-197656806800.0,
        flow_type=FlowType.INTERBANK_TRANSFER,
        velocity_turnover_days=30.0,
        data_source="ecb_sdmx_tgb",
        source_line_item="TGB.M.FR.N.A094T.U2.EUR.E",
        confidence=1.0,
        metric_value=-181.34,
        raw_payload={"test": True}
    )
    
    count = store.insert_flow_events([event])
    assert count == 1
    
    df = store.query_df("SELECT * FROM flow_events WHERE event_id = 'test_ev_1'")
    assert len(df) == 1
    assert df["instrument"].iloc[0] == "target2_net_balance"
    assert df["nominal_amount"].iloc[0] == -181336520000.0
    
    store.close()
