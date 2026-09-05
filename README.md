# PulseScan
**Binance Agent OS Mini Hackathon — Track A: Data & Analysis**

PulseScan is an AI agent that scans a market watchlist for **statistical anomalies and shifting correlations** — catching moves that a single-asset view would miss, and writing them up as a market intelligence report.

Where InsightDesk answers "how healthy is my portfolio?", PulseScan answers "what's unusual happening across the market right now?" — a market-wide lens rather than a holdings-based one.

## What it does

1. **Data Ingestion** — pulls recent price/volume series for every symbol on the watchlist.
2. **Anomaly Detection** — computes a z-score for each asset's latest return against its own recent distribution, flagging statistically unusual moves (not just "big" moves — moves that are big *for that asset*).
3. **Correlation Analysis** — builds a pairwise correlation matrix across the watchlist and flags pairs whose correlation has notably diverged from what's typical (e.g. two assets that usually move together suddenly decoupling).
4. **Report Generation** — assembles both into a markdown market intelligence report: flagged anomalies, the correlation matrix, and any correlation breaks worth a second look.

## Architecture

```
 ┌────────────────┐     ┌────────────────────┐     ┌──────────────────────┐
 │  Data Ingestion │────▶│  Anomaly + Corr.    │────▶│  Report Generator     │
 │ (price/volume    │     │  Engine (z-scores,  │     │  (market intel        │
 │  series)          │     │  correlation matrix) │     │  summary)              │
 └────────────────┘     └────────────────────┘     └──────────────────────┘
```

## Files

- `pulsescan/data.py` — market data ingestion (Binance public klines)
- `pulsescan/analysis.py` — z-score anomaly detection + pairwise correlation matrix
- `pulsescan/report.py` — assembles findings into a markdown report
- `pulsescan/agent.py` — main loop wiring ingestion → analysis → report
- `config.yaml` — watchlist, z-score threshold, correlation-break threshold

## Running it

```bash
pip install -r requirements.txt
python -m pulsescan.agent --config config.yaml --once
```

## Demo script (for the submission video)

1. Show `config.yaml` — watchlist and the z-score / correlation thresholds.
2. Run the agent, let the report print.
3. Point at a flagged anomaly: "this asset's latest move is 2.5 standard deviations from its own normal — statistically unusual, not just a big number."
4. Point at the correlation matrix, then a flagged correlation break: "these two normally move together, but that relationship just weakened — worth watching."
5. Close on the architecture diagram.

## Why this fits Track A — Data & Analysis

PulseScan does market-wide analysis, not just per-asset stats — cross-referencing every symbol against every other symbol is exactly the kind of computation an AI agent should automate, and the anomaly/correlation framing gives judges a genuinely different Data & Analysis angle than a standard portfolio dashboard.

## Roadmap (post-hackathon)

- Widen the watchlist and run on a rolling schedule instead of a single pass
- Feed flagged anomalies into SignalPilot as a signal source
- Add a rolling correlation chart instead of a single snapshot matrix
