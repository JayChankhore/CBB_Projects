import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Load class labels
class_data = pd.read_csv("class.tsv", sep="\t", header=None)

# Load filtered gene expression data
filtered_data = pd.read_csv(
    "filtered.tsv.gz",
    sep="\t",
    compression="gzip"
)

# Load columns data
columns_data = pd.read_csv(
    "columns.tsv.gz",
    sep="\t",
    compression="gzip",
    engine="python",
    on_bad_lines="skip"
)

print("Class Data:")
print(class_data.head())

print("\nFiltered Data:")
print(filtered_data.head())

# Remove non-numeric column if present
numeric_data = filtered_data.select_dtypes(include=['number'])

# Transpose data
X = numeric_data.T

# PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X)

# Plot
plt.figure(figsize=(8,6))

plt.scatter(
    principal_components[:,0],
    principal_components[:,1]
)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Plot")

plt.savefig("pca_plot.png")

print("\nPCA completed successfully.")