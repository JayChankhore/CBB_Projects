library(clusterProfiler)
library(org.Hs.eg.db)

# Load your gene list
genes_to_test <- readLines("my_nrf1_genes.txt")

# Convert Symbols to Entrez IDs
gene_df <- bitr(genes_to_test, 
                fromType = "SYMBOL",
                toType = "ENTREZID",
                OrgDb = org.Hs.eg.db)

gene_ids <- unique(gene_df$ENTREZID)

# Run the GO Enrichment
ego <- enrichGO(gene = gene_ids,
                OrgDb = org.Hs.eg.db,
                ont = "BP",
                readable = TRUE)

# Create and save the dot plot
library(ggplot2)
png("nrf1_dotplot.png", width = 800, height = 1000)
dotplot(ego, showCategory = 15) + ggtitle("NRF1 Targeted Pathways")
dev.off()