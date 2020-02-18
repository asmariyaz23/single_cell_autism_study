import csv
import sys
import pandas as pd
import os

brain_r=sys.argv[1]


## Intersection region stage wise
if not os.path.exists(os.path.join(brain_r,"region_wise_missense")):
    os.mkdir(os.path.join(brain_r,"region_wise_missense"))

with open("../"+brain_r+"/"+brain_r+"_intersected_tests_cluster_ids.gmt","r") as cf:
    cluster_id={}
    for cluster in cf:
        gene_list=cluster.split("\t")
        cluster_id[gene_list[0]]=gene_list[2:]


region_CE=os.listdir("regions_matrix")
for cem in region_CE:
    region=cem.split("_")[0]
    cepath=os.path.join("regions_matrix",cem)
    with open(cepath,"r") as c:
        pre_df=csv.reader(c,delimiter=',')
        header=pre_df.next()
        exondata_stage=list(pre_df)
        for cluster, de_genes in cluster_id.iteritems():
            l=[]
            if len(l)==0:
                l.append(header)
            for row in exondata_stage:
                if (row[3]).strip('\r\n') in de_genes:
                    l.append(row)
            with open(brain_r+"/region_wise_missense/"+brain_r+"_"+cluster+"_"+cem,"w") as wf:
                writer=csv.writer(wf)
                writer.writerows(l)    


'''
## Intersection region stage wise
with open("../"+brain_r+"/"+brain_r+"_intersected_tests_cluster_ids.gmt","r") as cf:
    cluster_id={}
    for cluster in cf:
        gene_list=cluster.split("\t")
        cluster_id[gene_list[0]]=gene_list[2:]


stage_region_CE=os.listdir("regions_stage_matrix")
for cem in stage_region_CE:
    region=cem.split("_")[0]
    cepath=os.path.join("regions_stage_matrix",cem)
    with open(cepath,"r") as c:
        pre_df=csv.reader(c,delimiter=',')
        header=pre_df.next()
        exondata_stage=list(pre_df)
        for cluster, de_genes in cluster_id.iteritems():
            l=[]
            if len(l)==0:
                l.append(header)
            for row in exondata_stage:
                if (row[4]).strip('\r\n') in de_genes:
                    l.append(row)
            with open(brain_r+"/stage_region_wise/"+brain_r+"_"+cluster+"_"+cem,"w") as wf:
                writer=csv.writer(wf)
                writer.writerows(l)    
'''





'''
## Intersection stage wise
with open("../visp/visp_intersected_tests_cluster_ids.gmt","r") as cf:
    cluster_id={}
    for cluster in cf:
        gene_list=cluster.split("\t")
        cluster_id[gene_list[0]]=gene_list[2:]

with open("adulthood","r") as rf:
    pre_df=csv.reader(rf,delimiter=',')
    header=pre_df.next()
    exondata_stage=list(pre_df)
    for cluster, de_genes in cluster_id.iteritems():
        l=[]
        if len(l)==0:
            l.append(header)
        for row in exondata_stage:
            if (row[3]).strip('\r\n') in de_genes:
                l.append(row)
        with open("visp/visp_"+cluster+"_adulthood.csv","w") as wf:
            writer=csv.writer(wf)
            writer.writerows(l)
'''

