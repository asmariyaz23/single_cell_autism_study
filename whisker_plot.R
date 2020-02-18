library('ggplot2')
library('tidyverse')
args <- commandArgs(TRUE)
cluster_file <- args[1]

dat <- read.csv(cluster_file, header=TRUE, sep='\t' , stringsAsFactors = FALSE)

status <- c("Cluster0","Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5",
            "Cluster6","Cluster7", "Cluster8", "Cluster9", "Cluster10", "Cluster11",
            "Cluster12","Cluster13", "Cluster14", "Cluster15", "Cluster16")

plot_pdf<-paste((tools::file_path_sans_ext(basename(cluster_file))),".pdf",sep = "")
pdf(plot_pdf)
(p <- ggplot(dat, aes(x = odds_ratio, y = factor(status,levels=c("Cluster0","Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5",
                                                                 "Cluster6","Cluster7", "Cluster8", "Cluster9", "Cluster10", "Cluster11",
                                                                 "Cluster12","Cluster13", "Cluster14", "Cluster15", "Cluster16")))) + 
    geom_vline(aes(xintercept = 1), size = .25, linetype = "dashed") +
    geom_errorbarh(aes(xmax = dat$ucl, xmin = dat$lcl), size = .5, height =
                .2, color = "gray50") + 
    geom_point(size = 2, color = "orange") +
    scale_x_continuous(breaks = seq(1.0, 5.0, 0.1), labels = seq(1.0, 5.0, 0.1),
                       limits =  c(0.3,5.0)) +
    theme_bw()+
    theme(panel.grid.minor = element_blank()) +
    ylab("") +
    xlab("Odds ratio") +
    ggtitle(tools::file_path_sans_ext(basename(cluster_file)))
) 
dev.off()
