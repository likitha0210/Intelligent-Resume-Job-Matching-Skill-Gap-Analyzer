from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import numpy as np
import docx2txt
import PyPDF2
import re
from sentence_transformers import SentenceTransformer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# --- Helper Functions ---

def extract_text(file: UploadFile) -> str:
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file.filename.endswith(".docx"):
        file.file.seek(0)
        return docx2txt.process(file.file)
    elif file.filename.endswith(".txt"):
        file.file.seek(0)
        return file.file.read().decode("utf-8")
    return ""

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    if vec1.ndim == 1:
        vec1 = vec1.reshape(1, -1)
    if vec2.ndim == 1:
        vec2 = vec2.reshape(1, -1)
    sim = np.dot(vec1, vec2.T) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return sim.item()

def extract_keywords(text: str):
    text = text.lower()
    skills_list = ["python", "sql", "pandas", "numpy", "ml", "deep learning",
        "nlp", "tensorflow", "pytorch", "scikit-learn", "data science", "ai",
        "aws", "azure", "docker", "kubernetes", "spark", "hadoop", "big data",
        "computer vision", "reinforcement learning", "etl", "power bi", "tableau"]
    found_skills = [skill for skill in skills_list if skill in text]
    return found_skills

def extract_experience(text: str):
    match = re.search(r"(\d+)\s+years?", text.lower())
    return int(match.group(1)) if match else 0

def candidate_score(candidate_text, jd_text, jd_vec, candidate_vec):
    similarity = cosine_similarity(candidate_vec, jd_vec)
    jd_keywords = extract_keywords(jd_text)
    candidate_keywords = extract_keywords(candidate_text)
    
    matched_skills = sum(1 for skill in jd_keywords if skill in candidate_keywords)
    skill_score = matched_skills / (len(jd_keywords) + 1e-5)
    
    jd_exp = extract_experience(jd_text)
    candidate_exp = extract_experience(candidate_text)
    experience_score = min(candidate_exp / (jd_exp + 1e-5), 1.0)
    
    total_score = 0.5 * similarity + 0.3 * skill_score + 0.2 * experience_score
    
    missing_skills = list(set(jd_keywords) - set(candidate_keywords))
    exp_gap = max(0, jd_exp - candidate_exp)
    
    return total_score, missing_skills, exp_gap

# --- Endpoints ---

@app.post("/rank_candidates")
async def rank_candidates(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    jd_vec = model.encode([job_description])[0]
    results = []

    for resume in resumes:
        text = extract_text(resume)
        if not text.strip():
            continue
        candidate_vec = model.encode([text])[0]
        score, missing_skills, exp_gap = candidate_score(text, job_description, jd_vec, candidate_vec)
        results.append({
            "candidate": resume.filename,
            "score": score,
            "missing_skills": missing_skills,
            "experience_gap_years": exp_gap
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return {"results": results}
