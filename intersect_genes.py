import csv
import sys

def read_file(gene_file):
    gene_list=[]
    with open(gene_file,"r") as gf:
        for gene in gf:
            gene_list.append(gene)
    gene_list_stripped = map(lambda each:each.strip(), gene_list)
    return(gene_list_stripped)

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

gene_file1=sys.argv[1]
gene_file2=sys.argv[2]
gene_list1=read_file(gene_file1)
gene_list2=read_file(gene_file2)
print(len(intersection(gene_list1, gene_list2)))
