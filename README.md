# JobInsight

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Machine%20Learning-scikit--learn-F7931E?logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/License-Not%20specified-lightgrey" alt="License not specified">
</p>

JobInsight is an interactive job-market analytics and career exploration platform built with Python and Streamlit. It brings job listing analysis, skill demand insights, salary analytics, resume matching, and career exploration together in one dashboard.

The project combines data preparation, rule-based skill extraction, machine learning, text similarity, and interactive visualizations to help users explore job-market data.

---

## 1. Overview

JobInsight provides a workspace for exploring job postings and comparing candidate profiles with the skills and requirements found in those listings.

The platform includes:

- Job-market and listing analytics
- Job search, filtering, and listing details
- Skill extraction and demand analysis
- Skill demand trends and co-occurrence exploration
- Salary analysis and Random Forest salary estimates
- Resume text extraction and skill detection
- Resume-to-job and profile-to-job matching
- Skill gap analysis and career recommendations
- Company and location insights
- Interactive Streamlit dashboard

JobInsight is an analytics and career exploration project. Its results depend on the quality, completeness, and coverage of the supplied job data.

---

## 2. Key Features

### 2.1 Job Market Intelligence

Explore job listings across roles, employers, locations, industries, experience levels, employment types, and work models. Dashboard metrics and visualizations respond to the available data and selected filters.

### 2.2 Job Explorer

Search and filter job listings, review listing details, and explore opportunities using shared dashboard filters such as location, industry, experience, employer, and salary.

### 2.3 Skills Intelligence

JobInsight extracts skills from job text using a maintained vocabulary in `src/skill_extraction.py`. Explore skill frequencies, commonly requested skills, skill co-occurrence, and available demand trends.

### 2.4 Salary Intelligence

Analyze reported salary ranges by role, location, employment type, experience, and extracted skill. The dashboard can also use the saved Random Forest pipeline to estimate salary from supported job attributes.

Salary estimates are data-dependent and should be treated as estimates, not guarantees.

### 2.5 Resume Analyzer

Upload a PDF, DOCX, or TXT resume to extract its text and identify skills from the project's skill vocabulary. The analyzer can compare the candidate profile with filtered job listings and highlight frequently requested skills not detected in the resume.

Resume parsing extracts text; it does not structurally identify education, work history, certifications, or other resume sections.

### 2.6 Job Matching

Paste candidate profile or resume text to rank job listings using TF-IDF and cosine similarity. Similarity scores indicate text overlap and are not hiring probabilities or predictions of hiring outcomes.

### 2.7 Skill Gaps and Career Exploration

Compare candidate skills with skills appearing in the job data to explore potential gaps and related career recommendations.

### 2.8 Company and Location Intelligence

Explore job activity by employer and geography to understand where and by whom opportunities are being listed.

---

## 3. System Architecture

```text
Job Postings CSV
       |
       v
Data Cleaning
       |
       v
Cleaned Job Data
       |
       +-------------------------------+
       |                               |
       v                               v
Skill Extraction                 Salary Model Training
       |                               |
       v                               v
Jobs with Skills                 Saved Model Pipeline
       |                               |
       +---------------+---------------+
                       |
                       v
             Streamlit Dashboard
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
   Market Insights  Salary Analysis  Candidate Matching
                                      |
                                      v
                             Skill Gap Exploration
```

---

## 4. Repository Structure

```text
JobInsight/
├── app.py                       # Streamlit dashboard
├── requirements.txt             # Python dependencies
├── data/
│   ├── jobs.csv                 # Source dataset (not tracked)
│   ├── cleaned_jobs.csv         # Cleaned dataset (not tracked)
│   ├── jobs_with_skills.csv     # Processed dataset (not tracked)
│   └── skill_frequency.csv      # Skill counts (generated)
├── models/
│   └── salary_model.joblib      # Trained salary pipeline
└── src/
    ├── market_analytics.py      # Skill-frequency analysis
    ├── preprocess.py            # Job dataset cleaning
    ├── resume_matcher.py        # Profile-to-job similarity matching
    ├── resume_parser.py         # PDF, DOCX, and TXT text extraction
    ├── salary_model.py          # Salary model training and evaluation
    └── skill_extraction.py      # Job skill extraction
```

