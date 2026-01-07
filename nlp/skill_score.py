from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=40
)

def skills_match(resume: str, job: str) -> int:
    tfidf = vectorizer.fit_transform([job])
    features = vectorizer.get_feature_names_out()

    matched = sum(1 for f in features if f.lower() in resume.lower())

    if not features.any():
        return 0

    return int(round((matched / len(features)) * 100))
