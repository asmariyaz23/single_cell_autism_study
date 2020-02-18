library("rjson")
tabledata= data.frame(pathwayname= character(), CE_Stage_Cluster=integer(), Pvalue = double(), Oddsratio = double(), stringsAsFactors=FALSE)
fisherjson <- fromJSON(file = "~/MBRU/AbdulRahman_study/CE_matrix/acc/fisher_prenatal.json")
i=1
for (j in fisherjson)
{ 
  tabledata[i, 1]=j$Cluster_name
  tabledata[i, 2]=j$x
  mat <- matrix(c(j$x,j$`m-x`,j$`T-x`,j$n), nrow = 2)
  fmat <- fisher.test(mat)
  tabledata[i, 3]=fmat$p.value
  tabledata[i, 4]=fmat$estimate
  i=i+1
}
View(tabledata)
