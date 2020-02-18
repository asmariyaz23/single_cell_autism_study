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
    work_dir="/Users/asmaimran/MBRU/AbdulRahman_study/CE_matrix/mtg"
    region="mtg"
    num_clusters=17
    stage1="prenatal"
    stage2="adulthood"

    fd={}
    original_matrix=get_matrix(os.path.join(work,"small"))
    #y=sum_matrix(1,original_matrix)
    #b=sum_matrix(0,original_matrix)
    for cnum in range(0,num_clusters+1):
        cluster_name="Cluster"+str(cnum)
        s1="_".join([region,cluster_name,stage1+".csv"])
        s2="_".join([region,cluster_name,stage2+".csv"])
        s1_matrix=get_matrix(os.path.join(work_dir,s1))
        s2_matrix=get_matrix(os.path.join(work_dir,s2))
        #donor_regions=len(new_matrix.columns)
        x=sum_matrix(1,s1_matrix)
        a=sum_matrix(0,s1_matrix)
        y=sum_matrix(1,s2_matrix)
        b=sum_matrix(0,s2_matrix)
        fd[cluster_name]={"Cluster_name":cluster_name,
                    "x":x,
                    "y":y,
                    "a":a,
                    "b":b}
        #fd[cluster_name]=c_dict
    prop_json=os.path.join(work_dir,"stage_vs_adulthood","proportion_"+stage1+"_"+stage2+".json")
    with open(prop_json,"w") as fj:
        json.dump(fd,fj,indent=4)
