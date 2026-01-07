from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.keyword_score import keyword_match
from nlp.experience_score import experience_match_score
from nlp.skill_score import skills_match


app = FastAPI(title="Resume Job Matcher AI")

# Load model ONCE
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class MatchRequest(BaseModel):
    resume: str
    job: str

class MatchResponse(BaseModel):
    similarity_score: float
    match: bool
    skillsMatch: int
    experienceMatch: int
    keywordsMatch: int

@app.post("/match-score", response_model=MatchResponse)
def match_score(request: MatchRequest):
    resume_emb = model.encode([request.resume])
    job_emb = model.encode([request.job])

    skills = skills_match(request.resume, request.job)
    experience = experience_match_score(request.resume, request.job)
    keywords = keyword_match(request.resume, request.job)

    score = cosine_similarity(resume_emb, job_emb)[0][0]

    return {
        "similarity_score": round(float(score), 3),
        "match": score > 0.32,
        "skillsMatch": skills,
        "experienceMatch": experience,
        "keywordsMatch": keywords 
    }
