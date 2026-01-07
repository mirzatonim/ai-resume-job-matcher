import pandas as pd
import random

# Load datasets
resumes = pd.read_csv("data/resumes.csv")
jobs = pd.read_csv("data/jobs.csv")

# Rename columns
resumes = resumes.rename(columns={"Resume": "resume_text"})
jobs = jobs.rename(columns={"Description": "job_text", "Job Title": "job_title"})

# Drop nulls
resumes.dropna(inplace=True)
jobs.dropna(inplace=True)

# Lowercase for matching
resumes["Category"] = resumes["Category"].str.lower()
jobs["job_title"] = jobs["job_title"].str.lower()

pairs = []

# Create positive pairs
for _, resume in resumes.iterrows():
    matched_jobs = jobs[jobs["job_title"].str.contains(resume["Category"], na=False)]

    for _, job in matched_jobs.sample(min(2, len(matched_jobs))).iterrows():
        pairs.append({
            "resume_text": resume["resume_text"],
            "job_text": job["job_text"],
            "label": 1
        })

# Create negative pairs
for _, resume in resumes.iterrows():
    non_matched_jobs = jobs[~jobs["job_title"].str.contains(resume["Category"], na=False)]

    for _, job in non_matched_jobs.sample(2).iterrows():
        pairs.append({
            "resume_text": resume["resume_text"],
            "job_text": job["job_text"],
            "label": 0
        })

pairs_df = pd.DataFrame(pairs)

# Shuffle
pairs_df = pairs_df.sample(frac=1).reset_index(drop=True)

# Save
pairs_df.to_csv("data/pairs.csv", index=False)

print("Pairs generated:", pairs_df.shape)
print(pairs_df.head())
