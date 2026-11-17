"""Fetch gitignored datasets from official sources or a GitHub Release mirror.

Run from the repository root:

    python scripts/fetch_data.py --list-sources
    python scripts/fetch_data.py --synthetic
    python scripts/fetch_data.py --aemo
    python scripts/fetch_data.py --from-release
    python scripts/fetch_data.py --solar

CSV and zip files stay out of git. `--from-release` unpacks the published
`data-v1` pack; `--solar` fetches only the Ausgrid zip.
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
RELEASE_PACK = (
    "https://github.com/dimnoll/nsw-time-series-forecasting/releases/download/data-v1/data-pack.zip"
)
RELEASE_SOLAR = (
    "https://github.com/dimnoll/nsw-time-series-forecasting/releases/download/data-v1/"
    "2012-2013.Solar.home.electricity.data.v2.zip"
)
SOLAR_ZIP_NAME = "2012-2013 Solar home electricity data v2.zip"
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
            f"Release download failed for data-pack.zip ({exc})"
        ) from exc
    with zipfile.ZipFile(pack) as archive:
        archive.extractall(ROOT)
    return pack


def fetch_solar(url: str) -> Path:
    dest = ROOT / "th-nsw-solar-home" / SOLAR_ZIP_NAME
    print(f"GET {url}")
    try:
        download(url, dest)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise SystemExit(
            f"Release download failed for the Ausgrid zip ({exc})"
        ) from exc
    return dest


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
    print(f"  zip:    {RELEASE_SOLAR}")
    print("  python scripts/fetch_data.py --solar")
    print("  writes th-nsw-solar-home/" + SOLAR_ZIP_NAME)
    print("  then run data_preprocess.py in that folder")
    print()
    print("GitHub Release pack (processed tables + the Ausgrid zip)")
    print(f"  {RELEASE_PACK}")
    print("  python scripts/fetch_data.py --from-release")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-sources", action="store_true")
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--aemo", action="store_true")
    parser.add_argument("--from-release", action="store_true")
    parser.add_argument("--solar", action="store_true")
    parser.add_argument("--release-url", default=RELEASE_PACK)
    parser.add_argument("--solar-url", default=RELEASE_SOLAR)
    args = parser.parse_args()

    if not any(
        [args.list_sources, args.synthetic, args.aemo, args.from_release, args.solar]
    ):
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
    if args.solar:
        dest = fetch_solar(args.solar_url)
        print(f"wrote {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
