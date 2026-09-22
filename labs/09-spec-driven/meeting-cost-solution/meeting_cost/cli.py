import argparse
import sys

from meeting_cost.calculator import InvalidInputError, calculate


def build_parser():
    parser = argparse.ArgumentParser(
        prog="meeting_cost",
        description="Calculate what a meeting costs in salary time.",
    )
    parser.add_argument("duration", help="meeting length in minutes")
    parser.add_argument("rates", nargs="*", help="hourly rate of one attendee")
    return parser


def format_report(result):
    lines = [
        f"Duration: {result.duration_minutes} minutes",
        f"Attendees: {len(result.breakdown)}",
    ]
    for position, entry in enumerate(result.breakdown, start=1):
        lines.append(f"Attendee {position} at {entry.hourly_rate} per hour: {entry.cost}")
    lines.append(f"Total: {result.total}")
    return "\n".join(lines)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = calculate(args.duration, args.rates)
    except InvalidInputError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(format_report(result))
    return 0
