import pandas as pd
from pandas import DataFrame
import csv

#mut_expression_percentile=4.548912
mut_expression_percentile=6.388519
fm_burden_percentile=0.09541985

retain=["row_num","gene_id","ensembl_gene_id","gene_symbol",
        "entrez_id","start","end","chromosome","length","count","FM_burden"]


expr_vec=range(1,525)
expr_vec_str=["X"+str(expr) for expr in expr_vec]
CE_matrix_list=[]

with open("abi.developmental_matrix.expression.csv","r") as cm:
    exon_df=pd.read_csv(cm)
    for index, row in exon_df.iterrows():
        CE_matrix=[]
        fm=float(row["FM_burden"])
        if fm < fm_burden_percentile:
            for expr_header in expr_vec_str:
                cell_expr=float(row[expr_header])
                if cell_expr > mut_expression_percentile:
                    CE_matrix.append("1")
                else:
                    CE_matrix.append("0")
        else:
            CE_matrix=["0"]*524
        info=[row[ele] for ele in retain]
        CE_matrix_list.append(info+CE_matrix)

with open("abi.developmental_matrix.binary.csv","w") as cw:
    header=list(exon_df)
    CE_matrix_list.insert(0,header)
    writer=csv.writer(cw)
    writer.writerows(CE_matrix_list)
