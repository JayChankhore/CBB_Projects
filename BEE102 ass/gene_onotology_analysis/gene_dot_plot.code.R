genes = read.table(
  "/home/userjay_chankhore/my_nrf1_genes.txt",
  header = FALSE,
  stringsAsFactors = FALSE
)$V1

# GO enrichment
ego <- enrichGO(
  gene = genes,
  OrgDb = org.Hs.eg.db,
  keyType = "SYMBOL",
  ont = "BP",
  pAdjustMethod = "BH",
  qvalueCutoff = 0.01
)

# Save results
write.csv(as.data.frame(ego), "GO_annotation_results.csv")

# Create PNG plot
png("dotplot.png", width = 1200, height = 1200)

dotplot(
  ego,
  showCategory = 20,
  font.size = 8
)

dev.off()
