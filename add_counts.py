import json
import csv
import sys

exon_counts=sys.argv[1]
row_metadata=sys.argv[2]

with open(exon_counts,"r") as ec:
    e_json=json.load(ec) 

exons_count_l=[]

with open(row_metadata,"r") as rm:
    reader=csv.reader(rm)
    header=next(reader, None)
    for row in reader:
        chr=row[7]
        ensembl_id=row[2]
        start=row[5]
        end=row[6]
        length=int(row[8])
        count=int(e_json[chr][ensembl_id][start+"-"+end])
        fm=float(count)/float(length)
        row.extend([str(count),str(fm)])
        exons_count_l.append(row)

new_header=header+["count","FM_burden"]
with open("rows_metadata_chr_counts.csv","w") as wc:
    writer=csv.writer(wc)
    writer.writerow(new_header)
    writer.writerows(exons_count_l) 
