import gffutils
import sys
import json
import csv

gencodedb=sys.argv[1]
#expressionrows=sys.argv[2]
#db=gffutils.create_db(gencodegtf, "gencodev10.db")
db=gffutils.FeatureDB(gencodedb,keep_order=True)
features = db.all_features()
id_dict={}
for feat in features:
    chr_num=feat[0]
    gene_id=(feat[8]["gene_id"][0]).split(".")[0]
    gene_name=feat[8]["gene_name"][0]
    
    if gene_id in id_dict:
        already=id_dict[gene_id]
        if not (chr_num,gene_name) in already:
            already.append((chr_num,gene_name))
    else:
        id_dict[gene_id]=[(chr_num,gene_name)]


with open("rows_metadata_chr.csv","w") as wr:
    writer=csv.writer(wr)
    writer.writerow(["row_num","gene_id","ensembl_gene_id","gene_symbol",
                     "entrez_id","start","end","chromosome","length"])
    with open(expressionrows,"r") as er:
        csv_reader=csv.reader(er, delimiter=',')
        header=next(csv_reader)
        for row in csv_reader:
            val=id_dict[row[2]]
            start=int(row[5])
            end=int(row[6])
            length=str(end-start)
            chr=val[0][0]
            writer.writerow(row+[chr,length])
