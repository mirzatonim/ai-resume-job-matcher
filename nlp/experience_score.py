import re

def extract_years(text):
    matches = re.findall(r'(\d+)\+?\s*(years|yrs)', text.lower())
    years = [int(m[0]) for m in matches]
    return max(years) if years else 0


def experience_match_score(resume_text, job_text):
    resume_years = extract_years(resume_text)
    job_years = extract_years(job_text)

    if job_years == 0:
        return 50.0

    return round(min(resume_years / job_years, 1.0) * 100, 2)
