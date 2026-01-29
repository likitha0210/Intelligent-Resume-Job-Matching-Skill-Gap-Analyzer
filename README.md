## Intelligent Resume–Job Matching & Skill Gap Analyzer

An AI-powered system that automatically matches resumes with a given Job Description (JD), ranks candidates based on relevance, and identifies missing skills and experience gaps. This project helps recruiters shortlist candidates faster and helps applicants understand what they need to improve to qualify for a role.

## Project Overview

The Intelligent Resume–Job Matching & Skill Gap Analyzer takes a Job Description and multiple resumes as input and evaluates how well each candidate matches the role. Instead of relying only on keyword matching, it combines **semantic similarity**, **skill overlap**, and **experience matching** to produce a final score for each candidate.
The system also provides actionable feedback by highlighting **missing skills** and **experience gaps**, making it useful for both recruiters and job seekers.

## How It Works

1. **Resume & JD Ingestion**
   Supports PDF, DOCX, and TXT resumes
   Job Description is provided as plain text

2. **Text Understanding**
   Uses Sentence Transformers to generate embeddings
   Calculates semantic similarity between JD and resumes

3. **Skill Matching**
   Extracts skills from both JD and resumes
   Identifies missing JD-required skills in each resume

4. **Experience Matching**
   Extracts years of experience using pattern matching
   Computes experience gap if JD requirements are not met

5. **Final Scoring**
   Weighted score based on:
   Semantic similarity
   Skill match percentage
   Experience match

## Tech Stack

**Backend:** FastAPI
**Frontend:** Streamlit
**NLP Model:** Sentence-Transformers (all-MiniLM-L6-v2)
**Libraries:** NumPy, PyPDF2, docx2txt, Regex
**Language:** Python

## Features

- Upload multiple resumes at once
- Rank candidates automatically
- Identify missing skills per candidate
- Detect experience gaps
- Recruiter-friendly and applicant-friendly insights

## How to Run

## Backend
```bash
uvicorn main:app --reload
