# Greenland Strategic Minerals Lens

Analytical framework behind the strategic_score used in this repository.
Author: Maurice McDonald, Epoch Frameworks LLC.

## Purpose

Rank Greenland rare earth deposits by their usefulness to a Western supply chain
that wants to reduce dependence on Chinese processing, not by geology alone.

## The five lenses

| Lens | Weight | What it measures | Score drivers |
| --- | --- | --- | --- |
| Geological | 0.25 | Is there enough of the right material? | Resource tonnage, TREO grade, heavy REE share |
| Regulatory | 0.20 | Can it legally be mined? | Permit status, uranium content vs the 2021 ban (100 ppm threshold), license history |
| Ownership | 0.20 | Who controls it? | Western vs Chinese equity, state involvement, operator track record |
| Infrastructure | 0.15 | Can it physically get to market? | Port distance, ice-free months, power, road access |
| Geopolitical | 0.20 | Does anyone with money and power want it built? | US, EU, Danish and Greenlandic policy alignment, offtake interest |

Each lens is scored 0 to 100. The composite is:

```
strategic_score = 0.25 * geological
                + 0.20 * regulatory
                + 0.20 * ownership
                + 0.15 * infrastructure
                + 0.20 * geopolitical
```

## Scoring rules

- A deposit above the 100 ppm uranium threshold caps at 40 on the regulatory lens
  while the ban stands.
- Any Chinese equity stake above 5 percent caps the ownership lens at 60.
- Port distance beyond 200 km caps infrastructure at 40 regardless of season.
- Lens scores are judgment calls anchored to public filings; they are not measurements.

## Categories

| strategic_score | Category |
| --- | --- |
| 0 to 40 | Low |
| 41 to 60 | Medium |
| 61 to 80 | High |
| 81 to 100 | Very High |

## Known limitations

Ownership data lags company filings by one to two quarters. Regulatory scores
assume the uranium ban remains in force. The scenario tab in the dashboard exists
to relax those assumptions one at a time.
