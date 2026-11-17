"""Zip gitignored datasets into data-pack.zip for a GitHub Release.

Run from the repository root after the files exist locally:

    python scripts/pack_data.py

The published pack is:
https://github.com/dimnoll/nsw-time-series-forecasting/releases/download/data-v1/data-pack.zip
Training scripts still read the unpacked paths.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data-pack.zip"

MEMBERS = [
    ROOT / "tf-syndt" / "synthetic_load_15min_7200.csv",
    ROOT / "th-nsw-solar-home" / "2012-2013 Solar home electricity data v2.zip",
    ROOT / "th-nsw-solar-home" / "2012-2013 Solar home electricity data v2.csv",
    ROOT / "th-nsw-solar-home" / "data_daily_long.csv",
    ROOT / "th-nsw-demand-price" / "data_processed" / "nsw_halfhour_201207_201306.csv",
    ROOT / "th-nsw-demand-price" / "data_processed" / "nsw_daily_201207_201306.csv",
]


def extra_aemo() -> list[Path]:
    folder = ROOT / "th-nsw-demand-price" / "data_csvs"
    if not folder.is_dir():
        return []
    return sorted(folder.glob("PRICE_AND_DEMAND_*.csv"))


def main() -> int:
    files = [path for path in MEMBERS + extra_aemo() if path.is_file()]
    if not files:
        print("no dataset files found; run scripts/fetch_data.py first", file=sys.stderr)
        return 1

    if OUT.exists():
        OUT.unlink()

    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
            print(f"add {path.relative_to(ROOT)}")

    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
