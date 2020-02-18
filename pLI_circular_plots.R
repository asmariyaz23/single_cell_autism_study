require(ggplot2)

# function to compute standard error of mean
#se <- function(x) sqrt(var(x)/length(x)) 
#set.seed(9876) 

df=data.frame(read.csv("/Users/asmaimran/MBRU/AbdulRahman_study/visp/ORAfile_visphigh_pli_allTests_updated.csv"))

# calculate the ANGLE of the labels
number_of_bar <- nrow(df)
angle <-  90 - 360 * (df$pathwayid) /number_of_bar     

# calculate the alignment of labels: right or left
# If I am on the left part of the plot, my labels have currently an angle < -90
df$hjust<-ifelse( angle < -90, 1, 0)

# flip angle BY to make them readable
df$angle<-ifelse(angle < -90, angle+180, angle)

pli_plot <- ggplot(df, aes(pathwayid, Overlap, fill = -log10(Pvalue))) +
  geom_bar(width = 1, stat = "identity", color = "white") +
  #scale_y_continuous(breaks = 0:nlevels(df$pathwayname)) +
  scale_fill_distiller(palette = "Oranges", direction = +1,guide=guide_colorbar(text = element_text(size=20),barwidth=2,barheight=10)) +
 # theme(axis.ticks = element_blank(),
#        axis.text = element_blank(),
#        axis.title = element_blank(),
#        axis.line = element_blank(),
#        panel.grid = element_blank(),
#        plot.margin = unit(rep(-1,4), "cm")) +
  ggtitle("VISp region - Overlapped genes with pLI > 0.9") +
  xlab("Clusters") + 
  theme_minimal() + 
  theme(axis.text.x=element_blank(),axis.title.x = element_text(size = 18),axis.title.y = element_text(size = 18),plot.title = element_text(size=20, face="bold",hjust = 0.5)) +
  geom_text(data=df, aes(x=pathwayid, y=Overlap+10, label=pathwayid, hjust=df$hjust), color="black", size=3, angle= df$angle, inherit.aes = FALSE ) +
  coord_polar() 
ggsave(file="/Users/asmaimran/MBRU/AbdulRahman_study/visp/visp_pli_shades_plots/visp_pLI_circular.svg",plot=pli_plot, width=15, height=15, dpi=600)

