"""Recompute per-origin and valid-coordinate-weighted errors from research archives.
Internal archive directory names are detected by artifact shape, not exposed publicly.
"""
import argparse, pathlib, tarfile, io
import numpy as np
import pandas as pd

EXPERIMENTS = {
 "long-horizon-clipping": "long_horizon_clipping.tar.gz",
 "external-datasets": "external_datasets.tar.gz",
 "validation-locked-selection": "validation_locked_selection.tar.gz",
 "ett-delayed-adaptation": "ett_delayed_adaptation.tar.gz",
}

def load_origins(path):
    tables=[]
    with tarfile.open(path,"r:gz") as tf:
        candidates=[]
        for m in tf:
            if not m.isfile() or not m.name.endswith("/per_origin.csv") or "smoke" in m.name.lower():
                continue
            content=tf.extractfile(m)
            if content is None:continue
            d=pd.read_csv(content)
            required={"method","origin","seed","mechanism","delay","horizon","mse"}
            if not required.issubset(d.columns):continue
            if "dataset" not in d:d["dataset"]=d.get("target","etth2")
            d["record_source"]=m.name
            candidates.append(d)
        if not candidates: raise ValueError("Archive has no applicable per-origin tables; inspect original experiment output")
        # Archive may also include copied runs; prefer its dominant experiment directory.
        counts={}
        for d in candidates:
            prefix=d.record_source.iloc[0].split("/")[0]
            counts[prefix]=counts.get(prefix,0)+1
        chosen=max(counts,key=counts.get)
        tables=[d for d in candidates if d.record_source.iloc[0].split("/")[0]==chosen]
    return pd.concat(tables,ignore_index=True)

def analyze(df,directory):
    # Present model names as they appear in the manuscript, not historical runner labels.
    names={"OMPB+SharedFeat":"SharedFeat", "OMPB+MaskOnlyCtrl":"MaskOnlyCtrl"}
    df=df.copy()
    df["method"]=df["method"].str.replace(r"^[A-Z]\d+[A-Z]?-", "", regex=True).replace(names)
    keys=["dataset","horizon","mechanism","delay","seed","method"]
    if df.duplicated(keys+["origin"]).any():raise ValueError("Duplicated method/forecast-origin keys")
    for col in ["mse","mae"]:
        if col in df and not np.isfinite(df[col]).all(): raise ValueError("Nonfinite "+col)
    if "n_valid" in df:
        if (df.n_valid<=0).any():raise ValueError("Empty scored target origins")
        df["sq_numerator"]=df.mse*df.n_valid
        if "mae" in df:df["abs_numerator"]=df.mae*df.n_valid
    aggregations={"origins":("origin","size"),"mse_origin_mean":("mse","mean")}
    if "mae" in df:aggregations["mae_origin_mean"]=("mae","mean")
    if "n_valid" in df:
        aggregations.update(valid_coordinates=("n_valid","sum"),total_sq=("sq_numerator","sum"))
        if "mae" in df:aggregations["total_abs"]=("abs_numerator","sum")
    by_seed=df.groupby(keys,dropna=False).agg(**aggregations).reset_index()
    if "valid_coordinates" in by_seed:
        by_seed["mse_valid_coordinate"]=by_seed.total_sq/by_seed.valid_coordinates
        if "total_abs" in by_seed:by_seed["mae_valid_coordinate"]=by_seed.total_abs/by_seed.valid_coordinates
    directory.mkdir(parents=True,exist_ok=True)
    by_seed.to_csv(directory/"per_seed.csv",index=False)
    ckeys=["dataset","horizon","mechanism","delay","method"]
    column="mse_valid_coordinate" if "mse_valid_coordinate" in by_seed else "mse_origin_mean"
    condition=by_seed.groupby(ckeys,dropna=False).agg(mean_mse=(column,"mean"),seeds=("seed","nunique")).reset_index()
    condition.to_csv(directory/"condition_means.csv",index=False)
    return by_seed,condition

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--experiment",choices=list(EXPERIMENTS),required=True)
    ap.add_argument("--archive",type=pathlib.Path)
    ap.add_argument("--out",type=pathlib.Path)
    args=ap.parse_args()
    archive=args.archive or pathlib.Path("results/archives")/EXPERIMENTS[args.experiment]
    out=args.out or pathlib.Path("results/derived")/args.experiment
    data=load_origins(archive)
    seed,condition=analyze(data,out)
    print(f"{args.experiment}: {data.record_source.nunique()} run files; {len(seed)} method-seed rows; {len(condition)} conditions")
if __name__=="__main__":main()
