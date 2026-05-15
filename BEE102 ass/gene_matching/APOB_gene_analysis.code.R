
library(EnsDb.Hsapiens.v86)
library(ensembldb)
library(IRanges)
library(dplyr)


edb <- EnsDb.Hsapiens.v86


tx <- transcripts(edb,
                  filter = GeneNameFilter("APOB"),
                  columns = c("gene_id","seq_name","tx_id","tx_biotype","tx_name")) %>%
  as.data.frame()
print(tx)


prots <- proteins(edb,
                  filter = GeneNameFilter("APOB"),
                  columns = c("gene_id","seq_name","protein_id","tx_id","protein_length")) %>%
  as.data.frame()
print(prots)


cds <- cdsBy(edb, by = "tx", filter = GeneNameFilter("APOB"))


cds_df <- as.data.frame(unlist(cds), row.names = NULL) %>%
  mutate(tx_id = names(unlist(cds)))   # keep transcript ID as a column
print(cds_df)

ranges <- IRanges(start = rep(1, nrow(prots)),
                  end = prots$protein_length,
                  names = prots$protein_id)

prot2genome <- proteinToGenome(ranges, edb)


prot2genome_df <- as.data.frame(prot2genome, row.names = NULL)
print(prot2genome_df)
