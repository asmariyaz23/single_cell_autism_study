asdexon=[]
with open("ASDExongenelist_gene_symbols.csv","r") as asd:
    for line in asd:
        tl=line.split(";")
        ml=map(str.strip,tl)
        asdexon=asdexon+ml

with open("ASDExongenelist_genes.csv","w") as wsd:
    for item in asdexon:
        wsd.write("%s\n" % item)
