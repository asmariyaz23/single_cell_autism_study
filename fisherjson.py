from scipy.stats import fisher_exact
import sys
import json
import pandas as pd
import os
import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects.numpy2ri import numpy2rpy
from rpy2.robjects.packages import importr
import numpy as np


json_f=sys.argv[1]
brain_part=sys.argv[2]

with open(json_f,"r") as jf:
    ce_dict=json.load(jf)
    for region in ce_dict:
        for stage in ce_dict[region]:
            ce_wdict=[]
            for c in ce_dict[region][stage]:
                cluster=ce_dict[region][stage][c]
                mat=np.array([[cluster["x"],cluster["m_x"]],
                             [cluster["T_x"], cluster["n"]]])
                r_cont = numpy2rpy(mat)
                r.assign("cont", r_cont)
                r('fmat_pval <- fisher.test(cont, alternative="greater",conf.int=TRUE)$p.value')
                r('fmat_estimate <- fisher.test(cont, alternative="greater",conf.int=TRUE)$estimate')
                r('fmat_conf <- fisher.test(cont, alternative="greater",conf.int=TRUE)$conf.int')
                pval=r("fmat_pval")
                odds=r("fmat_estimate")
                conf_int=r("fmat_conf")
                ce_wdict.append({"Cluster_name":cluster["Cluster_num"],
                                 "CE_Stage_region":cluster["x"],
                                 "Pvalue":float((str(pval).split(" ")[1]).strip("\n")),
                                 "Odds_ratio":float((str(odds).split("\n")[1]).strip('"')),
                                 "Lower_CI":conf_int[0],
                                 "Upper_CI":conf_int[1]})
            df=pd.DataFrame(ce_wdict)
            df.to_csv(os.path.join(brain_part,"stage_region_wise",
                                   "fisher",region+"_"+stage+".csv"))
