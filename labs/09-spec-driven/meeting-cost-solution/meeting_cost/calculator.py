from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

MINUTES_PER_HOUR = Decimal(60)
TOTAL_EXPONENT = Decimal("0.01")


class InvalidInputError(ValueError):
    def __init__(self, field, message):
        super().__init__(message)
        self.field = field


@dataclass(frozen=True)
class AttendeeCost:
    hourly_rate: Decimal
    cost: Decimal


@dataclass(frozen=True)
class MeetingCost:
    duration_minutes: Decimal
    breakdown: tuple[AttendeeCost, ...]
    total: Decimal


def _to_decimal(value, field):
    try:
        amount = Decimal(str(value).strip())
    except InvalidOperation:
        raise InvalidInputError(field, f"{field} is not a number: {value!r}") from None
    if not amount.is_finite():
        raise InvalidInputError(field, f"{field} is not a number: {value!r}")
    return amount


def parse_duration(value):
    duration = _to_decimal(value, "duration")
    if duration < 0:
        raise InvalidInputError("duration", f"duration must not be negative: {duration}")
    return duration


def parse_rate(value, position):
    field = f"rate {position}"
    rate = _to_decimal(value, field)
    if rate < 0:
        raise InvalidInputError(field, f"{field} must not be negative: {rate}")
    return rate


def round_total(amount):
    return amount.quantize(TOTAL_EXPONENT, rounding=ROUND_HALF_UP)


def calculate(duration_minutes, hourly_rates):
    duration = parse_duration(duration_minutes)
    rates = [parse_rate(rate, position) for position, rate in enumerate(hourly_rates, start=1)]
    hours = duration / MINUTES_PER_HOUR
    breakdown = tuple(AttendeeCost(rate, rate * hours) for rate in rates)
    total = sum((entry.cost for entry in breakdown), Decimal(0))
    return MeetingCost(duration, breakdown, round_total(total))
