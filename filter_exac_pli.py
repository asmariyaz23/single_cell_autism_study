import sys
import pandas as pd


exac_pli=sys.argv[1]
with open(exac_pli,"r") as pr:    
    df=pd.read_csv(pr,delimiter="\t")
    filtered=df[df.pLI > 0.9]
    filtered.to_csv("exac_pli_highpli.tsv",sep="\t")
