acc <- readRDS("/Users/asmaimran/MBRU/AbdulRahman_study/acc/acc.rds")
tsne_acc <- DimPlot(acc, reduction = "tsne", label.size=10, pt.size=1.0, label=TRUE) + NoAxes() + NoLegend()
ggsave(file="/Users/asmaimran/MBRU/AbdulRahman_study/acc/tsne_acc.svg", plot=tsne_acc, width=15, height=15, dpi=600)