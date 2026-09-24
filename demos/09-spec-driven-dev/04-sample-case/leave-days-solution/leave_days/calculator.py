from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

FULL_DAY = Decimal("1")
HALF_DAY = Decimal("0.5")
WEEKEND = {5, 6}


class InvalidInputError(ValueError):
    def __init__(self, field: str, message: str):
        super().__init__(f"{field} {message}")
        self.field = field


@dataclass(frozen=True)
class HolidayCalendar:
    days_off: dict[date, Decimal]
    years: frozenset[int]


@dataclass(frozen=True)
class YearCharge:
    year: int
    days: Decimal


@dataclass(frozen=True)
class LeaveCharge:
    start: date
    end: date
    per_year: tuple[YearCharge, ...]
    total: Decimal


def parse_date(value: str, field: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise InvalidInputError(field, f"is not a date in YYYY-MM-DD form: {value!r}") from None


def parse_holidays(lines) -> HolidayCalendar:
    days_off: dict[date, Decimal] = {}
    for number, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            continue
        field = f"holidays line {number}"
        parts = line.split()
        if len(parts) > 2 or (len(parts) == 2 and parts[1] != "half"):
            raise InvalidInputError(field, f"is not 'YYYY-MM-DD' or 'YYYY-MM-DD half': {line!r}")
        day = parse_date(parts[0], field)
        if day in days_off:
            raise InvalidInputError(field, f"repeats {day.isoformat()}")
        days_off[day] = HALF_DAY if len(parts) == 2 else FULL_DAY
    return HolidayCalendar(days_off, frozenset(day.year for day in days_off))


def working_fraction(day: date, calendar: HolidayCalendar) -> Decimal:
    if day.weekday() in WEEKEND:
        return Decimal("0")
    return FULL_DAY - calendar.days_off.get(day, Decimal("0"))


def charge_leave(start: str, end: str, calendar: HolidayCalendar) -> LeaveCharge:
    first = parse_date(start, "start")
    last = parse_date(end, "end")
    if last < first:
        raise InvalidInputError("end", f"must not be before start: {last.isoformat()}")
    for year in range(first.year, last.year + 1):
        if year not in calendar.years:
            raise InvalidInputError("holidays", f"has no entries for {year}")
    totals: dict[int, Decimal] = {}
    day = first
    while day <= last:
        totals[day.year] = totals.get(day.year, Decimal("0")) + working_fraction(day, calendar)
        day += timedelta(days=1)
    per_year = tuple(YearCharge(year, days) for year, days in sorted(totals.items()))
    return LeaveCharge(first, last, per_year, sum((charge.days for charge in per_year), Decimal("0")))
