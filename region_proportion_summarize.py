from scipy.stats import fisher_exact
import sys
import json
import pandas as pd
import os
import rpy2.robjects as robjects
from rpy2.robjects import r as R
from rpy2.robjects.numpy2ri import numpy2rpy
from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector
import numpy as np
import csv

base = importr('base')
epitools=importr('epitools')

brain_part="visp"
cluster_num=16

regions=["A1C","AMY","CBC","DFC",
         "HIP","IPC","ITC","M1C",
         "MD","MFC","OFC","S1C",
         "STC","STR","V1C","VFC"]

work_dir=os.path.join(brain_part,"stage_region_wise","stage_vs_adulthood")
all_jsons=os.listdir(work_dir)

jdict={}
for f in all_jsons:
    if f.endswith(".json"):
        fstr=f.split(".")[0]
        with open(os.path.join(work_dir,f),"r") as wr:
            jdict[fstr]=json.load(wr)

comparisons=["prenatal_adulthood",
             "early_childhood_adulthood"]

i=1
for cnum in range(0,cluster_num+1):
    region_d={}
    for r in regions:
        comp_d={}
        for comparison in comparisons:
            jd="proportion"+"_"+r+"_"+comparison
            clus_details=jdict[jd]["Cluster"+str(cnum)]
            ce=np.array([clus_details["a"],clus_details["b"]])
            univ=np.array([clus_details["U"],clus_details["U"]])
            r_ce=numpy2rpy(ce)
            r_univ=numpy2rpy(univ)
            R.assign("ce", r_ce)
            R.assign("univ", r_univ)
            omat=FloatVector([clus_details["a"],clus_details["b"],clus_details["U"],clus_details["U"]])
            R('pmat <- prop.test(x=ce,n=univ,alternative="greater",conf.level=0.95)$p.value')
            pval=float((str(R("pmat")).split(" ")[1]).strip("\n"))
            epiod=epitools.oddsratio(omat)
            odds=epiod[1][1]
            comp_d[comparison+"_pval"]=pval
            comp_d[comparison+"_pval_adj"]=float(pval)*float(2)*(float(cluster_num+1))
            comp_d[comparison+"_odds_ratio"]=odds
        region_d[r]=comp_d
         
    with open(os.path.join(work_dir,brain_part+"_prop_summary",brain_part+"_proportion_cluster"+str(cnum)+".csv"),"w") as wh:
        writer=csv.writer(wh)
        writer.writerow(["Region",comparisons[0]+"_pval",comparisons[0]+"_pval_adj",
                         comparisons[0]+"_odds_ratio",
                         comparisons[1]+"_pval",comparisons[1]+"_pval_adj",
                         comparisons[1]+"_odds_ratio"])
        rl=[]
        for r in region_d:
            rl.append([r,region_d[r][comparisons[0]+"_pval"],
                        region_d[r][comparisons[0]+"_pval_adj"],
                        region_d[r][comparisons[0]+"_odds_ratio"],
                        region_d[r][comparisons[1]+"_pval"],
                        region_d[r][comparisons[1]+"_pval_adj"],
                        region_d[r][comparisons[1]+"_odds_ratio"]])
        writer.writerows(rl)
