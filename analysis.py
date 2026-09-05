"""
analysis.py — anomaly detection and correlation analysis for PulseScan.

No external stats library required — everything here is plain
Python so the project has minimal dependencies and is easy to read
line-by-line in a demo.
"""
from dataclasses import dataclass
from typing import List, Dict, Tuple
from .data import SeriesData


def returns(closes: List[float]) -> List[float]:
    return [(closes[i] - closes[i - 1]) / closes[i - 1] for i in range(1, len(closes))]


def mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stdev(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return variance ** 0.5


def pearson_correlation(a: List[float], b: List[float]) -> float:
    n = min(len(a), len(b))
    a, b = a[-n:], b[-n:]
    ma, mb = mean(a), mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    den_a = sum((x - ma) ** 2 for x in a) ** 0.5
    den_b = sum((x - mb) ** 2 for x in b) ** 0.5
    if den_a == 0 or den_b == 0:
        return 0.0
    return num / (den_a * den_b)


@dataclass
class AnomalyResult:
    symbol: str
    latest_return_pct: float
    zscore: float
    flagged: bool


def detect_anomalies(series_list: List[SeriesData], zscore_threshold: float) -> List[AnomalyResult]:
    results = []
    for s in series_list:
        rets = returns(s.closes)
        if len(rets) < 5:
            results.append(AnomalyResult(s.symbol, 0.0, 0.0, False))
            continue
        history, latest = rets[:-1], rets[-1]
        m, sd = mean(history), stdev(history)
        if sd == 0:
            # Zero historical variance (e.g. a flat price) means ANY
            # nonzero move is maximally anomalous, not a zero z-score.
            flagged = latest != m
            z = float("inf") if flagged and latest > m else (float("-inf") if flagged else 0.0)
        else:
            z = (latest - m) / sd
            flagged = abs(z) >= zscore_threshold
        results.append(AnomalyResult(s.symbol, latest * 100, z, flagged))
    return results


def correlation_matrix(series_list: List[SeriesData]) -> Dict[Tuple[str, str], float]:
    matrix = {}
    for i, a in enumerate(series_list):
        for b in series_list[i + 1:]:
            corr = pearson_correlation(returns(a.closes), returns(b.closes))
            matrix[(a.symbol, b.symbol)] = corr
    return matrix


def detect_correlation_breaks(series_list: List[SeriesData], break_threshold: float) -> List[str]:
    """
    Compares correlation over the first half of the window vs. the
    second half — a simple way to flag pairs whose relationship has
    shifted recently without needing a full rolling-window model.
    """
    breaks = []
    for i, a in enumerate(series_list):
        for b in series_list[i + 1:]:
            ra, rb = returns(a.closes), returns(b.closes)
            n = min(len(ra), len(rb))
            if n < 10:
                continue
            half = n // 2
            early_corr = pearson_correlation(ra[:half], rb[:half])
            recent_corr = pearson_correlation(ra[half:], rb[half:])
            if abs(recent_corr - early_corr) >= break_threshold:
                breaks.append(
                    f"{a.symbol}/{b.symbol}: correlation shifted from {early_corr:.2f} to {recent_corr:.2f}"
                )
    return breaks
