import sys
import json
import matplotlib.pyplot as plt
import re
import numpy as np
import matplotlib


region=sys.argv[1]
json_dict=sys.argv[2]

with open(json_dict) as json_file:
    data=json.load(json_file)
    cluster_count={}
    for cluster in data:
        cluster_pli=[]
        cluster_genes=data[cluster]["genes_with_pli"]
        num_gene_cluster_no_filter=data[cluster]["Total_num_genes"]
        for gene in cluster_genes:
            if float(cluster_genes[gene]) > 0.9:
                cluster_pli.append(float(cluster_genes[gene]))
        cluster_count[cluster]=cluster_pli


plt.rcdefaults()
fig, ax = plt.subplots()

convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

clus_nums=sorted(cluster_count.keys(),key = alphanum_key)
data_plot=[]
for i in clus_nums:
    data_plot.append(cluster_count[i])
ax.set_xticklabels(clus_nums, rotation=90) ;
ax.boxplot(data_plot,labels=clus_nums,showfliers=False)
fig.tight_layout()

plt.savefig(region+".png",dpi=300, bbox_inches='tight')                
