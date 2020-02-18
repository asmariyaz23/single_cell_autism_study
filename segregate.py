import pandas as pd
import os

first_h=["row_num","gene_id","ensembl_gene_id",
         "gene_symbol","entrez_id","start","end",
         "chromosome","length","count","FM_burden"]


regions=['HIP', 'OFC', 'M1C', 'MFC', 'A1C', 'STC', 
         'CBC', 'VFC', 'ITC', 'AMY', 'STR', 'IPC', 
         'S1C', 'V1C', 'MD', 'DFC']

## segregating stage region wise
all_regions=[os.path.join("regions_matrix",r) for r in os.listdir("regions_matrix")]
for r in regions:
    path=os.path.join("regions_matrix",r+".csv")
    with open(path,"r") as rs:
        reg_df=pd.read_csv(rs)
        header=list(reg_df)
        reg_prenatal_df=reg_df[first_h]
        reg_early_df=reg_df[first_h]
        reg_adult_df=reg_df[first_h]
        for h in header[11:]:
            kwargs={h:reg_df[h]}
            if "-PN-" in h:
                reg_prenatal_df=reg_prenatal_df.assign(**kwargs)
            elif "-EC-" in h:
                reg_early_df=reg_early_df.assign(**kwargs)
            else:
                reg_adult_df=reg_adult_df.assign(**kwargs)            
        w_files={r+"_prenatal.csv":reg_prenatal_df,
                 r+"_early_childhood.csv":reg_early_df, 
                 r+"_adulthood.csv":reg_adult_df}
        for f,df in w_files.iteritems():
            with open(os.path.join("regions_stage_matrix",f),"w") as rsw:
                df.to_csv(rsw)


'''
## segregating region wise
with open("abi.developmental_matrix.binary.filtered.csv","r") as rh:
    abi_matrix=pd.read_csv(rh)
    header=list(abi_matrix)
    for region in regions:
        with open(os.path.join("regions_matrix",region+".csv"),"w") as nh:
             p_df=abi_matrix[first_h]
             for h in header[11:]:
                 kwargs={h:abi_matrix[h]}
                 if region in h:
                     p_df=p_df.assign(**kwargs)

             p_df.to_csv(nh,index=False)


## segregating development stage wise
with open("abi.developmental_matrix.binary.filtered.csv","r") as rh:
    abi_matrix=pd.read_csv(rh)
    header=list(abi_matrix)
    with open("prenatal","w") as p, open("early_childhood","w") as e, open("adulthood","w") as a:
        p_df=abi_matrix[first_h]
        a_df=abi_matrix[first_h]
        e_df=abi_matrix[first_h]
        for h in header[11:]:
            kwargs = {h : abi_matrix[h]}
            if "-PN-" in h:
                p_df=p_df.assign(**kwargs)
            elif "-EC-" in h:
                e_df=e_df.assign(**kwargs)
            else:
                a_df=a_df.assign(**kwargs)

        p_df.to_csv(p,index=False)
        e_df.to_csv(e,index=False)
        a_df.to_csv(a,index=False)
'''


