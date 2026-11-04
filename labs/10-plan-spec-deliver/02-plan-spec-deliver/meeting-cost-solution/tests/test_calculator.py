from decimal import Decimal

import pytest

from meeting_cost.calculator import InvalidInputError, calculate, round_total


def test_sixty_minutes_three_attendees_totals_240():
    result = calculate("60", ["100", "80", "60"])
    assert result.total == Decimal("240.00")


def test_thirty_minutes_one_attendee_totals_45():
    result = calculate("30", ["90"])
    assert result.total == Decimal("45.00")


def test_breakdown_sums_to_total():
    result = calculate("50", ["100", "80", "60"])
    assert round_total(sum(entry.cost for entry in result.breakdown)) == result.total


def test_breakdown_reports_one_entry_per_attendee_with_its_rate():
    result = calculate("60", ["100", "80", "60"])
    assert [entry.hourly_rate for entry in result.breakdown] == [
        Decimal("100"),
        Decimal("80"),
        Decimal("60"),
    ]
    assert [entry.cost for entry in result.breakdown] == [
        Decimal("100"),
        Decimal("80"),
        Decimal("60"),
    ]


def test_total_is_rounded_half_up_to_two_decimal_places():
    result = calculate("1", ["7.5"])
    assert result.total == Decimal("0.13")


def test_breakdown_values_stay_unrounded():
    result = calculate("10", ["100"])
    assert result.breakdown[0].cost == Decimal("100") * (Decimal(10) / Decimal(60))
    assert result.breakdown[0].cost != round_total(result.breakdown[0].cost)


def test_monetary_values_are_decimal_not_float():
    result = calculate("60", ["100", "80", "60"])
    assert isinstance(result.total, Decimal)
    assert all(isinstance(entry.cost, Decimal) for entry in result.breakdown)
    assert all(isinstance(entry.hourly_rate, Decimal) for entry in result.breakdown)


def test_zero_attendees_total_zero_and_empty_breakdown():
    result = calculate("60", [])
    assert result.total == Decimal("0.00")
    assert result.breakdown == ()


def test_zero_duration_total_zero_with_one_entry_per_attendee():
    result = calculate("0", ["100", "80"])
    assert result.total == Decimal("0.00")
    assert [entry.cost for entry in result.breakdown] == [Decimal("0"), Decimal("0")]


def test_negative_duration_names_duration():
    with pytest.raises(InvalidInputError) as caught:
        calculate("-30", ["100"])
    assert caught.value.field == "duration"
    assert "duration" in str(caught.value)


def test_negative_rate_names_the_offending_rate():
    with pytest.raises(InvalidInputError) as caught:
        calculate("30", ["100", "-80"])
    assert caught.value.field == "rate 2"
    assert "rate 2" in str(caught.value)


def test_non_numeric_rate_names_the_offending_rate():
    with pytest.raises(InvalidInputError) as caught:
        calculate("30", ["100", "eighty"])
    assert caught.value.field == "rate 2"
    assert "rate 2" in str(caught.value)


def test_non_numeric_duration_names_duration():
    with pytest.raises(InvalidInputError) as caught:
        calculate("half an hour", ["100"])
    assert caught.value.field == "duration"
    assert "duration" in str(caught.value)


def test_not_a_number_rate_is_rejected():
    with pytest.raises(InvalidInputError) as caught:
        calculate("30", ["nan"])
    assert caught.value.field == "rate 1"


def test_invalid_input_is_not_coerced_to_a_default():
    with pytest.raises(InvalidInputError):
        calculate("60", ["100", ""])
