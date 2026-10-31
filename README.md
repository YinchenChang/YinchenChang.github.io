# yinchenchang.github.io

Source for Andy Chang's public research site: essays and the AI Compute Investment Map. Built with GitHub Pages (Jekyll, minima theme).

- `index.md`, `about.md`, `writing.md` — pages
- `_posts/` — essays (`YYYY-MM-DD-title.md`)
- `map/index.md` — the map page (layers in `_data/map.yml`)
- `coverage/`, `zh/coverage/`, `stocks/<ticker>/` — company coverage, generated weekly by `tools/build_coverage.py` from the AI Investment Map (`company-models/markets/invest_map/dist/data.json`)
- `models/<folder>.html` — mirrored model pages (non-Taiwan, non-private only; written by `tools/build_coverage.py`)

No personal context. Company data and ratings come from the AI Investment Map. **Taiwan-listed stocks never show a target price** (nor upside, pessimistic-case price, or the model page); `tools/build_coverage.py` stops the build if one appears (Andy 2026-10-31). Items dated within 7 days show a blinking NEW badge (`data-new` attribute).
