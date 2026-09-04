# Scenarios

Named what-if adjustments to the five lens scores. Each file describes one
scenario. The dashboard's scenario tab currently hardcodes its own options and
does not read these files yet; wiring them up is an open item.

Schema:

```
{
  "name":        short label shown in the UI,
  "description": one or two sentences,
  "adjustments": [
    { "when": { "column": ..., "op": ">", "value": ... },
      "set":  { "column": ..., "delta": ... } }
  ]
}
```

Adjustments apply in order. `when` filters rows; `set` adds `delta` to the
named lens column for those rows. After all adjustments, every lens column is
clipped to 0 to 100 and strategic_score is recomputed with the standard weights.
