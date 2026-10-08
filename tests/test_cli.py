"""Unit and Integration Tests for Capital Manifold CLI."""

from __future__ import annotations

import json
from pathlib import Path
import pytest
from capital_manifold.cli import build_parser, main


def test_cli_parser_creation():
    parser = build_parser()
    assert parser.prog == "capital-manifold"
    subparsers = [action for action in parser._actions if action.dest == "subcommand"]
    assert len(subparsers) == 1
    choices = subparsers[0].choices
    assert set(choices.keys()) == {"audit", "siphon", "simulate", "serve", "traverse"}


def test_cli_help(capsys):
    ret = main([])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Capital Manifold" in captured.out
    assert "audit" in captured.out
    assert "siphon" in captured.out

    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_cli_audit_subcommand(tmp_path: Path):
    out_json = tmp_path / "audit_test.json"
    ret = main(["audit", "--output-json", str(out_json)])
    assert ret == 0
    assert out_json.exists()
    with open(out_json) as f:
        data = json.load(f)
    assert "system_integrity_score" in data
    assert "category_scores" in data


def test_cli_siphon_subcommand(tmp_path: Path):
    out_json = tmp_path / "siphon_test.json"
    ret = main(["siphon", "--output-json", str(out_json)])
    assert ret == 0
    assert out_json.exists()
    with open(out_json) as f:
        data = json.load(f)
    assert "total_siphoned_volume_usd" in data
    assert "bilateral_discrepancies" in data


def test_cli_simulate_subcommand(tmp_path: Path):
    out_json = tmp_path / "simulate_test.json"
    ret = main(["simulate", "--output-json", str(out_json)])
    assert ret == 0
    assert out_json.exists()
    with open(out_json) as f:
        data = json.load(f)
    assert "overall_resilience_score" in data
    assert "regimes" in data


def test_cli_traverse_subcommand():
    ret = main(["traverse", "--mode", "macro"])
    assert ret == 0
