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
    brain_part=sys.argv[1]
    num_clusters=sys.argv[2]
    stages=["prenatal","early_childhood","adulthood"]
    regions=["A1C","AMY","CBC","DFC","HIP",
             "IPC","ITC","M1C","MD","MFC",
             "OFC","S1C","STC","STR","V1C",
             "VFC"]
    stage_region_CE_cm={}
    for region in regions:
        stage_df=get_matrix(os.path.join("regions_matrix",region+".csv"))
        U=sum_matrix(1,stage_df)
        stage_df_cells=stage_df.shape[0]*stage_df.shape[1]
        for stage in stages:
            stage_region_df=get_matrix(os.path.join("regions_stage_matrix",region+"_"+stage+".csv"))
            allcells_stage_region=stage_region_df.shape[0]*stage_region_df.shape[1]
            contingency_mat={}
            for num_clus in range(0,int(num_clusters)+1):
                clus_name="Cluster"+str(num_clus)
                part_region_clus_df=get_matrix(os.path.join(brain_part,"region_wise",
                                                            brain_part+"_"+clus_name+"_"+region+".csv"))
                part_stage_region_df=get_matrix(os.path.join(brain_part,"stage_region_wise",
                                                             brain_part+"_"+clus_name+"_"+region+"_"+stage+".csv"))
                x=sum_matrix(1,part_stage_region_df)
                m_x=(sum_matrix(1,part_region_clus_df))-x
                T=sum_matrix(1,stage_region_df)
                T_x=(T-x)
                a=U-x
                b=a-(m_x)
                n=b-(T_x)
                if clus_name not in contingency_mat:
                    contingency_mat[clus_name]={"x":x,
                                                "T_x":T_x,
                                                "m_x":m_x,
                                                "n":n,
                                                "Cluster_num":clus_name}                                        

            if region not in stage_region_CE_cm:
                stage_region_CE_cm[region]={stage:contingency_mat} 
            if stage not in stage_region_CE_cm[region]:
                already=stage_region_CE_cm[region]
                already[stage]=contingency_mat
                stage_region_CE_cm[region]=already
    fisher_json=os.path.join(os.path.join(brain_part,"stage_region_wise","fisher",
                                          brain_part+".json"))
    with open(fisher_json,"w") as fj:
        json.dump(stage_region_CE_cm,fj,indent=4)


























