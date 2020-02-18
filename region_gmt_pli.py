import sys
import csv
import json

region_json=sys.argv[1]
region=sys.argv[2]

with open(region_json,"r") as rj:
    data=json.load(rj)
    clusters={}
    for cluster in data:
        cluster_pli=[]
        cluster_genes=data[cluster]["genes_with_pli"]
        for gene in cluster_genes:
            if float(cluster_genes[gene]) > 0.9:
                cluster_pli.append(gene)
        clusters[cluster]=[cluster.upper(),cluster.lower()]+cluster_pli

with open(region+"_plihighgenes.gmt","w") as plh:
    for cluster in clusters:
        plh.write("\t".join(clusters[cluster])+"\n")         

