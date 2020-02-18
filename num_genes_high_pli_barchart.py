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
        count=0
        count_filter=0
        cluster_pli=[]
        cluster_genes=data[cluster]["genes_with_pli"]
        num_gene_cluster_no_filter=data[cluster]["Total_num_genes"]
        print(cluster)
        print(len(cluster_genes))
        print(num_gene_cluster_no_filter)
        for gene in cluster_genes:
            if float(cluster_genes[gene]) > 0.9:
                count_filter=count_filter+1
        cluster_count[cluster]={"genes_with_pli_filter_applied":count_filter,
                                "Total_num_genes":num_gene_cluster_no_filter,
                                "genes_with_pli":len(cluster_genes)
                               }


plt.rcdefaults()
fig, ax = plt.subplots()


convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

clus_nums=sorted(cluster_count.keys(),key = alphanum_key)
pli=[]
nonpli=[]
for i in clus_nums:
    pli.append(cluster_count[i]["genes_with_pli_filter_applied"])
    nonpli.append(cluster_count[i]["genes_with_pli"])
width = 0.35
x = np.arange(len(clus_nums)) 
rects1 = ax.bar(x - width/2, pli, width, label='DE genes>0.9')
rects2 = ax.bar(x + width/2, nonpli, width, label='Total DE Genes')
ax.set_ylabel('Number of DE genes',fontsize=6)
ax.set_title(region+' pli genes',fontsize=6)
ax.set_xticks(x)
ax.set_xticklabels(clus_nums, rotation=90,fontsize=6)
ax.legend(fontsize=6)


fig.tight_layout()

plt.savefig(region+".png",dpi=300, bbox_inches='tight')                
