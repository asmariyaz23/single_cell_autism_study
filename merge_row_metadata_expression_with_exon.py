import pandas as pd

with open("rows_metadata_chr_counts.csv","r") as mf, open("/Users/asmaimran/Downloads/matrix","r") as ef:
     metadata=pd.read_csv(mf)
     expression=pd.read_csv(ef)
     df3=pd.merge(metadata,expression,on="ensembl_gene_id")
     all_headers=list(df3)
     needed_metadata=["row_num_x","gene_id_x","ensembl_gene_id",
                      "gene_symbol_x","entrez_id_x","start","end",
                      "chromosome","length","count","FM_burden"]
     expression_headers=[h for h in all_headers if h.startswith("'X")]
     final_matrix_headers=needed_metadata+expression_headers

     with open("abi.csv","w") as af:
         df3[final_matrix_headers].to_csv(af,index=False)