The data files are shown to explain the workflow; source and processed CSV datasets are excluded from version control by `.gitignore`.

---

## 5. Technical Stack

### Programming and Data

- Python
- pandas
- NumPy

### Machine Learning and Text Matching

- scikit-learn
- Random Forest Regression
- TF-IDF and cosine similarity

### Dashboard and Visualization

- Streamlit
- Plotly

### Document Processing and Model Storage

- PyPDF2
- python-docx
- joblib

---

## 6. Environment Setup

### 6.1 Open the Project

Clone your GitHub repository or download the project, then open a terminal in the project root (the directory containing `app.py` and `requirements.txt`).

### 6.2 Create a Virtual Environment

```bash
python -m venv .venv
```

### 6.3 Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 6.4 Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 7. Data Setup

Job datasets are not included in this repository. Add a job-postings CSV at `data/jobs.csv`. For best results, include `title` and `job_description`; fields such as `company_name`, `country`, `city`, `salary_min`, `salary_max`, and `date_posted` enable additional dashboard insights.

Run the data preparation scripts from the project root:

```bash
python src/preprocess.py
python src/skill_extraction.py
python src/market_analytics.py
```

The scripts create the cleaned job dataset, the dataset with extracted skills, and skill-frequency data. The available dashboard views depend on the columns present in your data.

### Train the Salary Model

To train or regenerate the salary prediction pipeline:

```bash
python src/salary_model.py
```

The training script reads `data/cleaned_jobs.csv` and saves the trained pipeline to `models/salary_model.joblib`. Suitable salary records and fields such as `salary_min`, `salary_max`, `title`, `country`, and `years_experience_numeric` are needed for model training.

---

## 8. Running Locally

Start the dashboard from the project root:

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser.

---

## 9. Dashboard Pages

The sidebar provides access to:

- Home
- Market Intelligence
- Job Explorer
- Skills Intelligence
- Skill Trends
- Salary Intelligence
- Resume Analyzer
- Job Matcher
- Skill Gap
- Career Recommendations
- Company Intelligence
- Location Intelligence

Some insights require particular fields or enough relevant data to be present in the input dataset.

---

## 10. Data, Model, and Privacy Notes

- Job data is not bundled with the repository. Provide a dataset you are authorized to use.
- Source and processed CSV files are excluded from version control. Avoid committing personal, confidential, or licensed data.
- Skill detection uses a maintained vocabulary and may not recognize every skill, synonym, or phrasing.
- Resume matching uses text similarity; it is not an assessment of candidate suitability or hiring probability.
- The resume analyzer extracts document text and does not perform structural resume parsing.
- Salary predictions depend on the training data and model features. They are estimates, not guarantees or professional compensation advice.
- If the app is deployed or shared, consider that uploaded resumes may be processed by the server hosting the app. Do not upload sensitive documents to an untrusted deployment.

---

## 11. Project Highlights

- End-to-end job-data preparation and dashboard workflow
- Interactive analytics built with Streamlit and Plotly
- Job skill extraction and demand analysis
- Random Forest salary prediction pipeline
- Resume parsing for PDF, DOCX, and TXT files
- TF-IDF-based candidate-to-job matching
- Career exploration through skill-gap, company, and location insights

---

## 12. Author

**Varadraj Bhandare**

M.Sc. Data Science & Big Data Analytics

Areas of interest:

- Data Analytics
- Data Science
- Machine Learning
- Natural Language Processing
- Job Market and Career Analytics
- Business Intelligence

---

## 13. License

No license is currently specified for this repository. Until a license is added, standard copyright restrictions apply.
