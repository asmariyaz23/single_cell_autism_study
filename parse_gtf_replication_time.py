import gffutils
import sys
import json
import csv
import os
import numpy as np

'''
#gencodegtf=sys.argv[1]
#expressionrows=sys.argv[2]
#db=gffutils.create_db(gencodegtf, "gencodev32.db")
db=gffutils.FeatureDB("gencodev32.db",keep_order=True)
features = db.all_features()
id_dict={}
for feat in features:
    chr_num=feat[0]
    type=feat[2]
    start=feat[3]
    end=feat[4]
    gene_id=(feat[8]["gene_id"][0]).split(".")[0]
    gene_name=feat[8]["gene_name"][0]
    gene_type=feat[8]["gene_type"][0]
    if type=="gene" and gene_type=="protein_coding":
        if chr_num not in id_dict:
	    id_dict[chr_num]={gene_id:{"start":start,
					    "end":end,
					    "gene_name":gene_name}}
	else:
	    already=id_dict[chr_num]  
	    already[gene_id]={"start":start,
			      "end":end,
			      "gene_name":gene_name}
	    id_dict[chr_num]=already  

with open("gencodev32.json", "w") as write_file:
    json.dump(id_dict, write_file)

'''

input_dir="/Users/asmaimran/MBRU/AbdulRahman_study/early_development"
gen_path="gencodev32.json"
with open(gen_path,"r") as g:
    id_dict=json.load(g)

with open(os.path.join(input_dir,"RT_BG01_NPC_AvgZ_hg38.bedgraph"),"r") as rr:
    mutations=csv.reader(rr,delimiter="\t")
    next(mutations, None)
    l=[]
    for mut in mutations:
        chr=mut[0]
        start_mut=int(mut[1])
        end_mut=int(mut[2])
        rep_time=float(mut[3])
	all_genes=id_dict[chr]
        i=0
        for gene in all_genes:
            gene_range=range(all_genes[gene]["start"],all_genes[gene]["end"]+1)
            if start_mut in gene_range and end_mut in gene_range:
                l.append([chr,start_mut,end_mut,rep_time,all_genes[gene]["gene_name"]])
                i=1
                break               
        if i==0:
            l.append([chr,start_mut,end_mut,rep_time,np.nan])    

 
    with open(os.path.join(input_dir,"RT_BG01_NPC_AvgZ_hg38.ann.csv"),"w") as ww:
        writer=csv.writer(ww,delimiter="\t")
        writer.writerows(l)

