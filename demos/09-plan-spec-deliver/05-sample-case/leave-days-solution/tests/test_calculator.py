from decimal import Decimal
from pathlib import Path

import pytest

from leave_days.calculator import InvalidInputError, YearCharge, charge_leave, parse_holidays

ROOT = Path(__file__).resolve().parent.parent


def calendar(name="holidays-2026-2027.txt"):
    return parse_holidays((ROOT / name).read_text(encoding="utf-8").splitlines())


def test_plain_week_counts_each_working_day():
    assert charge_leave("2026-12-14", "2026-12-18", calendar()).total == Decimal("5")


def test_christmas_week_counts_half_day_and_skips_holiday():
    assert charge_leave("2026-12-21", "2026-12-25", calendar()).total == Decimal("3.5")


def test_request_across_new_year_splits_per_year():
    charge = charge_leave("2026-12-28", "2027-01-08", calendar())
    assert charge.per_year == (YearCharge(2026, Decimal("3.5")), YearCharge(2027, Decimal("4")))
    assert charge.total == Decimal("7.5")


def test_per_year_charges_sum_to_total():
    charge = charge_leave("2026-12-01", "2027-01-15", calendar())
    assert sum(item.days for item in charge.per_year) == charge.total


def test_counts_are_decimal():
    charge = charge_leave("2026-12-21", "2026-12-25", calendar())
    assert isinstance(charge.total, Decimal)
    assert all(isinstance(item.days, Decimal) for item in charge.per_year)


def test_weekend_only_request_is_zero():
    assert charge_leave("2026-12-19", "2026-12-20", calendar()).total == Decimal("0")


def test_single_day_request_is_inclusive():
    assert charge_leave("2026-12-22", "2026-12-22", calendar()).total == Decimal("1")


def test_holiday_on_weekend_is_not_deducted_twice():
    assert charge_leave("2026-12-26", "2026-12-27", calendar()).total == Decimal("0")


def test_end_before_start_names_end():
    with pytest.raises(InvalidInputError) as error:
        charge_leave("2026-12-22", "2026-12-21", calendar())
    assert error.value.field == "end"


@pytest.mark.parametrize("start,end,field", [("2026-13-01", "2026-12-31", "start"), ("2026-12-01", "tomorrow", "end")])
def test_malformed_date_names_field(start, end, field):
    with pytest.raises(InvalidInputError) as error:
        charge_leave(start, end, calendar())
    assert error.value.field == field


def test_year_without_holiday_data_is_rejected():
    with pytest.raises(InvalidInputError) as error:
        charge_leave("2026-12-28", "2027-01-08", calendar("holidays-2026.txt"))
    assert error.value.field == "holidays"
    assert "2027" in str(error.value)


@pytest.mark.parametrize("lines,field", [
    (["2026-12-25", "2026-12-25"], "holidays line 2"),
    (["2026-12-24 quarter"], "holidays line 1"),
    (["", "24.12.2026"], "holidays line 2"),
])
def test_malformed_holiday_file_names_line(lines, field):
    with pytest.raises(InvalidInputError) as error:
        parse_holidays(lines)
    assert error.value.field == field


def test_no_holiday_date_is_hard_coded():
    source = (ROOT / "leave_days" / "calculator.py").read_text(encoding="utf-8")
    assert "12-25" not in source and "date(20" not in source
