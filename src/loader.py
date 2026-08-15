from __future__ import annotations

from pathlib import Path
import pandas as pd
from .normalizer import normalize_name


def load_official(filename: str | Path) -> pd.DataFrame:
    df = pd.read_csv(filename)
    required = {"date", "name"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            "Missing required CSV columns: " + ", ".join(sorted(missing))
        )

    df["date"] = pd.to_datetime(df["date"], errors="raise").dt.date
    df["name"] = df["name"].astype(str).str.strip()

    if "type" not in df.columns:
        df["type"] = "unknown"

    df["normalized_name"] = df["name"].apply(normalize_name)
    return df
