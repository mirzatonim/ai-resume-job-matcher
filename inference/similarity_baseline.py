import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
pairs = pd.read_csv("data/pairs.csv")

# Load model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Encode texts
resume_embeddings = model.encode(
    pairs["resume_text"].tolist(),
    show_progress_bar=True
)

job_embeddings = model.encode(
    pairs["job_text"].tolist(),
    show_progress_bar=True
)

# Compute cosine similarity
similarities = [
    cosine_similarity([r], [j])[0][0]
    for r, j in zip(resume_embeddings, job_embeddings)
]

pairs["similarity_score"] = similarities

# Analyze results
positive_avg = pairs[pairs["label"] == 1]["similarity_score"].mean()
negative_avg = pairs[pairs["label"] == 0]["similarity_score"].mean()

print("Average similarity (Positive pairs):", round(positive_avg, 3))
print("Average similarity (Negative pairs):", round(negative_avg, 3))

# Optional threshold accuracy
threshold = 0.5
pairs["prediction"] = (pairs["similarity_score"] > threshold).astype(int)

accuracy = (pairs["prediction"] == pairs["label"]).mean()
print("Baseline accuracy:", round(accuracy, 3))
