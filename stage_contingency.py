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
    return(pd.read_csv(path,usecols=lambda x: x not in skipcols, index_col=0))

def sum_matrix(num_to_count,matrix):
    return((pd.value_counts(matrix.values.flatten())[num_to_count]))

if __name__ == "__main__":
    work="/Users/asmaimran/MBRU/AbdulRahman_study/CE_matrix/"
    work_dir="/Users/asmaimran/MBRU/AbdulRahman_study/CE_matrix/mtg"
    region="mtg"
    num_clusters=17
    stage="adulthood"

    fd={}
    original_matrix=get_matrix(os.path.join(work,"abi.developmental_matrix.CE_modified.csv"))
    old_matrix=get_matrix(os.path.join(work,stage))
    for cnum in range(0,num_clusters+1):
        cluster_name="Cluster"+str(cnum)
        cf="_".join([region,cluster_name,stage+".csv"])
        new_matrix=get_matrix(os.path.join(work_dir,cf))
        donor_regions=len(new_matrix.columns)
        x=sum_matrix(1,new_matrix)
        m_x=sum_matrix(0,new_matrix)
        old_ones=sum_matrix(1,old_matrix)
        T_x=old_ones-x
        a=(donor_regions*309224)-(m_x)
        b=a-(x)
        c=b-T_x
        num_cells=original_matrix.shape[0]*original_matrix.shape[1]
        fd[cluster_name]={"Cluster_name":cluster_name,
                    "T-x":T_x,
                    "x":x,
                    "m-x":m_x,
                    "n":c,
                    "new_matrix_num_cells":num_cells}
        #fd[cluster_name]=c_dict
    fisher_json=os.path.join(work_dir,"fisher_"+stage+".json")
    with open(fisher_json,"w") as fj:
        json.dump(fd,fj,indent=4)
