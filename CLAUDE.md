# Greenland REE Intelligence Dashboard

Streamlit dashboard ranking 15 Greenland rare earth deposits by strategic value to
a Western supply chain. Author: Maurice McDonald, Epoch Frameworks LLC.

## Run and test

```
pip install -r requirements.txt
streamlit run app.py          # dashboard at http://localhost:8501
python -m pytest -q tests     # must stay green
```

There is no build step. There is no Dash app; the Dash version was retired in
January 2026 (see docs/decisions.md).

## Layout

- `app.py` is the whole Streamlit app: data loading, sidebar filters, four tabs.
- `greenland_ree_deposits.csv` is the dataset of record. Columns are defined in
  `docs/data-dictionary.md`.
- `greenland-strategic-minerals-lens.md` defines the five-lens scoring model.
- `greenland-mineral-intelligence-skill.md` covers data sourcing and refresh.
- `dashboard.jsx` is a React port of the Overview tab. It carries its own copy of
  the data and is not wired to the CSV.
- `scenarios/` holds named what-if scenarios as JSON.
- `docs/decisions.md` records why things are the way they are. Read it before
  changing structure.

## Rules

1. `strategic_score` must equal the weighted sum of the five lens scores using the
   weights in the README and the lens document. Never hand-edit a composite score.
2. Keep the FRED-style look: white background, periwinkle `#8E9FD5` primary,
   charcoal `#2D3436` text. Do not introduce new colors without a reason.
3. `tests/` must pass after every change. Add a test when you add behavior.
4. Do not fetch from external services at app startup. The GEUS WFS pull is a
   separate script, not part of the dashboard.
5. Keep `README.md` truthful. If you add or remove a file, update the repository
   structure section in the same change.
6. Prefer editing `app.py` in place over splitting it into modules unless asked.
