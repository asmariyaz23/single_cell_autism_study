import csv
import sys
import os
import pandas as pd
import json

def get_matrix(path):
    skipcols=["row_num","gene_id","ensembl_gene_id",
              "gene_symbol","entrez_id","start",
              "end","chromosome","length",
              "count","FM_burden"]
    return(pd.read_csv(path,usecols=lambda x: x not in skipcols))

def sum_matrix(num_to_count,matrix):
    return((pd.value_counts(matrix.values.flatten())[num_to_count]))

if __name__ == "__main__":
    work="/Users/asmaimran/MBRU/AbdulRahman_study/CE_matrix/"
    work_dir="/Users/asmaimran/MBRU/AbdulRahman_study/CE_matrix/visp"
    region="visp"
    num_clusters=16
    stage1="early_childhood"
    stage2="adulthood"

    regions=["A1C","AMY","CBC","DFC","HIP",
             "IPC","ITC","M1C","MD","MFC",
             "OFC","S1C","STC","STR","V1C",
             "VFC"]
    
    prop_d={}
    for r in regions:
        region_df=get_matrix(os.path.join("regions_matrix",r+".csv"))
        region_df_num_col=region_df.shape[1]
        U=float(sum_matrix(1,region_df))
        for cnum in range(0,num_clusters+1):
            cluster_name="Cluster"+str(cnum) 
            s1="_".join([region,cluster_name,r,stage1+".csv"])
            s2="_".join([region,cluster_name,r,stage2+".csv"])
            s1_matrix=get_matrix(os.path.join(work_dir,"stage_region_wise",s1))
            s2_matrix=get_matrix(os.path.join(work_dir,"stage_region_wise",s2))
            a=float(sum_matrix(1,s1_matrix))
            b=float(sum_matrix(1,s2_matrix))
            prop_d[cluster_name]={"cluster_name":cluster_name,
                                  "a":a/region_df_num_col,
                                  "b":b/region_df_num_col,
                                  "U":U/region_df_num_col}

        if not os.path.exists(os.path.join(work_dir,"stage_region_wise","stage_vs_adulthood")):
            os.mkdir(os.path.join(work_dir,"stage_region_wise","stage_vs_adulthood"))
        prop_json=os.path.join(work_dir,"stage_region_wise",
                               "stage_vs_adulthood","proportion_"+ r +"_"+stage1+"_"+stage2+".json")
        
        with open(prop_json,"w") as fj:
                  json.dump(prop_d,fj,indent=4)
