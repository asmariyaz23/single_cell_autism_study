library (tidyr)
library(ggplot2)
library(viridis)
df=data.frame(read.csv("/Users/asmaimran/MBRU/AbdulRahman_study/mtg/ORAfile_mtghigh_pli_allTests_updated.csv"))
region="MTG" 

pl=c("Oranges","Blues","Reds","Purples","Greens")
for (i in 1:length(pl)) {
  pli_plot <- ggplot(df,aes(x=pathwayid,y=Oddsratio,fill=-log10(Pvalue))) + xlab("Clusters") +
    ggtitle(paste(region,"region - genes with pLI > 0.9",sep=" ")) +
    ylab("Odds Ratio") +
    geom_col(position="dodge",width=0.4,size=0.7) + 
    coord_flip() + 
    scale_fill_distiller(palette = pl[[i]], direction = +1,guide=guide_colorbar(text = element_text(size=20),barwidth=2,barheight=10)) +
    scale_x_continuous(breaks=seq(0, 17, 1)) +
    theme(plot.title = element_text(size=20, face="bold",hjust = 0.5),text = element_text(size=20),panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          panel.background = element_blank(), axis.line = element_line(colour = "black"))
  ggsave(file=paste("/Users/asmaimran/MBRU/AbdulRahman_study/mtg/try_pli_shades_plots/mtg_pli",paste(pl[[i]],".svg",sep=''),sep='_'), plot=pli_plot, width=15, height=15, dpi=600)
}
  
