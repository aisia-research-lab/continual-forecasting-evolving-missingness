"""Produce descriptive tables for the experiments retained in the manuscript."""
from pathlib import Path
import pandas as pd
for folder in sorted(Path("results/derived").iterdir()):
    if not folder.is_dir() or not (folder/"condition_means.csv").exists():continue
    df=pd.read_csv(folder/"condition_means.csv")
    print("\n"+folder.name)
    print(df.groupby(["dataset","method"],as_index=False).mean_mse.mean().to_string(index=False))
