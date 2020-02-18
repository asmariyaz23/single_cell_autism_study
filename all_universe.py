import csv
import json


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

region_map={}
with open("human_ACC_entrezid_genename.csv","r") as map_f:
    region=csv.reader(map_f)
    for gene in region:
        region_map[gene[0]]=(gene[1]).strip()

with open("acc/acc_intersected_tests_cluster.json","r") as cluster_f:
    cluster_genes=json.load(cluster_f)
    cluster_id={}
    for cluster, genes in cluster_genes.items():
        ids=[]
        only_g=genes["genes_with_pli"]
        withpligenes=only_g.keys()
        for g in withpligenes:
            ids.append(region_map[g])
        cluster_id[cluster]=ids

allhighpli=[]
with open("exac_pli_highpli_entrezids.tsv","r") as highpli_f:
     gene=csv.reader(highpli_f)
     allhighpli=[g[0] for g in gene]

T=len(allhighpli)

fisher_dict={}
for cluster in cluster_id:
    m=len(cluster_id[cluster]) 
    x=len(intersection(allhighpli,cluster_id[cluster]))
    n=18225-m-(T-x)
    fisher_dict[cluster]={"Cluster_name":cluster,
                          "m-x":m-x,
                          "T-x":T-x,
                          "n":n,"x":x}

with open("acc/fisher_acc_pligenes_with_allhighpli.json","w") as fw:
    json.dump(fisher_dict,fw,indent=4)
