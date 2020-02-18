#!/usr/bin/env Rscript
library(dplyr)

args <- commandArgs(TRUE)
filename_matrix <- args[1]
CN <- args[2]
write_file <- args[3]

v<-readRDS(filename_matrix)
region_ml <- v %>% select(p_val,avg_logFC,pct.1,pct.2,p_val_adj,gene,cluster) %>% filter(cluster==CN & p_val<=0.01)
#write.table(region_ml, write_file, append = FALSE, sep = "\t", dec = ".",
#            row.names = TRUE, col.names = TRUE)
saveRDS(region_ml, file=write_file)
