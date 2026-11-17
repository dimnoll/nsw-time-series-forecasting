"""Fetch gitignored datasets from official sources or a GitHub Release mirror.

Run from the repository root:

    python scripts/fetch_data.py --list-sources
    python scripts/fetch_data.py --synthetic
    python scripts/fetch_data.py --aemo
    python scripts/fetch_data.py --from-release

CSV and zip files stay out of git. After a Release exists, `--from-release`
unpacks `data-pack.zip` into the same paths the training scripts already use.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
AEMO_STUB = "https://www.aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_"
AEMO_MONTHS = [
    f"{year}{month:02d}"
    for year, month in (
        (2012, 7), (2012, 8), (2012, 9), (2012, 10), (2012, 11), (2012, 12),
        (2013, 1), (2013, 2), (2013, 3), (2013, 4), (2013, 5), (2013, 6),
    )
]
RELEASE_ASSET = (
    "https://github.com/dimnoll/nsw-time-series-forecasting/releases/latest/download/data-pack.zip"
)
USER_AGENT = "nsw-time-series-forecasting/0.1 (+https://github.com/dimnoll/nsw-time-series-forecasting)"


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=120) as response:
        dest.write_bytes(response.read())


def generate_synthetic() -> Path:
    script = ROOT / "tf-syndt" / "generate_synthetic_data.py"
    spec = importlib.util.spec_from_file_location("generate_synthetic_data", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    frame = module.generate_synthetic_load_data(n_samples=7200, freq="15min")
    out = ROOT / "tf-syndt" / "synthetic_load_15min_7200.csv"
    frame.to_csv(out, float_format="%.3f")
    return out


def fetch_aemo() -> list[Path]:
    dest_dir = ROOT / "th-nsw-demand-price" / "data_csvs"
    dest_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for month in AEMO_MONTHS:
        name = f"PRICE_AND_DEMAND_{month}_NSW1.csv"
        url = f"{AEMO_STUB}{month}_NSW1.csv"
        dest = dest_dir / name
        print(f"GET {url}")
        try:
            download(url, dest)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise SystemExit(f"AEMO download failed for {name}: {exc}") from exc
        written.append(dest)
    return written


def fetch_release(url: str) -> Path:
    pack = ROOT / "data-pack.zip"
    print(f"GET {url}")
    try:
        download(url, pack)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise SystemExit(
            "Release download failed. Publish `data-pack.zip` on GitHub Releases, "
            f"or pass --release-url. ({exc})"
        ) from exc
    with zipfile.ZipFile(pack) as archive:
        archive.extractall(ROOT)
    return pack


def list_sources() -> None:
    print("Synthetic load (generated, not a third-party dataset)")
    print("  python scripts/fetch_data.py --synthetic")
    print("  writes tf-syndt/synthetic_load_15min_7200.csv")
    print()
    print("AEMO aggregated price and demand (NSW1, Jul 2012 – Jun 2013)")
    print("  portal: https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data")
    print(f"  files:  {AEMO_STUB}YYYYMM_NSW1.csv")
    print("  python scripts/fetch_data.py --aemo")
    print("  then:   python th-nsw-demand-price/data_preprocess.py")
    print()
    print("Ausgrid solar home electricity data (2012–2013, CC BY 4.0)")
    print("  origin: Ausgrid; historically listed on Data.NSW")
    print("  paper:  Ratnam et al., International Journal of Sustainable Energy, 2017")
    print("  place `2012-2013 Solar home electricity data v2.zip` (or the unzipped CSV)")
    print("  in th-nsw-solar-home/, then run data_preprocess.py there")
    print("  Ausgrid no longer hosts the zip; this working tree may hold a CC BY 4.0")
    print("  snapshot. The public mirror is a GitHub Release, not git.")
    print()
    print("GitHub Release mirror (optional, after data-v1 exists)")
    print(f"  {RELEASE_ASSET}")
    print("  python scripts/fetch_data.py --from-release")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-sources", action="store_true")
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--aemo", action="store_true")
    parser.add_argument("--from-release", action="store_true")
    parser.add_argument("--release-url", default=RELEASE_ASSET)
    args = parser.parse_args()

    if not any([args.list_sources, args.synthetic, args.aemo, args.from_release]):
        list_sources()
        return 0

    if args.list_sources:
        list_sources()
    if args.synthetic:
        out = generate_synthetic()
        print(f"wrote {out.relative_to(ROOT)}")
    if args.aemo:
        for path in fetch_aemo():
            print(f"wrote {path.relative_to(ROOT)}")
    if args.from_release:
        pack = fetch_release(args.release_url)
        print(f"unpacked {pack.relative_to(ROOT)} into {ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
