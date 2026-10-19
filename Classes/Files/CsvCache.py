"""Immutable CSV tables shared by packet handlers; restart after asset updates."""
import csv
from functools import lru_cache
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=32)
def read_csv(path):
    with (_ROOT / path).open(encoding="utf-8", newline="") as source:
        return tuple(tuple(row) for row in csv.reader(source))

