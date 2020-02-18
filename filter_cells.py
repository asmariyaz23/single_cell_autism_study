import pandas as pd
import csv
import numpy as np

exon_matrix=pd.read_csv("/Users/asma/Downloads/human_MTG_gene_expression_matrices_2018-06-14/human_MTG_2018-06-14_exon-matrix.csv")
#exon_matrix=pd.read_csv("small_exp.csv")
exon_nan=exon_matrix.replace([0],np.nan)
exon_fil=exon_nan.dropna(thresh=exon_nan.shape[0]*0.9,how='all',axis=1)
