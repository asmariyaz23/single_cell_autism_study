from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt

Astrocytes=["11","9","11"]
Microglia=["17","13","16"]
Oligo=["10","10","8"]
OPC=["16","12","15"]

region_order=["mtg","acc","visp"]
gmt_files=["mtg/mtg_intersected_tests_cluster.gmt",
           "acc/acc_intersected_tests_cluster.gmt",
           "visp/visp_intersected_tests_cluster.gmt"]
clusters_of_interest=OPC

region_map={}
for gmt in gmt_files:
    region=gmt.split("/")[0]
    with open(gmt,"r") as pli:
        cluster_id={}
        for cluster in pli:
            gene_list=cluster.split("\t")
            cluster_id[gene_list[0]]=[gene.strip() for gene in gene_list[2:]]
        region_map[region]=cluster_id    

genes_interest={}
for i,r in enumerate(region_order):
    gmt_dict=region_map[r]
    clus_num="Cluster"+clusters_of_interest[i]
    genes=gmt_dict[clus_num]
    genes_interest[r]=genes

plt.figure(figsize=(15,15)) 

out=venn3([set(genes_interest[region_order[0]]), set(genes_interest[region_order[1]]), set(genes_interest[region_order[2]])], set_labels = (region_order[0].upper()+" Cluster "+clusters_of_interest[0], 
                                                                                                                                        region_order[1].upper()+" Cluster "+clusters_of_interest[1], 
                                                                                                                                        "VISp Cluster "+clusters_of_interest[2]))
for text in out.set_labels:
    text.set_fontsize(25)
    text.set_fontweight("bold")
    
for text in out.subset_labels:
    text.set_fontsize(20)

plt.title('Overlap of DE genes - OPC',fontsize=30,fontweight="bold",pad=30)
plt.savefig("OPC_venn.svg",dpi=600) 
