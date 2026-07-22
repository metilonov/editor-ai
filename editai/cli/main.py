from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from editai.cli.analyze import analyze_file
from editai.cli.doctor import doctor_main
from editai.cli.render import render_file


def main()->int:
    parser=argparse.ArgumentParser(prog="editai");sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    for name in ("analyze","render"):
        p=sub.add_parser(name);p.add_argument("video",type=Path);p.add_argument("--profile",default="dynamic");p.add_argument("--clips",type=int,default=3);p.add_argument("--duration",type=int,default=30)
        if name=="render":p.add_argument("--vertical",choices=["blur","crop","fit"],default="blur")
    args=parser.parse_args()
    if args.command=="doctor":return doctor_main()
    if args.command=="analyze":return asyncio.run(analyze_file(args.video,args.profile,args.clips,args.duration))
    return asyncio.run(render_file(args.video,args.profile,args.clips,args.duration,args.vertical))

if __name__=="__main__":raise SystemExit(main())
