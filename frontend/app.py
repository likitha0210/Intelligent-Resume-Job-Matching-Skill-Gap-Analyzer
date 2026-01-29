import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("AI Candidate Matcher")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf","docx","txt"], accept_multiple_files=True)
jd = st.text_area("Paste Job Description")

if st.button("Rank Candidates"):
    if uploaded_files and jd.strip():
        files = [("resumes", (file.name, file, "application/octet-stream")) for file in uploaded_files]
        response = requests.post(BACKEND_URL + "/rank_candidates", data={"job_description": jd}, files=files)
        if response.status_code == 200:
            results = response.json()["results"]
            for r in results:
                st.write(f"**{r['candidate']}** — Score: {r['score']:.2f}")
                st.write(f"Missing Skills: {r['missing_skills']}")
                st.write(f"Experience Gap: {r['experience_gap_years']} years")
