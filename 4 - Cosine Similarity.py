import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

data_folder = "Vectorized Data"
output_file = "Cosine Similarity Results/cosine_similarity_output.txt"

# Clear the output file at the beginning
with open(output_file, 'w') as f:
    f.write("")  # Overwrite with empty content


def load_vector_from_file(path):
    with open(path, 'r') as f:
        return np.array([float(x) for x in f.readline().strip().split(',')]).reshape(1, -1)

# Step 1: Build file pairs
file_pairs = {}

for filename in os.listdir(data_folder):
    if not filename.endswith(".txt"):
        continue

    # Identify base ID
    if " - Final_" in filename:
        base_id = filename.split(" - Final_")[0].strip()
        file_pairs.setdefault(base_id, {})["final"] = filename
    elif "_normalized_tokenized_vectorized.txt" in filename:
        base_id = filename.replace("_normalized_tokenized_vectorized.txt", "")
        file_pairs.setdefault(base_id, {})["base"] = filename

# Debug: show matched pairs
print("📂 Matched Pairs:")
for key, pair in file_pairs.items():
    if "base" in pair and "final" in pair:
        print(f"✔️ {pair['base']}  +  {pair['final']}")

# Step 2: Compute similarity
results = []
for key, pair in file_pairs.items():
    if "base" in pair and "final" in pair:
        try:
            vec1 = load_vector_from_file(os.path.join(data_folder, pair["base"]))
            vec2 = load_vector_from_file(os.path.join(data_folder, pair["final"]))

            if vec1.shape[1] != vec2.shape[1]:
                print(f"⚠️ Skipping {key}: Vector length mismatch ({vec1.shape[1]} vs {vec2.shape[1]})")
                continue

            sim = cosine_similarity(vec1, vec2)[0][0]
            results.append((key, sim))
        except Exception as e:
            print(f"❌ Error processing {key}: {e}")

# Step 3: Save output
with open(output_file, 'w') as out:
    out.write("File Name,Cosine Similarity\n")
    for name, sim in results:
        out.write(f"{name},{sim:.6f}\n")

print(f"✅ Done. Results written to '{output_file}'")
