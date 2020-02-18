import csv
import sys
import json 
import pyreadr
import pandas
import os

def read_file(cluster_dir,test):
    cd=os.listdir(cluster_dir)
    clusters=[]
    for cluster in cd:
        if cluster.endswith("_filter_"+test+".rds"):
            pyr=pyreadr.read_r(os.path.join(cluster_dir,cluster))
            df1=pyr[None]
            cluster_list=list(df1['gene'])
            cnum=str(''.join(filter(str.isdigit, cluster)))
            f=["Cluster"+cnum,"CLUSTER"+cnum]+cluster_list
            clusters.append(f)
    return(clusters)

def gene_entrez_id(entire_file):
    d={}
    with open(entire_file, "r") as ef:
        reader=csv.reader(ef,delimiter=',')
        next(reader)
        d={rows[0]:rows[1] for rows in reader}
    return(d)

def combine(cluster_list,entire_list):
    ids=[entire_list[gene] for gene in cluster_list]
    return(ids)     


cluster_dir=sys.argv[1]
entire_file2=sys.argv[2]
output=sys.argv[3]
test=sys.argv[4]
cluster_lists=read_file(cluster_dir,test)
entire_list2=gene_entrez_id(entire_file2)
with open(output, "w") as gd:
     writer=csv.writer(gd, delimiter="\t")
     for cluster in cluster_lists:
         cluster_ids=combine(cluster[2:],entire_list2)
         crow=[cluster[0],cluster[1]]+cluster_ids
         writer.writerow(crow)    
