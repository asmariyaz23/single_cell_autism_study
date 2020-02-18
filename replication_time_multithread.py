from multiprocessing import Pool
import multiprocessing
import numpy as np
from itertools import repeat
import sys
import csv
import json

def load_json(gen_path):
    with open(gen_path,"r") as g:
        return(json.load(g))

def comparison_range(replication,id_dict):
    l=[]
    chr=replication[0]
    start_mut=int(replication[1])
    end_mut=int(replication[2])
    rep_time=float(replication[3])
    if chr in id_dict:
        all_genes=id_dict[chr]
        i=0
        for gene in all_genes:
            gene_range=range(all_genes[gene]["start"],all_genes[gene]["end"]+1)
            if (start_mut in gene_range) and (end_mut in gene_range):
                l.append([chr,start_mut,end_mut,rep_time,gene])
                i=1
        if i==0:
            l.append([chr,start_mut,end_mut,rep_time,np.nan])
    else:
        print("Chromosome not found in database: " + chr)
    return(l)


if __name__ == '__main__':
   
    bed_replication=sys.argv[1]
    database_json=sys.argv[2]
    anno_output=sys.argv[3]

    id_dict=load_json(database_json)

    # Define the dataset
    with open(bed_replication,"r") as br:
        data=list(list(rec) for rec in csv.reader(br, delimiter='\t'))

    data_rep=data[1:]

    # Run this with a pool of 5 agents having a chunksize of 3 until finished
    agents=5
    chunksize=3
    use_num_cpu=multiprocessing.cpu_count()-1

    with Pool(processes=use_num_cpu) as pool:
        result=pool.starmap(comparison_range, zip(data_rep, repeat(id_dict)), chunksize)

    with open(anno_output,"w") as ww:
        writer=csv.writer(ww,delimiter="\t")
        writer.writerows(result)
