# Greenland Mineral Intelligence Skill

Technical notes for pulling and preparing the data behind this dashboard.

## Sources

| Source | What it provides | How to access |
| --- | --- | --- |
| GEUS Greenland Mineral Resources Portal (greenmin.gl) | Mineral occurrences, drill holes, geochemistry | Free WFS endpoint at https://data.geus.dk/geusmap/ows/ |
| USGS MRDS | Global deposit records | Free bulk download |
| Greenland Mineral Authority (govmin.gl) | Licence status and holders | Free, manual lookup |
| Company filings (SEC, SEDAR, ASX) | Resource estimates, ownership, financing | Public |

## Pulling occurrences from GEUS

```python
import requests
import geopandas as gpd
from io import BytesIO

WFS_URL = "https://data.geus.dk/geusmap/ows/"
params = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeName": "greenland_portal:mineral_occurrences",
    "outputFormat": "application/json",
}
gdf = gpd.read_file(BytesIO(requests.get(WFS_URL, params=params).content))
ree = gdf[gdf["commodity"].str.contains("REE|rare earth", case=False, na=False)]
```

## Building greenland_ree_deposits.csv

One row per deposit with these columns, in this order:

```
deposit_name, latitude, longitude, resource_mt, treo_grade_pct, heavy_ree_pct,
owner, chinese_stake_pct, status, uranium_ppm, strategic_score,
geological_score, regulatory_score, ownership_score, infrastructure_score,
geopolitical_score, discovery_year, ice_free_months, port_distance_km
```

Rules:
- resource_mt is total resource in million tonnes, all categories combined.
- treo_grade_pct is percent total rare earth oxide.
- chinese_stake_pct is the latest disclosed Chinese equity share, 0 if none.
- The five lens scores follow greenland-strategic-minerals-lens.md.
- strategic_score should be derived from the lens scores, not typed by hand.

## Refresh cadence

GEUS updates continuously. Company filings quarterly. Re-score ownership and
regulatory lenses after each quarterly filing cycle.
