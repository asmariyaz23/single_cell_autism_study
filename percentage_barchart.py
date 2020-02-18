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
        for gene in cluster_genes:
            if float(cluster_genes[gene]) > 0.9:
                count_filter=count_filter+1
        cluster_count[cluster]={"genes_with_pli_filter_applied":count_filter,
                                "Total_num_genes":num_gene_cluster_no_filter,
                                "genes_with_pli":len(cluster_genes)
                               }
        #print(count_filter)


plt.rcdefaults()
fig, ax = plt.subplots()


convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

clus_nums=sorted(cluster_count.keys(),key = alphanum_key)
percents=[]
for i in clus_nums:
    x=float(cluster_count[i]["genes_with_pli_filter_applied"])
    y=float(cluster_count[i]["genes_with_pli"])
    percents.append((x/y)*100.0)

print(percents)


index = np.arange(len(clus_nums))

plt.bar(index, percents, color='green')
plt.xticks(index, clus_nums, fontsize=5, rotation=30)
plt.ylabel('Percentage', fontsize=5)

fig.tight_layout()

plt.savefig(region+"_percent.png",dpi=300, bbox_inches='tight')                
