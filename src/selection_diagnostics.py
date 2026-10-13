"""Reconstruct whole-arm Validation-Locked origin differences from original records."""
import argparse, pathlib,tarfile,pandas as pd
from src.reanalyze import load_origins

def main():
    p=argparse.ArgumentParser();p.add_argument("--archive",type=pathlib.Path,default=pathlib.Path("results/archives/validation_locked_selection.tar.gz"));args=p.parse_args()
    with tarfile.open(args.archive,"r:gz") as t:
        eligible=[m for m in t if m.isfile() and m.name.endswith("/validation_selections.csv")]
        if len(eligible)!=1:raise ValueError("Expected exactly one validation selection file")
        sel=pd.read_csv(t.extractfile(eligible[0]))
    choices=dict(zip(sel.group,sel.selected))
    d=load_origins(args.archive)
    keys=["dataset","horizon","mechanism","delay","seed","origin"]
    pivot=d.pivot_table(index=keys,columns="method",values="mse",aggfunc="first")
    differences=[]
    for key,row in pivot.iterrows():
        dataset,h,mask,delay,seed,origin=key
        name=choices.get(f"{dataset}_H{h}_s{seed}")
        if name is None or name not in row.index:raise ValueError(f"Missing selection for {key}")
        differences.append((dataset, float(row[name]-row["OMPB-Delayed"])))
    pairs=pd.DataFrame(differences,columns=["dataset","difference"])
    print(pairs.groupby("dataset").difference.agg(origins="size",harm=lambda x:(x>1e-12).mean(),tie=lambda x:(abs(x)<=1e-12).mean(),benefit=lambda x:(x<-1e-12).mean()).to_string())
if __name__=="__main__":main()
