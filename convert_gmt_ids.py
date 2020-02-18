import csv

region_map={}
with open("human_MTG_2018-06-14_entrezid_gene.csv","r") as region_f:
    region=csv.reader(region_f)
    for gene in region:
        region_map[gene[1]]=(gene[0]).strip()


with open("mtg/mtg_intersected_tests_cluster.gmt","r") as pli:
    cluster_id={}
    for cluster in pli:
        gene_list=cluster.split("\t")
        cluster_id[gene_list[0]]=[region_map[gene.strip()] for gene in gene_list[2:]]
        
with open("mtg/mtg_intersected_tests_cluster_ids.gmt","w") as wpli:
    writer=csv.writer(wpli,delimiter="\t")
    all=[]
    for c,v in cluster_id.items():
        all.append([c,c.lower()]+v)
    writer.writerows(all)              
