import json
import sys
import csv

exon_row_data=sys.argv[1]
with open(exon_row_data,"r") as erd:
    ecsv=csv.reader(erd)
    next(ecsv)
    exon_dict={}
    for exon in ecsv:
        ensembl_gene_id=exon[2]
        start=exon[5]
        end=exon[6]
        chromosome=exon[7]
        if chromosome in exon_dict:
            ensembl_ids=exon_dict[chromosome]
            if ensembl_gene_id in ensembl_ids:
                locations=ensembl_ids[ensembl_gene_id]
                locations[start+"-"+end]=0
                ensembl_ids[ensembl_gene_id]=locations
            else:
                ensembl_ids[ensembl_gene_id]={start+"-"+end:0}
            exon_dict[chromosome]=ensembl_ids
        else:            
            exon_dict[chromosome]={ensembl_gene_id:{start+"-"+end:0}}

with open("exons.json","w") as ejson:
    json.dump(exon_dict,ejson,indent=4,sort_keys=True) 
