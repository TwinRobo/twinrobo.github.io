"""Copy the TwinRobo Benchmark's results into the site: ``docs/benchmark/results.md``.

    python tools/sync_benchmark.py [--bench ~/git/TwinRobo-Benchmark]

The benchmark's repository is private for now, so its report is copied here (a snapshot,
stamped with the benchmark commit it comes from) instead of read at build time. Re-run it
and commit the page after the benchmark's results change.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "docs" / "benchmark" / "results.md"

BANNER = """# Results

!!! warning "Simulation only: these rank digital twins, not yet the real cameras"
    Every catalog lens is a surrogate (a published design scaled to the camera's focal
    length and f-number; vendors publish no prescriptions), and sensor noise is not
    simulated. Differences between cameras that survive the *framed* and *optics only*
    conditions are mostly within the 95 % intervals. Grounding mostly reflects how the
    model handles each image's size and aspect, not the optics. The VLA column covers six
    cameras, run with two TwinRobo-Core versions (see [Findings](index.md)).

Benchmark commit `{bench}` · TwinRobo-Core `{core}` · copied {date}.
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bench", type=Path, default=Path.home() / "git" / "TwinRobo-Benchmark")
    a = ap.parse_args()
    md = (a.bench / "results" / "benchmark.md").read_text()
    core = re.search(r"- TwinRobo-Core: ([0-9a-f+dirty, ]+)", md)
    # the report's own title and intro paragraph are replaced by the banner
    body = md.split("\n", 1)[1]
    body = re.sub(r"\A\s*Each row is.*?\n\n", "", body, flags=re.S)
    # repository-internal instructions do not apply on the site
    body = re.sub(r"\nRebuild: `\./run_all\.sh`.*\Z", "\n", body, flags=re.S)
    body = body.replace("(closed loop; `src/vla`)", "(closed loop)")
    body = body.replace("### ", "## ", 3)  # the three condition tables are sections here
    head = BANNER.format(
        bench=git(a.bench, "rev-parse", "--short", "HEAD"),
        core=core.group(1).strip() if core else "?",
        date=git(a.bench, "log", "-1", "--format=%cs"),
    )
    if re.search(r"/home/|shij0c", body):
        raise SystemExit("the report names a local path: fix the benchmark's report first")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(head + "\n" + body.lstrip())
    print("wrote", OUT.relative_to(SITE))


if __name__ == "__main__":
    main()
