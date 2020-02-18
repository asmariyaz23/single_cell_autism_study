import csv
import sys

def read_mapping(gene_file):
    gene_list={}
    with open(gene_file,"r") as gf:
        for gene_line in gf:
            sym=gene_line.split(",")[0]
            eid=(gene_line.split(",")[1]).strip("\n")
            gene_list[sym]=eid
    print gene_list
    return(gene_list)

def cluster(rank_file):
    cluster_list={}
    with open(rank_file,"r") as gf:
         for gene_line in gf:
             fc=(gene_line.split("\t")[0]).strip()
             sym=(gene_line.split("\t")[1]).strip()
             cluster_list[sym]=fc
    print cluster_list
    return(cluster_list)

def mapping(cluster_read,mapping_dict):
    id_rank={}
    for gene,fc in cluster_read.items():
        id=mapping_dict[gene]
        id_rank[id]=fc        
    return(id_rank)

def write_rank(id_rank):
    with open("acc0_id.rnk", 'w') as f:
        for key in id_rank.keys():
            f.write("%s\t%s\n"%(key,id_rank[key]))


mapping_f=sys.argv[1]
cluster_f=sys.argv[2]
mapping_dict=read_mapping(mapping_f)
cluster_read=cluster(cluster_f)
id_rank=mapping(cluster_read,mapping_dict)
write_rank(id_rank)
