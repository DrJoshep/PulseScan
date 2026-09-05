"""
agent.py — PulseScan main loop.

Usage:
    python -m pulsescan.agent --config config.yaml --once [--out report.md]
"""
import argparse
import yaml

from .data import fetch_watchlist_series
from .analysis import detect_anomalies, correlation_matrix, detect_correlation_breaks
from .report import build_report


def run_once(config: dict) -> str:
    series_list = fetch_watchlist_series(
        config["watchlist"], config["lookback_periods"], config["interval"]
    )
    anomalies = detect_anomalies(series_list, config["thresholds"]["anomaly_zscore"])
    matrix = correlation_matrix(series_list)
    breaks = detect_correlation_breaks(series_list, config["thresholds"]["correlation_break"])
    return build_report(config["report"]["title"], anomalies, matrix, breaks)


def main():
    parser = argparse.ArgumentParser(description="PulseScan market anomaly & correlation agent")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--once", action="store_true", help="run a single scan and exit")
    parser.add_argument("--out", default=None, help="optional file path to write the report to")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    report = run_once(config)
    print(report)

    if args.out:
        with open(args.out, "w") as f:
            f.write(report)


if __name__ == "__main__":
    main()
