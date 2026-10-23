#!/usr/bin/env python3
"""Analyze genuinely independent, frozen, pre-adjudication A/B DCTR ratings.

No ratings are generated, imputed or taken from author-coded reference labels.
Agreement is NOT security-outcome accuracy.
"""
import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

LEVELS = tuple("L" + str(i) for i in range(5))
REQUIRED = {"unit_id", "cluster_id", "repository", "rater_a_level", "rater_b_level"}

def read_frozen_ratings(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError("missing required columns: " + str(sorted(REQUIRED-set(reader.fieldnames or []))))
        rows, seen = [], set()
        for i, raw in enumerate(reader, 2):
            r = {k: (raw.get(k) or "").strip() for k in REQUIRED}
            if any(not r[k] for k in ("unit_id","cluster_id","repository")):
                raise ValueError("line %d: empty evidence identifier" % i)
            if r["unit_id"] in seen:
                raise ValueError("line %d: duplicate unit" % i)
            if r["rater_a_level"] not in LEVELS or r["rater_b_level"] not in LEVELS:
                raise ValueError("line %d: both frozen, independent L0-L4 ratings required" % i)
            seen.add(r["unit_id"])
            rows.append(r)
    if not rows:
        raise ValueError("no independently double-coded rows")
    return rows

def kappa(pairs):
    if not pairs:
        return None
    n=len(pairs)
    a=[0]*5
    b=[0]*5
    observed=0.0
    for x,y in pairs:
        i,j=int(x[1]),int(y[1])
        a[i]+=1
        b[j]+=1
        observed += abs(i-j)/4
    observed /= n
    expected=sum(a[i]*b[j]*abs(i-j)/4 for i in range(5) for j in range(5))/(n*n)
    return None if expected==0 else 1-observed/expected

def boot(rows, reps=5000, seed=20261023):
    if reps < 1:
        raise ValueError("bootstrap repetitions must be positive")
    groups=defaultdict(list)
    for r in rows:
        groups[(r["repository"],r["cluster_id"])].append(r)
    keys=sorted(groups)
    if len(keys)<2:
        return {"interval_95":None,"defined_replicates":0,"requested_replicates":reps,
                "reason":"fewer than 2 repository-qualified clusters"}
    rng=random.Random(seed)
    values=[]
    for _ in range(reps):
        pairs=[(r["rater_a_level"],r["rater_b_level"])
               for key in (rng.choice(keys) for _ in keys) for r in groups[key]]
        value=kappa(pairs)
        if value is not None and math.isfinite(value):
            values.append(value)
    if not values:
        return {"interval_95":None,"defined_replicates":0,"requested_replicates":reps,
                "reason":"all resampled kappa values undefined"}
    values.sort()
    def pct(q):
        p=(len(values)-1)*q
        lo,hi=math.floor(p),math.ceil(p)
        return values[lo]+(p-lo)*(values[hi]-values[lo])
    return {"interval_95":[round(pct(.025),6),round(pct(.975),6)],
            "defined_replicates":len(values),"requested_replicates":reps,"seed":seed,
            "method":"exploratory repository-cluster percentile bootstrap"}

def analyze(rows, reps=5000, seed=20261023):
    if not rows:
        raise ValueError("no rows")
    pairs=[(r["rater_a_level"],r["rater_b_level"]) for r in rows]
    groups=defaultdict(list)
    for r in rows:
        groups[(r["repository"],r["cluster_id"])].append(r)
    counts_a=Counter(a for a,b in pairs)
    counts_b=Counter(b for a,b in pairs)
    cross={f"{a}/{b}":sum((x,y)==(a,b) for x,y in pairs) for a in LEVELS for b in LEVELS}
    agreement=sum(a==b for a,b in pairs)
    score=kappa(pairs)
    return {
      "status":"PRE_ADJUDICATION_RELIABILITY_NOT_SECURITY_ACCURACY",
      "units":len(rows),"repository_count":len({r["repository"] for r in rows}),
      "repository_cluster_count":len(groups),
      "exact_agreement":{"agreed":agreement,"total":len(rows),"rate":round(agreement/len(rows),6)},
      "cluster_macro_exact_agreement":round(sum(
          sum(r["rater_a_level"]==r["rater_b_level"] for r in group)/len(group)
          for group in groups.values())/len(groups),6),
      "linear_weighted_cohen_kappa":None if score is None else round(score,6),
      "cluster_bootstrap_kappa":boot(rows,reps,seed),
      "independent_a_level_counts":{i:counts_a[i] for i in LEVELS},
      "independent_b_level_counts":{i:counts_b[i] for i in LEVELS},
      "cross_tab":cross,
      "critical_boundary_disagreements":{
        "L2/L3":cross["L2/L3"]+cross["L3/L2"],
        "L3/L4":cross["L3/L4"]+cross["L4/L3"],
        "L4/L4":cross["L4/L4"]},
      "l3_jointly_labeled_clusters":len({(r["repository"],r["cluster_id"]) for r in rows if r["rater_a_level"]==r["rater_b_level"]=="L3"}),
      "l4_jointly_labeled_clusters":len({(r["repository"],r["cluster_id"]) for r in rows if r["rater_a_level"]==r["rater_b_level"]=="L4"}),
      "limitation":"Agreement cannot establish security correctness, calibrated risk or natural L4 prevalence."
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--bootstrap",type=int,default=5000)
    parser.add_argument("--seed",type=int,default=20261023)
    args=parser.parse_args()
    report=analyze(read_frozen_ratings(args.input),args.bootstrap,args.seed)
    Path(args.output).write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("Computed pre-adjudication agreement for %d real double-coded units" % report["units"])

if __name__=="__main__":
    main()
