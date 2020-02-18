import sys
import cyvcf
import json
import re

vcfile=sys.argv[1]
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
with open(vcfile,"r") as vr:
    vcf_reader = cyvcf.Reader(vr)
    for record in vcf_reader:
        #rec_list=record.split("\t")
        info_dict={}
        csq=record.INFO["CSQ"]
        csq_list=csq.split("|")
        consequence=csq_list[1]
        ensembl_gene_id=csq_list[4]
        if (consequence in consequences):
            AC_Adj=float(record.INFO["AC_Adj"][0])
            AN_Adj=float(record.INFO["AN_Adj"])
            maf=AC_Adj/AN_Adj
            if (maf < 0.001):
                chr="chr"+record.CHROM
                pos=int(record.POS)
                ensembl_gene_id=csq_list[4]
                if chr in json_dict:
                    ensembl_ids_dict=json_dict[chr]
                    if ensembl_gene_id in ensembl_ids_dict:
                        pos_list=ensembl_ids_dict[ensembl_gene_id]
                        pos_list.append(pos)
                        ensembl_ids_dict[ensembl_gene_id]=pos_list
                    else:
                        ensembl_ids_dict[ensembl_gene_id]=[pos]
                    json_dict[chr]=ensembl_ids_dict
                else:
                    json_dict[chr]={ensembl_gene_id:[pos]} 

with open("ExAC.r1.sites.vep.filtered.json","w") as ejson:
    json.dump(json_dict,ejson,indent=4,sort_keys=True)
