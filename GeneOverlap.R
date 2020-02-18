args <- commandArgs(TRUE)
gmt_file <- args[1]
geneList <- args[2]
output1 <-args[3]
#output2 <-args[4]

#define the format of the result table
tabledata= data.frame(pathway_id=character(),Pathway_name=character(),pathway_len=integer(),Genelist_len=integer(),Overlap=integer(),Pvalue = double(), Oddsratio = double(), stringsAsFactors=FALSE)
overlapdata= data.frame(clusterid=character(),de_genes=character(), stringsAsFactors=FALSE)
#load required libraries
library(GeneOverlap)
library(cogena)
library(tidyverse)
library(dplyr)


#load input

allpath= gmt2list(gmt_file)
exon<-read_csv(geneList,col_names = FALSE)
genelist<-as.vector(exon$X1)
#loop and pairwase comparison between each pathway and the input genelist using geneoverlap (one sided FET)
for (i in 1:length(allpath))
{
  pathway= as.data.frame(allpath[i])[,1]
  if (length(pathway) <50  | length(pathway) > 1000) 
  {next()}
  go.obj <- newGeneOverlap(pathway,as.vector(genelist))
  go.obj <- testGeneOverlap(go.obj)
  tabledata[i, 6] = go.obj@pval
  tabledata[i, 7] = go.obj@odds.ratio
  tabledata[i, 2] = strsplit(names(allpath[i]), "%")[[1]][1]
  tabledata[i, 1] = strsplit(names(allpath[i]), "%")[[1]][3] 
  tabledata[i, 3] = length(pathway)
  tabledata[i, 4] = length(genelist)
  tabledata[i, 5] = length(go.obj@intersection)
}
tabledata <- tabledata[with(tabledata, order(as.integer(sub('\\D+', '', Pathway_name)))),]
tabledataALL= tabledata[which(tabledata$Pathway_name!= "NA" ),]
tabledataALL= tabledataALL %>% arrange(tabledataALL$Pvalue)
newp = p.adjust(tabledataALL$Pvalue, method = "fdr", n = length(tabledataALL$Pvalue))
tabledataALL= tabledataALL %>%  mutate(FDR = newp)
tabledataALL = tabledataALL [which(tabledataALL$FDR< 0.01 ),]

#for (i in 1:length(allpath))
#{
#  pathway= as.data.frame(allpath[i])[,1]
#  go.obj <- newGeneOverlap(pathway,as.vector(genelist))
#  go.obj <- testGeneOverlap(go.obj)
#  overlapdata[i, 1] <- strsplit(names(allpath[i]), "%")[[1]][1]
#  overlapdata[i, 2] <- paste(go.obj@intersection,collapse = ",")
#}
#overlapdata <- overlapdata[with(overlapdata, order(as.integer(sub('\\D+', '', clusterid)))),]

#Save final result table "tabledataALL" to a csv file in the directory
write.csv(tabledataALL,output1, row.names=FALSE)
#write.csv(overlapdata,output2, row.names=FALSE)
