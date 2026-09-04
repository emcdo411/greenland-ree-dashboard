# Decision log

Newest first. Each entry says what was decided, why, and what it cost us.

## 2026-09-03: Benchmark baseline

Decided: tag `bench-baseline` and add `tests/`, the CSV, the React port, the lens
documents and a LICENSE so the repo matches its README.
Why: the repo is being used as a coding-agent benchmark and needs a known-good
starting state.
Cost: none. The README still describes some things as "coming soon" that now exist.

## 2026-09-03: Plotly 6 compatibility

Decided: replace `px.scatter_mapbox` with `px.scatter_map` and `mapbox_style`
with `map_style`.
Why: Plotly 6 removed the Mapbox-based scatter API. The Streamlit Cloud deploy
was crashing on startup.
Cost: two lines. No visual change.

## 2026-01-16: React port of the Overview tab

Decided: build `dashboard.jsx` as a standalone React component with its own copy
of the data.
Why: to have a portfolio piece that does not depend on Streamlit Cloud.
Cost: two copies of the same data that can drift. Nobody has reconciled them
since.

## 2026-01-14: Embed the data in app.py

Decided: hardcode the 15 deposits inside `load_data()` instead of reading the CSV.
Why: Streamlit Cloud's first deploy could not find the CSV and it was faster to
inline the data than to debug paths at midnight.
Cost: the CSV is now decorative. Edits to it do nothing. This was meant to be
temporary.

## 2026-01-14: strategic_score typed by hand

Decided: enter the composite score directly rather than compute it.
Why: the lens scores were being tuned live during the DFW Plotly meetup and the
composite was easier to eyeball.
Cost: the numbers no longer agree with the documented weights. Tanbreez shows 80
but computes to 81.3; Kvanefjeld shows 52 but computes to 57.3.

## 2026-01-13: Streamlit instead of Dash

Decided: retire the Dash version and rebuild in Streamlit.
Why: Streamlit Cloud hosts for free with a GitHub link; the Dash version needed
paid hosting and a callbacks rewrite for every new filter.
Cost: lost Dash's finer layout control. The sidebar CSS took several attempts to
override Streamlit defaults.

## 2026-01-12: Five-lens scoring model

Decided: weight geology at 0.25, regulatory 0.20, ownership 0.20, infrastructure
0.15, geopolitical 0.20.
Why: geology gates everything else, but a deposit nobody can permit or ship is
worth little, so the four non-geological lenses together carry 0.75.
Cost: the weights are judgment, not fitted. Sensitivity to the regulatory weight
is the most contested choice.
