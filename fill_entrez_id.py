import csv
import sys
import json 

def read_file(gene_file):
    gene_list=[]
    with open(gene_file,"r") as gf:
        for gene in gf:
            gene_list.append(gene)
    return(gene_list)

def gene_entrez_id(entire_file):
    d={}
    with open(entire_file, "r") as ef:
        reader=csv.reader(ef,delimiter=',')
        next(reader)
        d={rows[1]:rows[0] for rows in reader}
    return(d)

def combine(cluster_list,entire_list):
    c_dict={}
    for gene in cluster_list:
        for k,v in entire_list.items():
            if v==(gene.strip()).strip('"'):
                if k in c_dict:
                    c_dict[k]=(c_dict[k]).append(v)
                    print("Multiple_gene_ids found "+k)
                else: 
                    c_dict[k]=[v]
    return(c_dict)     

def write(gene_dict,cluster_gene_id):
    with open(cluster_gene_id, "w") as gd:
        writer = csv.writer(gd, delimiter="\t")
        for g,d in gene_dict.items():
            writer.writerow([g,','.join(d)])

cluster_file1=sys.argv[1]
entire_file2=sys.argv[2]
output=sys.argv[3]
cluster_list1=read_file(cluster_file1)
entire_list2=gene_entrez_id(entire_file2)
cluster_id_sym=combine(cluster_list1,entire_list2)
write(cluster_id_sym,output)
