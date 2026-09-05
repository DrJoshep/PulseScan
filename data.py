"""
data.py — market data ingestion for PulseScan.

Pulls recent candles per symbol from Binance's public REST API
(no API key needed). Returns closing prices, which is all the
anomaly and correlation engine needs.
"""
import json
import urllib.request
from dataclasses import dataclass
from typing import List

BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"


@dataclass
class SeriesData:
    symbol: str
    closes: List[float]


def fetch_series(symbol: str, limit: int, interval: str) -> SeriesData:
    url = f"{BINANCE_KLINES_URL}?symbol={symbol}&interval={interval}&limit={limit}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        raw = json.loads(resp.read())
    closes = [float(c[4]) for c in raw]
    return SeriesData(symbol, closes)


def fetch_watchlist_series(watchlist: List[str], limit: int, interval: str) -> List[SeriesData]:
    results = []
    for symbol in watchlist:
        try:
            results.append(fetch_series(symbol, limit, interval))
        except Exception as exc:
            print(f"[warn] could not fetch data for {symbol}: {exc}")
    return results
