"""
report.py — assembles anomaly results + correlation matrix into a
markdown report for PulseScan.
"""
from typing import List, Dict, Tuple
from .analysis import AnomalyResult


def build_report(
    title: str,
    anomalies: List[AnomalyResult],
    matrix: Dict[Tuple[str, str], float],
    correlation_breaks: List[str],
) -> str:
    lines = [f"# {title}", ""]

    flagged = [a for a in anomalies if a.flagged]
    lines.append("## Executive Summary")
    lines.append(
        f"{len(flagged)} anomaly(ies) flagged out of {len(anomalies)} tracked assets. "
        f"{len(correlation_breaks)} correlation break(s) detected."
    )
    lines.append("")

    lines.append("## Anomaly Scan")
    lines.append("| Symbol | Latest Return | Z-Score | Flagged |")
    lines.append("|---|---|---|---|")
    for a in anomalies:
        mark = "⚠️ Yes" if a.flagged else "No"
        lines.append(f"| {a.symbol} | {a.latest_return_pct:+.2f}% | {a.zscore:+.2f} | {mark} |")
    lines.append("")

    lines.append("## Correlation Matrix")
    lines.append("| Pair | Correlation |")
    lines.append("|---|---|")
    for (sym_a, sym_b), corr in matrix.items():
        lines.append(f"| {sym_a} / {sym_b} | {corr:.2f} |")
    lines.append("")

    lines.append("## Correlation Breaks")
    if correlation_breaks:
        for b in correlation_breaks:
            lines.append(f"- ⚠️ {b}")
    else:
        lines.append("- None detected this pass.")

    return "\n".join(lines)
