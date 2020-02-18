args <- commandArgs(TRUE)
matrix <- args[1]
df <- read.table(matrix,header = FALSE)
cat("Conf Intervals \n")
cat(paste(fisher.test(df)$conf.int[[1]],fisher.test(df)$conf.int[[2]]),collapse='\n')
cat("P-val \n")
cat(fisher.test(df)$p.value,collapse='\n')
cat("Log Odds \n")
cat(fisher.test(df)$estimate,collapse='\n')
