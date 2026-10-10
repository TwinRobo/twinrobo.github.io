# twinrobo.github.io

The TwinRobo website: documentation, camera catalog, API reference and the camera
benchmark, published at **https://twinrobo.github.io/**. The code lives in
[TwinRobo-Core](https://github.com/TwinRobo/TwinRobo-Core).

## How it is built

MkDocs (Material) with TwinRobo-Core checked out beside it: the camera catalog page,
the contributing, CLA and license pages, and the API reference are generated from
Core's source at build time, so they follow Core without edits here.
`.github/workflows/pages.yml` builds on every push, daily, and by hand (Actions → Site →
Run workflow), and publishes to GitHub Pages.

```bash
pip install "mkdocs>=1.6,<2" "mkdocs-material>=9.5" "mkdocstrings[python]>=0.26" "mkdocs-gen-files>=0.5" pyyaml
TWINROBO_CORE=../TwinRobo-Core mkdocs serve      # or: git clone TwinRobo-Core into core/
```

## Layout

```
docs/                 the pages (written as if in TwinRobo-Core's docs/: links like ../CONTRIBUTING.md
                      resolve there; tools/docs/hooks.py turns them into site or GitHub links)
docs/benchmark/       the camera benchmark: findings (index.md) and results (results.md, copied)
overrides/            theme overrides (header with the tabs)
tools/docs/           page generator, link hook, catalog browser, playground renderers
tools/sync_benchmark.py   copies the benchmark's results into docs/benchmark/results.md
```

- **Benchmark results** come from the TwinRobo Benchmark (private for now):
  `python tools/sync_benchmark.py` copies its report, stamped with its commit; commit the
  page afterwards.
- **Playground images** (`docs/assets/playground/`) are rendered with TwinRobo-Core
  installed: `tools/docs/playground/render_mujoco.py`, `render_isaac.py` (inside Core's
  Isaac Sim container), then `assemble.py`.
