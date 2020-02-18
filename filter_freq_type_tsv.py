import sys
import cyvcf
import json
import re
import csv

exactsvfile=sys.argv[1]
headers=[]
        
consequences=["splice_acceptor_variant",
             "splice_donor_variant",
             "stop_gained",
             "frameshift_variant",
             "stop_lost",
             "start_lost",
             "inframe_insertion",
             "inframe_deletion",
             "missense_variant",
             "protein_altering_variant",
             "splice_region_variant"]

'''
JSON structure:
{ChrNum:{ensembl_id:[loc1,loc2...]}
'''


json_dict={}

with open(exactsvfile,"r") as vr:
    reader=csv.DictReader(vr,delimiter='\t')
    for row in reader:
        chrom="chr"+row["CHROM"]
        ensembl_id=row["Gene"]
        pos=int(row["POS"])
        filter=row["FILTER"]
        #print "Chromosome "+ chrom
        #print "Ensembl id "+ensembl_id
        #print "Pos "+pos
        #print "AC_Adj "+row["AC_Adj"]
        #print "AN_Adj "+row["AN_Adj"] 
        #print "--------------"
        if row["Consequence"] in consequences and filter=="PASS":
            if float(row["AN_Adj"]) == 0:
                af==0
            else:
                af=float(row["AC_Adj"])/float(row["AN_Adj"])
            if af < 0.001:
                if chrom in json_dict:
                    ensembl_ids_dict=json_dict[chrom]
                    if ensembl_id in ensembl_ids_dict:
                        pos_list=ensembl_ids_dict[ensembl_id]
                        pos_list.append(pos)
                        ensembl_ids_dict[ensembl_id]=pos_list
                    else:
                        ensembl_ids_dict[ensembl_id]=[pos]
                    json_dict[chrom]=ensembl_ids_dict
                else:
                    json_dict[chrom]={ensembl_id:[pos]}


with open("ExAC.r1.sites.vep.filtered.tsv.json","w") as ejson:
    json.dump(json_dict,ejson,indent=4,sort_keys=True)
