import argparse, os, sys
from .loader import load_place_text
from .scanner import scan_xml
from .replacer import rewrite_place
from .uploader import upload_all
from .logutil import info, warn, error
from .version import __version__
def main():
    ap=argparse.ArgumentParser(description=f"xixspoof2 v{__version__}")
    ap.add_argument("--file",required=True)
    ap.add_argument("--output")
    ap.add_argument("--cookie")
    ap.add_argument("--group",type=int)
    ap.add_argument("--threads",type=int,default=5)
    ap.add_argument("--dry-run",action="store_true")
    args=ap.parse_args()
    if not os.path.isfile(args.file):
        error(f"File not found: {args.file}"); sys.exit(1)
    try:
        xml=load_place_text(args.file)
    except Exception as e:
        error(str(e)); sys.exit(2)
    info(f"Loaded: {args.file}")
    info("Scanning for animations…")
    ids=scan_xml(xml)
    info(f"Found {len(ids)} unique ID(s).")
    if not ids:
        warn("No animation IDs detected. If this is a .rbxl, try saving as .rbxlx in Studio and re-run.")
        sys.exit(0)
    if args.dry_run:
        for i in sorted(ids, key=lambda x:int(x)): print(f" - {i}")
        sys.exit(0)
    cookie=args.cookie or os.getenv("RBLX_COOKIE")
    if not cookie:
        error("Missing .ROBLOSECURITY. Use --cookie or set env RBLX_COOKIE."); sys.exit(2)
    id_map, errors = upload_all(cookie, sorted(ids, key=lambda x:int(x)), args.group, args.threads)
    if not id_map:
        error("No animations re-uploaded. Aborting rewrite."); sys.exit(3)
    base,_=os.path.splitext(args.file)
    out=args.output or f"{base}.relinked.rbxlx"
    info(f"Rewriting place with {len(id_map)} replacement(s)…")
    new_xml=rewrite_place(xml, id_map)
    with open(out,"w",encoding="utf-8") as f: f.write(new_xml)
    info(f"Done. Wrote: {out}")
if __name__=="__main__":
    main()
