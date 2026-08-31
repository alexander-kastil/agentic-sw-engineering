# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "qrcode[pil]>=8.0",
# ]
# ///

import argparse
import json
import pathlib

import qrcode

LEVELS = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="scripts/generate_qr_batch.py",
        description="Render one PNG QR code per entry in a manifest file.",
        epilog=(
            "Examples:\n"
            "  uv run scripts/generate_qr_batch.py --manifest links.json --out-dir out --dry-run\n"
            "  uv run scripts/generate_qr_batch.py --manifest links.json --out-dir out --box-size 12\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--manifest", required=True, help="JSON file: a list of {slug, url} objects")
    parser.add_argument("--out-dir", required=True, help="Directory the PNG files are written to")
    parser.add_argument("--box-size", type=int, default=10, help="Pixels per QR module (default: 10)")
    parser.add_argument("--border", type=int, default=4, help="Quiet-zone width in modules (default: 4)")
    parser.add_argument(
        "--error-correction",
        choices=["L", "M", "Q", "H"],
        default="M",
        help="Recovery capacity: L=7%%, M=15%%, Q=25%%, H=30%% (default: M)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report the planned files without writing them")
    return parser


def main():
    args = build_parser().parse_args()
    entries = json.loads(pathlib.Path(args.manifest).read_text(encoding="utf-8"))
    out_dir = pathlib.Path(args.out_dir)
    written = []

    for entry in entries:
        target = out_dir / f"{entry['slug']}.png"
        if not args.dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
            code = qrcode.QRCode(
                box_size=args.box_size,
                border=args.border,
                error_correction=LEVELS[args.error_correction],
            )
            code.add_data(entry["url"])
            code.make(fit=True)
            code.make_image(fill_color="black", back_color="white").save(target)
        written.append({"slug": entry["slug"], "url": entry["url"], "path": target.as_posix()})

    print(json.dumps({"count": len(written), "dry_run": args.dry_run, "files": written}, indent=2))


if __name__ == "__main__":
    main()
