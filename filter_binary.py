import pandas as pd

first_h=["row_num","gene_id","ensembl_gene_id",
         "gene_symbol","entrez_id","start","end",
         "chromosome","length","count","FM_burden"]

no_include=["CB","CGE","DTH","LGE","MGE",
            "Ocx","PCx","TCx","URL"]

with open("abi.developmental_matrix.binary.csv","r") as ab:
    df=pd.read_csv(ab)
    headers=list(df)
    p_df=df[first_h]
    for h in headers[11:]:
        kwargs = {h : df[h]}
        if h.split("-")[2] not in no_include:
            p_df=p_df.assign(**kwargs)
    with open("abi.developmental_matrix.binary.filtered.csv","w") as wh:
        p_df.to_csv(wh,index=False) 
