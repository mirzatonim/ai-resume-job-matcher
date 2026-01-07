import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset once
pairs = pd.read_csv("data/pairs.csv")

corpus = (
    pairs["resume_text"].astype(str).tolist() +
    pairs["job_text"].astype(str).tolist()
)

vectorizer = TfidfVectorizer(
    stop_words="english",
    min_df=2,
    max_df=0.85,
    ngram_range=(1, 2)
)

# Fit ONCE on real corpus
vectorizer.fit(corpus)

def keyword_match(resume: str, job: str) -> int:
    tfidf = vectorizer.transform([resume, job])
    score = cosine_similarity(tfidf[0], tfidf[1])[0][0]
    return int(round(score * 100))
