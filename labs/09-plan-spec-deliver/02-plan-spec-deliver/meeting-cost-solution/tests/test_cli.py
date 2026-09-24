import subprocess
import sys
from pathlib import Path

from meeting_cost.cli import main

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_module(*args):
    return subprocess.run(
        [sys.executable, "-m", "meeting_cost", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_prints_total_and_breakdown_and_exits_zero(capsys):
    exit_code = main(["60", "100", "80", "60"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Attendee 1 at 100 per hour: 100" in output
    assert "Attendee 2 at 80 per hour: 80" in output
    assert "Attendee 3 at 60 per hour: 60" in output
    assert "Total: 240.00" in output


def test_cli_second_acceptance_criterion(capsys):
    exit_code = main(["30", "90"])
    assert exit_code == 0
    assert "Total: 45.00" in capsys.readouterr().out


def test_cli_zero_attendees_exits_zero_with_total_zero(capsys):
    exit_code = main(["60"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Attendees: 0" in output
    assert "Total: 0.00" in output


def test_cli_zero_duration_exits_zero_with_total_zero(capsys):
    exit_code = main(["0", "100", "80"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Total: 0.00" in output


def test_cli_negative_duration_exits_non_zero_naming_duration(capsys):
    exit_code = main(["-30", "100"])
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "duration" in captured.err
    assert captured.out == ""


def test_cli_negative_rate_exits_non_zero_naming_the_rate(capsys):
    exit_code = main(["30", "100", "-80"])
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "rate 2" in captured.err


def test_cli_non_numeric_rate_exits_non_zero_naming_the_rate(capsys):
    exit_code = main(["30", "eighty"])
    captured = capsys.readouterr()
    assert exit_code != 0
    assert "rate 1" in captured.err


def test_module_entry_point_returns_zero_for_valid_input():
    completed = run_module("60", "100", "80", "60")
    assert completed.returncode == 0
    assert "Total: 240.00" in completed.stdout


def test_module_entry_point_returns_non_zero_for_invalid_input():
    completed = run_module("-30", "100")
    assert completed.returncode != 0
    assert "duration" in completed.stderr


def test_calculation_logic_imports_without_the_cli_layer():
    probe = "import meeting_cost.calculator, sys; print('meeting_cost.cli' in sys.modules)"
    completed = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    assert completed.stdout.strip() == "False"
