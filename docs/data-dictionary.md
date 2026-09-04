# Data dictionary: greenland_ree_deposits.csv

One row per deposit, 15 rows. Column order is fixed; the app and the React port
both depend on it.

| Column | Type | Units | Meaning | Source |
| --- | --- | --- | --- | --- |
| deposit_name | text | | Common name used in filings and GEUS records | GEUS |
| latitude | number | decimal degrees | Approximate deposit centroid | GEUS |
| longitude | number | decimal degrees | Negative is west | GEUS |
| resource_mt | number | million tonnes | Total resource, all categories combined (measured, indicated, inferred) | Company filings |
| treo_grade_pct | number | percent | Total rare earth oxide grade | Company filings |
| heavy_ree_pct | number | percent of TREO | Share of heavy rare earths (Dy, Tb, Y and others) in the TREO | Company filings |
| owner | text | | Current licence holder or operator | Greenland Mineral Authority |
| chinese_stake_pct | number | percent | Latest disclosed Chinese equity share in the licence holder. 0 if none | Company filings |
| status | text | | One of: Advancing, Blocked, Permitted, Exploration, Prospect, Abandoned, Reserved, Multiple, Uncertain, Closed, PGE Focus | Analyst |
| uranium_ppm | number | parts per million | Typical uranium content of the ore. The 2021 ban applies above 100 ppm | Company filings, GEUS |
| strategic_score | number | 0 to 100 | Composite; should be the weighted sum of the five lens scores below | Derived |
| geological_score | number | 0 to 100 | Lens 1, weight 0.25 | Analyst |
| regulatory_score | number | 0 to 100 | Lens 2, weight 0.20 | Analyst |
| ownership_score | number | 0 to 100 | Lens 3, weight 0.20 | Analyst |
| infrastructure_score | number | 0 to 100 | Lens 4, weight 0.15 | Analyst |
| geopolitical_score | number | 0 to 100 | Lens 5, weight 0.20 | Analyst |
| discovery_year | integer | year | First documented discovery | GEUS, literature |
| ice_free_months | integer | months | Months per year the nearest port is navigable | Analyst estimate |
| port_distance_km | number | kilometres | Straight-line distance to the nearest usable port | Analyst estimate |

## Derived columns the app adds at load time

| Column | Rule |
| --- | --- |
| ownership_type | "Chinese Exposure" if chinese_stake_pct > 0, else "Western Control" |
| uranium_status | "Blocked (>100 ppm)" if uranium_ppm > 100, else "Clear (<100 ppm)" |
| score_category | Low 0 to 40, Medium 41 to 60, High 61 to 80, Very High 81 to 100 |
| contained_treo_kt | resource_mt × treo_grade_pct / 100 × 1000 |
| contained_hree_kt | contained_treo_kt × heavy_ree_pct / 100 |

## Known data issues

- strategic_score values in the CSV were typed by hand in January 2026 and do not
  match the weighted formula. See docs/decisions.md, entry 2026-01-14.
- Ivigtut Area and Skaergaard are included for completeness; neither is primarily
  a rare earth deposit.
- Ownership figures for Kvanefjeld and Narsaq Area reflect Shenghe Resources'
  stake in Energy Transition Minerals and lag ASX filings by up to a quarter.
