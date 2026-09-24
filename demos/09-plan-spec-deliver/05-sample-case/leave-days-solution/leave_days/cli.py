import argparse
import sys

from leave_days.calculator import InvalidInputError, LeaveCharge, charge_leave, parse_holidays


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="leave_days", description="Working days a leave request deducts from the allowance.")
    parser.add_argument("start", help="first day of leave, YYYY-MM-DD")
    parser.add_argument("end", help="last day of leave, YYYY-MM-DD, inclusive")
    parser.add_argument("--holidays", required=True, help="holiday file supplied by HR")
    return parser


def format_report(charge: LeaveCharge) -> str:
    lines = [f"Leave: {charge.start.isoformat()} to {charge.end.isoformat()}"]
    lines += [f"{item.year}: {item.days:.1f} days" for item in charge.per_year]
    lines.append(f"Total: {charge.total:.1f} days")
    return "\n".join(lines)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        with open(args.holidays, encoding="utf-8") as handle:
            calendar = parse_holidays(handle.readlines())
    except OSError:
        print(f"error: holidays file cannot be read: {args.holidays}", file=sys.stderr)
        return 1
    try:
        charge = charge_leave(args.start, args.end, calendar)
    except InvalidInputError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(format_report(charge))
    return 0
