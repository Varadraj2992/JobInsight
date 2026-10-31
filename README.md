# 💼 JobInsight

## AI-Powered Job Market Analytics and Career Recommendation Platform

JobInsight is an AI/ML-based platform designed to analyze job-market data, identify in-demand skills, predict salaries, compare resumes with job requirements, and identify skill gaps.

The system provides an interactive dashboard using Streamlit.

---

# 🎯 Project Objective

The main objective of JobInsight is to help job seekers understand current job-market requirements and make data-driven career decisions.

The system analyzes job postings and provides:

- Job market analytics
- Skill demand analysis
- Salary prediction
- Resume-job matching
- Skill gap analysis
- Career insights

---

# 🚀 Main Features

## 1. 📊 Job Market Analytics

Analyzes the job dataset to identify:

- Total number of jobs
- Job roles
- Companies
- Job locations
- Average salary
- Salary patterns

---

## 2. 🧠 Skill Extraction and Analysis

The system extracts technical and professional skills from job descriptions.

Examples:

- Python
- SQL
- Machine Learning
- Power BI
- Excel
- AWS
- Azure
- Spark
- TensorFlow
- PyTorch

The system also calculates skill frequency to identify frequently demanded skills.

---

## 3. 💰 Salary Prediction

A Machine Learning model predicts estimated salary based on:

- Job title
- Location
- Experience

The project uses a Random Forest Regression model.

### Model Evaluation

The current model produced:

- MAE: 0.415
- RMSE: 0.498
- R²: 0.964

These results are based on the current dataset and train-test split.

---

## 4. 📄 Resume-Job Matching

Users can upload a resume in:

- PDF
- DOCX
- TXT

The system extracts resume text and compares it with job descriptions.

The matching process uses:

- TF-IDF
- Cosine Similarity

The system generates a match score and displays relevant jobs.

---

## 5. 🎯 Skill Gap Analysis

The system compares skills detected in the resume with skills demanded in the job dataset.

It identifies skills that may be missing from the resume.

Example:

Resume skills:

Python, SQL, Excel

Potential skill gaps:

Power BI, AWS, Machine Learning

---

# 🏗️ System Architecture

```text
Job Dataset
     │
     ▼
Data Preprocessing
     │
     ▼
Skill Extraction
     │
     ├───────────────┐
     ▼               ▼
Market Analytics   Skill Analysis
     │
     ▼
Salary Prediction
     │
     ▼
Resume Upload
     │
     ▼
Resume Parsing
     │
     ▼
Resume-Job Matching
     │
     ▼
Skill Gap Analysis
     │
     ▼
Streamlit Dashboard