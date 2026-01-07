import pandas as pd

resumes = pd.read_csv("data/resumes.csv")
jobs = pd.read_csv("data/jobs.csv")

resumes = resumes.rename(columns={"Resume": "resume_text"})
jobs = jobs.rename(columns={"Description": "job_text"})

resumes.dropna(inplace=True)
jobs.dropna(inplace=True)

print(resumes.head())
print(jobs.head())