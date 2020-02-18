import csv
import os
import sys
import re


fisher_dir=sys.argv[1]
title=sys.argv[2]


_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]   

fisher_list=os.listdir(fisher_dir)
all_clusters={}
for fisher_result in fisher_list:
    r=os.path.join(fisher_dir,fisher_result)
    if os.path.isfile(r) and r.endswith("_fisher"):
        print fisher_result
	with open(os.path.join(fisher_dir,fisher_result),"r") as ff:
            lines = ff.read().splitlines()
	    all_clusters[fisher_result]={}
	    for i,line in enumerate(lines):
                print line
                sl=line.strip("\n")
		if i==3:
		    all_clusters[fisher_result]["total_cluster_markers"]=sl
		if i==6:
		    all_clusters[fisher_result]["total_gene_list"]=sl
		if i==9:
	            all_clusters[fisher_result]["overlap"]=sl
		if i==12:
		    all_clusters[fisher_result]["confidence_interval"]=sl
		if i==14:
		    all_clusters[fisher_result]["p-value"]=sl
		if i==16:
		    all_clusters[fisher_result]["log_odds_ratio"]=sl


with open(os.path.join(fisher_dir,title.replace(" ","_")+".csv"),"w") as fw:
    fisher_writer=csv.writer(fw,delimiter='\t',lineterminator="\n") 
    fw.write(title+"\n")
    fisher_writer.writerow(["#Cluster",
                            "total_cluster_markers",
                            "total_gene_list",
                            "overlap",
                            "confidence_interval",
                            "p-value",
                            "log_odds_ratio"])

    for cluster in sorted(all_clusters.iterkeys(),key=natural_sort_key):
        value=all_clusters[cluster]
        fisher_writer.writerow([cluster,
                                value["total_cluster_markers"],
                                value["total_gene_list"],
                                value["overlap"],
                                value["confidence_interval"],
                                value["p-value"],
                                value["log_odds_ratio"]])
