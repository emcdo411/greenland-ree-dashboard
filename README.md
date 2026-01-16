# 🌍 Greenland Rare Earth Intelligence Dashboard

[![Plotly](https://img.shields.io/badge/Built%20with-Plotly-3F4F75?style=flat&logo=plotly)](https://plotly.com/)
[![GEUS Data](https://img.shields.io/badge/Data-GEUS%20Portal-blue)](https://www.greenmin.gl/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Strategic mineral intelligence for the Arctic's most contested resource frontier.**

![Dashboard Preview](https://img.shields.io/badge/Status-Active%20Development-brightgreen)

---

## 📊 Overview

This project provides **open-source intelligence tools** for analyzing Greenland's rare earth element (REE) deposits — critical minerals that power everything from electric vehicles to missile guidance systems.

With China controlling ~85% of global REE processing and the US dependent on rare earths for 77.7% of DoD weapons systems, Greenland represents the largest Western-accessible alternative. This dashboard makes that strategic landscape visible.

### What This Project Does

| Capability | Description |
|------------|-------------|
| **Data Ingestion** | Pulls mineral occurrence data from GEUS (Geological Survey of Denmark & Greenland) via WFS |
| **Strategic Scoring** | Evaluates deposits across 5 dimensions: Geological, Regulatory, Ownership, Infrastructure, Geopolitical |
| **Ownership Tracking** | Monitors Chinese vs. Western equity stakes in Greenland mining projects |
| **FRED-Style Visualization** | Professional dashboard specs using Plotly with signature periwinkle (#8E9FD5) palette |

---

## 🗺️ Key Findings

| Deposit | Strategic Score | Status | Chinese Exposure |
|---------|-----------------|--------|------------------|
| **Tanbreez** | 80/100 ⭐ | Advancing (US-owned) | 0% |
| **Kvanefjeld** | 52/100 ⚠️ | Blocked (Uranium ban) | 9.21% |
| **Sarfartoq** | 61/100 | Permitted | 0% |
| **Motzfeldt** | 48/100 | Early exploration | 0% |

**Key Insight:** Tanbreez, with 30% heavy REE content (highest globally) and zero Chinese exposure, is the most strategically valuable deposit for Western supply chain diversification.

---

## 📁 Repository Structure

```
greenland-ree-dashboard/
│
├── greenland-mineral-intelligence-skill.md   # Technical framework for data ingestion
├── greenland-strategic-minerals-lens.md      # Analytical framework (5-lens methodology)
├── greenland_ree_deposits.csv                # Dataset: 15 deposits with coordinates & scores
├── README.md                                 # You are here
│
└── (coming soon)
    ├── dashboard.jsx                         # Interactive React/Plotly dashboard
    ├── data_pipeline.py                      # GEUS WFS data fetcher
    └── analysis_notebook.ipynb               # Jupyter exploration notebook
```

---

## 🔬 Methodology

### The Five Lenses

Each deposit is evaluated through five analytical perspectives:

```
STRATEGIC_SCORE = 
    (GEOLOGICAL × 0.25) +      # Resource size, grade, heavy REE %
    (REGULATORY × 0.20) +      # Permit status, uranium ban impact
    (OWNERSHIP × 0.20) +       # Western vs. Chinese control
    (INFRASTRUCTURE × 0.15) +  # Port access, power, ice-free season
    (GEOPOLITICAL × 0.20)      # US/EU/China strategic alignment
```

### Data Sources

| Source | Type | Access |
|--------|------|--------|
| [GEUS Greenland Portal](https://www.greenmin.gl/) | Mineral occurrences, drill holes, geochemistry | Free WFS API |
| [USGS MRDS](https://mrdata.usgs.gov/mrds/) | Global mineral deposit database | Free |
| Mining company filings | Resource estimates, ownership | SEC/SEDAR/ASX |
| [Greenland Mineral Authority](https://govmin.gl/) | License data, regulations | Free |

---

## 🚀 Quick Start

### Option 1: View the Data

```python
import pandas as pd

# Load the dataset
df = pd.read_csv('greenland_ree_deposits.csv')

# Top deposits by strategic score
print(df.sort_values('strategic_score', ascending=False)[['deposit_name', 'strategic_score', 'owner', 'chinese_stake_pct']].head())
```

### Option 2: Fetch Live Data from GEUS

```python
import requests
import geopandas as gpd
from io import BytesIO

WFS_URL = "https://data.geus.dk/geusmap/ows/"

params = {
    'service': 'WFS',
    'version': '2.0.0',
    'request': 'GetFeature',
    'typeName': 'greenland_portal:mineral_occurrences',
    'outputFormat': 'application/json'
}

response = requests.get(WFS_URL, params=params)
gdf = gpd.read_file(BytesIO(response.content))
print(f"Total mineral occurrences: {len(gdf)}")
```

### Option 3: Run the Dashboard (Coming Soon)

```bash
# Clone the repo
git clone https://github.com/emcdo411/greenland-ree-dashboard.git
cd greenland-ree-dashboard

# Install dependencies
pip install plotly pandas geopandas requests

# Run dashboard
python dashboard.py
```

---

## 📈 Sample Visualizations

### Strategic Score Comparison
```
Tanbreez     ████████████████████████████████████████ 80
Sarfartoq    ████████████████████████████████         61
Gardar South ███████████████████████████████          62
Kvanefjeld   ██████████████████████████               52
Motzfeldt    ████████████████████████                 48
```

### Ownership Breakdown
```
Western Control:  ████████████████████████████████████ 91%
Chinese Stakes:   ████                                  6%
Unknown:          ██                                    3%
```

---

## 🎯 Use Cases

| Audience | Application |
|----------|-------------|
| **Investment Analysts** | Due diligence on Greenland mining equities |
| **Policy Researchers** | Critical minerals supply chain analysis |
| **Journalists/OSINT** | Source-verified mapping for articles |
| **Government Agencies** | Strategic resource assessments |
| **Data Viz Community** | GIS + BI integration showcase |

---

## ⚠️ Limitations & Caveats

### What This Project CAN Do
✅ Map all documented mineral occurrences in Greenland  
✅ Filter and analyze rare earth deposits  
✅ Track ownership and regulatory status  
✅ Calculate strategic value scores  
✅ Visualize in FRED-style dashboards  

### What This Project CANNOT Do
❌ Predict undiscovered deposits  
❌ Access proprietary exploration data  
❌ Replace professional geological assessment  
❌ Provide real-time market data  

**Data Freshness:** GEUS data updates regularly; mining filings may lag 1-2 quarters.

---

## 🔗 Related Work

This project is part of a broader intelligence analysis on Greenland:

- **[The Greenland Paradox](https://claude.ai/public/artifacts/eab1b521-0bcb-4eea-a0a3-e2edb8668812)** — Interactive dashboard on European troop deployments
- **KenSight News Lens v3.5** — Multi-regional source triangulation methodology
- **DFW Plotly Meetup** — Where this analysis was first presented

---

## 👤 Author

**Maurice McDonald**  
Plotly Community Leader — DFW  
Enterprise BI & Analytics | Healthcare • Municipal • Intelligence Verticals

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/mauricemcdonald/)
[![Plotly](https://img.shields.io/badge/DFW%20Plotly-Meetup-3F4F75)](https://www.meetup.com/dfw-plotly/)

---

## 📜 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions welcome! Areas of interest:

- [ ] Interactive React/Plotly dashboard component
- [ ] Automated GEUS data pipeline
- [ ] Additional deposit research and scoring
- [ ] Jupyter notebook tutorials
- [ ] Translation to other languages

---

## 📚 References

1. GEUS (2026). *Greenland Mineral Resources Portal*. https://www.greenmin.gl/
2. USGS (2023). *Rare Earth Elements—Critical Minerals Review*. https://pubs.usgs.gov/
3. Government of Greenland (2021). *Act No. 20 on Uranium Mining Ban*. Inatsisartut.
4. Critical Metals Corp (2025). *Tanbreez Project Technical Report*. NASDAQ: CRML.
5. Energy Transition Minerals (2024). *Kvanefjeld Arbitration Update*. ASX: ETM.

---

<p align="center">
  <i>Built with 📊 Plotly and ☕ caffeine in Fort Worth, Texas</i>
</p>
