import argparse, os, sys
from .loader import load_place_text
from .scanner import scan_xml
from .replacer import rewrite_place
from .uploader import upload_all
from .logutil import info, warn, error
from .version import __version__
from .cookies import load_cookie, save_cookie
from .eyeball import start_eyeball

def main():
    ap = argparse.ArgumentParser(description=f"xixspoof2 v{__version__}")
    ap.add_argument("--file", required=True, help="Path to .rbxlx or .rbxl")
    ap.add_argument("--output", help="Output .rbxlx (default: <name>.relinked.rbxlx)")
    ap.add_argument("--cookie", help="Your .ROBLOSECURITY (or env RBLX_COOKIE or cookie.txt)")
    ap.add_argument("--no-save-cookie", action="store_true", help="Do not write cookie.txt when using --cookie")
    ap.add_argument("--group", type=int, help="Group ID to upload into")
    ap.add_argument("--threads", type=int, default=2, help="Upload concurrency (1–3 recommended)")
    ap.add_argument("--dry-run", action="store_true", help="Scan only, do not upload/replace")
    ap.add_argument("--deep", action="store_true", help="Deep scan (include scripts/URLs/bare IDs)")
    args = ap.parse_args()

    if not os.path.isfile(args.file):
        error(f"File not found: {args.file}")
        sys.exit(1)

    try:
        xml = load_place_text(args.file)
    except Exception as e:
        error(str(e)); sys.exit(2)

    stop_eye = start_eyeball("Scanning for animations…")
    ids = scan_xml(xml, deep=args.deep)
    stop_eye.set()

    info(f"Found {len(ids)} unique ID(s).")

    if not ids:
        warn("No animation IDs detected. If this is a .rbxl, try saving as .rbxlx in Studio and re-run (or use --deep).")
        sys.exit(0)

    if args.dry_run:
        for i in sorted(ids, key=lambda x: int(x)):
            print(f" - {i}")
        sys.exit(0)

    cookie = load_cookie(args.cookie)
    if not cookie:
        error("Missing .ROBLOSECURITY. Use --cookie or set env RBLX_COOKIE, or create cookie.txt.")
        sys.exit(2)
    if args.cookie and not args.no_save_cookie:
        save_cookie(args.cookie)

    id_map, errors = upload_all(cookie, sorted(ids, key=lambda x: int(x)), args.group, args.threads)
    if not id_map:
        error("No animations re-uploaded. Aborting rewrite.")
        sys.exit(3)

    base, _ = os.path.splitext(args.file)
    out = args.output or f"{base}.relinked.rbxlx"
    info(f"Rewriting place with {len(id_map)} replacement(s)…")
    new_xml = rewrite_place(xml, id_map)
    with open(out, "w", encoding="utf-8") as f:
        f.write(new_xml)
    info(f"Done. Wrote: {out}")
