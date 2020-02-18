#define the format of the result table
tabledata= data.frame( pathwayid= character(), pathwayname= character(), Pvalue = double(), Oddsratio = double(), stringsAsFactors=FALSE)
#load required libraries
library(GeneOverlap)
library(cogena)
library(dplyr)
library(gtools)
library(tidyverse)

#load input
exacplihigh=read.csv("/Users/asmaimran/MBRU/AbdulRahman_study/exac_pli_highpli.tsv",sep='\t')

genelists= gmt2list("/Users/asmaimran/MBRU/AbdulRahman_study/visp/visp_plihighgenes.gmt")

#loop and pairwase comparison between each mut list and the input genelist(each cluster is a pathway) using geneoverlap (one sided FET)
mutlist=exacplihigh[["gene"]]
print(mutlist)
for (i in 1:length(genelists)) 
  {
    pathway=as.data.frame(genelists[i])[,1]
    print(pathway) 
    # Restrict analysis to pathways of size 50 to 1000 genes 
    #if (length(pathway) <50  | length(pathway) > 1000) 
    #{next()}
    #use geneoverlap to calculate P value and odds ratio
    go.obj <- newGeneOverlap(pathway,mutlist)
    go.obj <- testGeneOverlap(go.obj)
    tabledata[i, 3] = go.obj@pval
    tabledata[i, 4] = go.obj@odds.ratio
    #Manipulation of string to get desired pathway name and pathway ID
    tabledata[i, 1] = strsplit(names(genelists[i]), "%")[[1]][1] 
    tabledata[i, 2] = strsplit(names(genelists[i]), "%")[[1]][1] 
  }
#remove cells that have NA value (these are the pathways with size greater that 1000 genes and less than 50 genes) and reorder in ascending order of p value
tabledataALL= tabledata[which(tabledata$pathwayid!= "NA" ),]
tabledataALL= tabledataALL %>% arrange(tabledataALL$Pvalue)
  
#My implementation of FDR control and selecting FDR to be less than 0.01
  
newp = p.adjust(tabledataALL$Pvalue, method = "fdr", n = length(tabledataALL$Pvalue))
tabledataALL= tabledataALL %>%  mutate(FDR = newp)
#tabledataALL = tabledataALL [which(tabledataALL$FDR< 0.01 ),]
tabledataALL=tabledataALL[mixedorder(tabledataALL$pathwayid),] 
#Save final result table "tabledataALL" to a csv file in the directory
write.csv(tabledataALL, paste("/Users/asmaimran/MBRU/AbdulRahman_study/visp/exac_visp_enrichment.csv",sep=''), row.names=FALSE)    
 
