from pathlib import Path
from typing import cast

import pandas as pd

cwd: Path = Path.cwd().resolve() / "input"
files = Path(cwd).glob("*.csv")
dfs = (cast(pd.DataFrame, pd.read_csv(f)) for f in files)
df: pd.DataFrame = pd.concat(dfs, ignore_index=True)

df["date"] = pd.to_datetime(df["date"])
df["score"] = pd.to_numeric(df["score"], errors="raise")

df = df.sort_values(["category", "date"])

df["cumulative_score"] = df.groupby("category")["score"].cumsum().round(1)

# print(df[["date", "category", "score", "cumulative_score"]])

output_dir = Path("dist")
output_dir.mkdir(exist_ok=True)

for date, group in df.groupby("date"):
    snapshot = (
        df[df["date"] <= date]
        .sort_values("date")
        .groupby("category", as_index=False)
        .last()[["category", "cumulative_score"]]
    )

    out_path = output_dir / f"leetcode_totals_{date.date()}.csv"
    snapshot.to_csv(out_path, index=False)
