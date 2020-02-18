import json
import sys

mut_file=sys.argv[1]
exon_file=sys.argv[2]

with open(mut_file,"r") as mf, open(exon_file,"r") as ef:
    mut_json=json.load(mf)
    exon_json=json.load(ef)
    for chr in exon_json:
        ensembl_ids=exon_json[chr]
        for ensembl in ensembl_ids:
            locations=ensembl_ids[ensembl]
            for location in locations:
                actual_start=int(location.split("-")[0])
                actual_end=int(location.split("-")[1])
                new_start=actual_start-3
                new_end=actual_end+3
                counts=0
                if chr in mut_json:
                   if ensembl in mut_json[chr]:
                       possible_mutations=mut_json[chr][ensembl]
                       for mut in possible_mutations:
                           if int(mut) > new_start and int(mut) < new_end:
                               counts=counts+1
                exon_json[chr][ensembl][location]=counts

with open("exon_mut_counts.json","w") as wf:
    json.dump(exon_json,wf,indent=4,sort_keys=True)
    
