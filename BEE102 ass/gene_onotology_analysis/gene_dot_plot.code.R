library(clusterProfiler)
library(org.Hs.eg.db)
genes = read.table("gene_list_tss_upstream_with_pattern/optimal_site_nrf1_in_hg38_tss_upstream_500.genes.tsv", 
                   sep = "\t", header = F, stringsAsFactors = F)$V1
ego <- enrichGO(gene         = genes,
                OrgDb        = org.Hs.eg.db,
                keyType      = "SYMBOL",
                ont          = "BP",
                pAdjustMethod = "BH",
                qvalueCutoff = 0.01)

write.csv(as.data.frame(ego), "GO_annotation_results.csv")
pdf ("dotplot.pdf", height = 8, width = 8)
dotplot(ego, showCategory =20, font.size = 6)
dev.off()
