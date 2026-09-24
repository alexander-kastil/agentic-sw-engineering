import subprocess
import sys
from pathlib import Path

from leave_days.cli import main

ROOT = Path(__file__).resolve().parent.parent
BOTH_YEARS = str(ROOT / "holidays-2026-2027.txt")


def test_prints_per_year_and_total(capsys):
    assert main(["2026-12-28", "2027-01-08", "--holidays", BOTH_YEARS]) == 0
    out = capsys.readouterr().out
    assert "2026: 3.5 days" in out
    assert "2027: 4.0 days" in out
    assert "Total: 7.5 days" in out


def test_invalid_input_names_field_on_stderr(capsys):
    assert main(["2026-12-22", "2026-12-21", "--holidays", BOTH_YEARS]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "end" in captured.err


def test_missing_holiday_file_names_holidays(capsys):
    assert main(["2026-12-21", "2026-12-25", "--holidays", str(ROOT / "missing.txt")]) == 1
    assert "holidays" in capsys.readouterr().err


def test_module_entry_point_runs():
    result = subprocess.run(
        [sys.executable, "-m", "leave_days", "2026-12-21", "2026-12-25", "--holidays", BOTH_YEARS],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "Total: 3.5 days" in result.stdout


def test_calculator_does_not_import_cli():
    result = subprocess.run(
        [sys.executable, "-c", "import sys, leave_days.calculator; print('leave_days.cli' in sys.modules)"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.stdout.strip() == "False"
