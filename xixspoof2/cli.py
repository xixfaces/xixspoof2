import argparse, os, sys
from .loader import load_place_text
from .scanner import scan_xml
from .replacer import rewrite_place
from .uploader import upload_all
from .logutil import info, warn, error

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--file",required=True)
    ap.add_argument("--output")
    ap.add_argument("--cookie")
    ap.add_argument("--group",type=int)
    ap.add_argument("--threads",type=int,default=5)
    ap.add_argument("--dry-run",action="store_true")
    args=ap.parse_args()

    if not os.path.isfile(args.file):
        error("File not found")
        sys.exit(1)

    cookie=args.cookie or os.getenv("RBLX_COOKIE")

    xml=load_place_text(args.file)
    info("Scanning…")
    ids=scan_xml(xml)

    info(f"Found {len(ids)} IDs")
    if args.dry_run:
        for i in sorted(ids,key=lambda x:int(x)): print(" -",i)
        sys.exit(0)

    if not cookie:
        error("No cookie provided")
        sys.exit(1)

    id_map,errors=upload_all(cookie,sorted(ids,key=lambda x:int(x)),args.group,args.threads)

    out=args.output or (os.path.splitext(args.file)[0]+".relinked.rbxlx")
    new_xml=rewrite_place(xml,id_map)
    with open(out,"w",encoding="utf-8") as f: f.write(new_xml)
    info(f"Wrote: {out}")
