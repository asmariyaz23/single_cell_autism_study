import csv
import sys
import json 
import pyreadr
import pandas
import os
import json

def read_file(region_cluster_num,tests,main_dir,region):
    cd={}
    for cluster in range(0,region_cluster_num):
        cd_testwise=[]
        cnum=cluster
        for test in tests:
            filename=region+"_m"+str(cnum)+"_filter_"+test+".rds"
            pyr=pyreadr.read_r(os.path.join(main_dir,region,"DE",test,"pval_adj_strin_filter",filename))
            df1=pyr[None]
            cd_testwise.append(list(df1['gene']))
        cd[str(cnum)]=tuple(set(cd_testwise[0]).intersection(*cd_testwise[1:]))
    return(cd)

def gene_pli_score(entire_file):
    d={}
    with open(entire_file, "r") as ef:
        reader=csv.reader(ef,delimiter='\t')
        next(reader)
        ##row[0] is gene_symbol
        d={rows[0]:rows[1] for rows in reader}
    return(d)

def write_intersection_per_cluster(main_dir,region,cd,map):
    with open(os.path.join(main_dir,region,region+"_intersected_tests_cluster.json"),"w") as cw:
        cluster_dict={}
        for k,v in cd.items():
            num_de_genes_cluster=len(v)
            pli_dict={}
            for gene in v:
                if gene in map:
                    pli_dict[gene]=map[gene.strip()]
                else:
                    print("Not found in Exac database:"+gene)
            cluster_dict["Cluster"+"_"+k]={"genes_with_pli":pli_dict,
                                           "Total_num_genes":num_de_genes_cluster} 
        json.dump(cluster_dict,cw)
        

main_dir=sys.argv[1]
region=sys.argv[2]
region_cluster_num=int(sys.argv[3])
gene_pli=sys.argv[4]
tests=['wilcox','t-test','bimod','MAST']
cd=read_file(region_cluster_num,tests,main_dir,region)
map=gene_pli_score(gene_pli)
write_intersection_per_cluster(main_dir,region,cd,map)
