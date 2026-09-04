# Changelog

## Unreleased

- Add CLAUDE.md, docs/, scenarios/, CHANGELOG.md and a CI workflow.

## 2026-09-03

- Fix startup crash on Plotly 6 (`scatter_mapbox` removed upstream).
- Add `tests/test_baseline.py`.
- Add `greenland_ree_deposits.csv`, `dashboard.jsx`, both lens documents and LICENSE.
- Tag `bench-baseline`.

## 2026-01-16

- Add React port of the Overview tab (`dashboard.jsx`).
- Fix sidebar rendering with Streamlit's default grey background.

## 2026-01-14

- Rebuild as an advanced Streamlit app: four tabs, scenario modelling, deposit comparison radar.
- Embed deposit data in `app.py` (temporary).
- Fix `ModuleNotFoundError` on Streamlit Cloud by adding `plotly` to requirements.
- Remove `coloraxis_colorbar` customisation that raised on current Plotly.

## 2026-01-13

- Port from Dash to Streamlit for free hosting.

## 2026-01-12

- Initial commit: README, dataset, five-lens methodology.
