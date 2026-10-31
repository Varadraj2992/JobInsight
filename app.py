import ast
import html
import re
import streamlit as st
import pandas as pd
import os
import joblib
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="JobInsight",
    page_icon="JI",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ink: #18332d;
    --muted: #687b75;
    --paper: #f3f7f4;
    --surface: #ffffff;
    --line: #dce7e1;
    --green: #176b59;
    --green-dark: #102e28;
    --sidebar: #142a3b;
    --mint: #d8eee4;
    --orange: #d66a43;
    --orange-pale: #fae7dc;
    --blue: #4c7e94;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
    letter-spacing: 0;
}

.stApp {
    background-color: var(--paper);
    background-image: linear-gradient(rgba(23, 107, 89, .025) 1px, transparent 1px), linear-gradient(90deg, rgba(23, 107, 89, .025) 1px, transparent 1px);
    background-size: 28px 28px;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { right: 1rem; }
[data-testid="stAppViewContainer"] > .main .block-container {
    max-width: 1480px;
    padding: 2.1rem 3.1rem 2.5rem;
}

h1, h2, h3, [data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: 0 !important;
    color: var(--ink) !important;
}

[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color: #e8f2ed; }
[data-testid="stSidebar"] section { padding-top: 1.2rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: #9fb7ad;
    font-family: 'DM Mono', monospace;
    font-size: .68rem;
    letter-spacing: 0;
    text-transform: uppercase;
}
[data-testid="stSidebar"] [role="radiogroup"] { gap: .35rem; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    border: 1px solid transparent;
    border-radius: 5px;
    padding: .58rem .7rem;
    transition: background .2s ease, border-color .2s ease, transform .2s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255,255,255,.07);
    transform: translateX(2px);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: rgba(216,238,228,.12);
    border-color: rgba(216,238,228,.2);
    box-shadow: inset 3px 0 var(--mint);
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: .75rem;
    padding: .8rem .4rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,.12);
    margin-bottom: 1.1rem;
}
.brand-stamp {
    display: grid;
    place-items: center;
    width: 39px;
    height: 39px;
    border-radius: 5px;
    background: var(--mint);
    color: var(--sidebar) !important;
    font: 800 .9rem 'Manrope', sans-serif;
}
.brand-name { color: #f5faf7; font: 800 1.05rem 'Manrope', sans-serif; }
.sidebar-footnote {
    margin-top: 2rem;
    padding: .8rem .4rem;
    border-top: 1px solid rgba(255,255,255,.12);
    color: #9fb7ad;
    font: .68rem 'DM Mono', monospace;
    line-height: 1.65;
}

.page-heading {
    padding: .25rem 0 1.45rem;
    animation: rise-in .45s ease both;
}
.page-kicker {
    color: var(--orange);
    font: 500 .68rem 'DM Mono', monospace;
    letter-spacing: 0;
    text-transform: uppercase;
    margin-bottom: .38rem;
}
.page-title {
    color: var(--ink);
    font: 800 clamp(1.7rem, 2.2rem, 2.2rem) 'Manrope', sans-serif;
    line-height: 1.15;
}
.page-subtitle { color: var(--muted); font-size: .93rem; margin-top: .45rem; }
.section-label {
    color: var(--muted);
    font: 500 .68rem 'DM Mono', monospace;
    letter-spacing: 0;
    text-transform: uppercase;
}

[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 3px solid var(--green);
    border-radius: 5px;
    padding: 1rem 1.15rem;
    animation: rise-in .5s ease both;
    transition: transform .2s ease, box-shadow .2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 22px rgba(24,51,45,.08);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: .78rem; }
[data-testid="stMetricValue"] { font-size: 1.65rem; }
[data-testid="stMetricDelta"] { font-family: 'DM Mono', monospace; }

.stButton > button, [data-testid="stFormSubmitButton"] button {
    border: 1px solid var(--green) !important;
    border-radius: 4px !important;
    background: var(--green) !important;
    color: white !important;
    font-weight: 700 !important;
    transition: background .2s ease, transform .2s ease, box-shadow .2s ease !important;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
    background: var(--green-dark) !important;
    transform: translateY(-1px);
    box-shadow: 0 5px 12px rgba(16,46,40,.18);
}
.stTextInput input, .stNumberInput input, [data-baseweb="select"] > div {
    border-radius: 4px !important;
    border-color: var(--line) !important;
    background: #fff !important;
}
[data-testid="stFileUploader"] section {
    border: 1px dashed #9ebbb0;
    border-radius: 5px;
    background: rgba(255,255,255,.72);
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 5px;
    overflow: hidden;
}
[data-testid="stAlert"] { border-radius: 4px; }
.skill-tags { display: flex; flex-wrap: wrap; gap: .5rem; margin: .4rem 0 1rem; }
.skill-tag {
    display: inline-block;
    border: 1px solid #b9d9cc;
    border-radius: 3px;
    background: #e7f3ed;
    color: #1d5e4d;
    padding: .32rem .58rem;
    font-size: .78rem;
    font-weight: 600;
}
.empty-state {
    border: 1px dashed #b9cec4;
    border-radius: 5px;
    padding: 2rem;
    color: var(--muted);
    background: rgba(255,255,255,.65);
    text-align: center;
}
.page-footer {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid var(--line);
    margin-top: 2rem;
    padding-top: .8rem;
    color: var(--muted);
    font: .65rem 'DM Mono', monospace;
    text-transform: uppercase;
}

@keyframes rise-in {
    from { opacity: 0; transform: translateY(9px); }
    to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
@media (max-width: 760px) {
    [data-testid="stAppViewContainer"] > .main .block-container { padding: 1.2rem 1rem 1.8rem; }
    .page-title { font-size: 1.65rem; }
    .page-footer { flex-direction: column; gap: .3rem; }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# IMPORT PROJECT MODULES
# --------------------------------------------------

from src.resume_parser import read_resume
from src.skill_extraction import extract_skills
from src.resume_matcher import match_resume_to_jobs


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOBS_FILE = os.path.join(
    BASE_DIR, "data", "jobs_with_skills.csv"
)

SKILLS_FILE = os.path.join(
    BASE_DIR, "data", "skill_frequency.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR, "models", "salary_model.joblib"
)

JOB_DATA_COLUMNS = {
    "title",
    "company_name",
    "country",
    "city",
    "location_resolved",
    "latitude",
    "longitude",
    "industry",
    "function",
    "occupational_category",
    "employment_type",
    "work_model",
    "experience_level",
    "years_experience_numeric",
    "date_posted",
    "salary_min",
    "salary_max",
    "salary_currency",
    "salary_rate_unit",
    "extracted_skills",
    "skill_count"
}


def normalize_pay_period(values):
    return (
        values
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "hourly": "hour",
            "per hour": "hour",
            "per annum": "year",
            "annum": "year",
            "yearly": "year",
            "annual": "year",
            "annually": "year",
            "per year": "year",
            "annuelle": "year",
            "p.a.": "year",
            "monthly": "month",
            "per month": "month",
            "weekly": "week",
            "per week": "week",
            "daily": "day",
            "per day": "day"
        })
        .where(lambda series: series.isin(["hour", "day", "week", "month", "year"]), "Unknown")
    )


# --------------------------------------------------
# LOAD JOB DATA
# --------------------------------------------------

@st.cache_data
def load_jobs():

    if os.path.exists(JOBS_FILE):
        jobs = pd.read_csv(
            JOBS_FILE,
            usecols=lambda column: column in JOB_DATA_COLUMNS,
            low_memory=False
        )
        if "salary_rate_unit" in jobs.columns:
            jobs["salary_rate_unit"] = normalize_pay_period(jobs["salary_rate_unit"])
        return jobs

    return pd.DataFrame()


@st.cache_data
def load_skill_frequency():

    if (
        os.path.exists(SKILLS_FILE)
        and os.path.exists(JOBS_FILE)
        and os.path.getmtime(SKILLS_FILE) >= os.path.getmtime(JOBS_FILE)
    ):
        return pd.read_csv(SKILLS_FILE)

    if not os.path.exists(JOBS_FILE):
        return pd.DataFrame(columns=["skill", "frequency"])

    skills = []
    skill_data = pd.read_csv(
        JOBS_FILE,
        usecols=["extracted_skills"],
        low_memory=False
    )

    for value in skill_data["extracted_skills"].dropna():
        try:
            parsed_skills = ast.literal_eval(str(value))
        except (ValueError, SyntaxError):
            continue

        if isinstance(parsed_skills, list):
            skills.extend(
                str(skill).strip()
                for skill in parsed_skills
                if str(skill).strip()
            )

    skill_frequency = (
        pd.Series(skills, dtype="string")
        .value_counts()
        .rename_axis("skill")
        .reset_index(name="frequency")
    )
    skill_frequency.to_csv(SKILLS_FILE, index=False)
    return skill_frequency


@st.cache_data
def load_job_texts():
    if not os.path.exists(JOBS_FILE):
        return pd.Series(dtype="string")

    return pd.read_csv(
        JOBS_FILE,
        usecols=["job_text"],
        low_memory=False
    )["job_text"]


def add_matching_text(candidate_jobs):
    matching_jobs = candidate_jobs.copy()
    matching_jobs["job_text"] = load_job_texts().reindex(matching_jobs.index).fillna("")
    return matching_jobs


@st.cache_resource
def load_salary_model():

    if os.path.exists(MODEL_FILE):
        try:
            return joblib.load(MODEL_FILE)
        except Exception:
            return None

    return None


jobs_df = load_jobs()
skill_df = load_skill_frequency()
salary_model = load_salary_model()


def filter_job_rows(data, search, location, industry, experience, employment, company, salary_filter, currency, period, salary_range, date_range=None):
    filtered = data

    selectors = [
        ("industry", industry),
        ("experience_level", experience),
        ("employment_type", employment)
    ]
    for column, selection in selectors:
        if selection != "All" and column in filtered:
            filtered = filtered[filtered[column].fillna("").astype(str) == selection]

    if location.strip():
        location_mask = pd.Series(False, index=filtered.index)
        for column in ["country", "city", "location_resolved"]:
            if column in filtered:
                location_mask |= filtered[column].fillna("").astype(str).str.contains(
                    re.escape(location.strip()), case=False, regex=True
                )
        filtered = filtered[location_mask]

    if company.strip() and "company_name" in filtered:
        filtered = filtered[
            filtered["company_name"].fillna("").astype(str).str.contains(
                re.escape(company.strip()), case=False, regex=True
            )
        ]

    if search.strip():
        searchable_columns = [
            column for column in ["title", "company_name", "country", "city", "extracted_skills"]
            if column in filtered
        ]
        for token in re.findall(r"[\w+#.]+", search.casefold()):
            if token in {"job", "jobs", "in", "at", "for", "with", "near", "and"}:
                continue
            token_mask = pd.Series(False, index=filtered.index)
            for column in searchable_columns:
                token_mask |= filtered[column].fillna("").astype(str).str.contains(
                    re.escape(token), case=False, regex=True
                )
            filtered = filtered[token_mask]

    if salary_filter and salary_range and {"salary_min", "salary_max", "salary_currency", "salary_rate_unit"}.issubset(filtered.columns):
        salary_min = pd.to_numeric(filtered["salary_min"], errors="coerce")
        salary_max = pd.to_numeric(filtered["salary_max"], errors="coerce")
        midpoint = pd.concat([salary_min, salary_max], axis=1).mean(axis=1)
        salary_mask = (
            (filtered["salary_currency"].fillna("Unknown").astype(str).str.upper() == currency)
            & (filtered["salary_rate_unit"] == period)
            & midpoint.between(salary_range[0], salary_range[1])
        )
        filtered = filtered[salary_mask]

    if date_range and "date_posted" in filtered:
        posted = pd.to_datetime(filtered["date_posted"], errors="coerce", format="mixed")
        start_date = pd.Timestamp(date_range[0])
        end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
        filtered = filtered[posted.between(start_date, end_date)]

    return filtered


@st.cache_data
def filtered_skill_frequency(search, location, industry, experience, employment, company, salary_filter, currency, period, salary_range, date_range=None):
    filtered = filter_job_rows(
        load_jobs(), search, location, industry, experience, employment, company,
        salary_filter, currency, period, salary_range, date_range
    )
    if filtered.empty or "extracted_skills" not in filtered:
        return pd.DataFrame(columns=["skill", "frequency"])

    counts = {}
    for value in filtered["extracted_skills"].dropna():
        try:
            parsed = ast.literal_eval(str(value))
        except (ValueError, SyntaxError):
            continue
        if isinstance(parsed, list):
            for skill in parsed:
                skill = str(skill).strip()
                if skill:
                    counts[skill] = counts.get(skill, 0) + 1

    return (
        pd.Series(counts, dtype="int64", name="frequency")
        .rename_axis("skill")
        .reset_index()
        .sort_values("frequency", ascending=False)
    )


@st.cache_data
def skill_trend_summary(skill, search, location, industry, experience, employment, company, salary_filter, currency, period, salary_range, date_range=None):
    filtered = filter_job_rows(
        load_jobs(), search, location, industry, experience, employment, company,
        salary_filter, currency, period, salary_range, date_range
    )
    if filtered.empty or "extracted_skills" not in filtered:
        return {
            "jobs": 0,
            "dated_jobs": 0,
            "trend": pd.DataFrame(columns=["Month", "Listings"]),
            "roles": pd.DataFrame(columns=["Role", "Listings"]),
            "locations": pd.DataFrame(columns=["Location", "Listings"]),
            "salary_median": None
        }

    matching_indexes = []
    for index, value in filtered["extracted_skills"].items():
        try:
            parsed = ast.literal_eval(str(value))
        except (ValueError, SyntaxError):
            continue
        if isinstance(parsed, list) and skill.casefold() in {str(item).casefold() for item in parsed}:
            matching_indexes.append(index)

    matches = filtered.loc[matching_indexes]
    trend = pd.DataFrame(columns=["Month", "Listings"])
    dated_jobs = 0
    if "date_posted" in matches:
        dates = pd.to_datetime(matches["date_posted"], errors="coerce", format="mixed")
        dated = dates.dropna()
        dated_jobs = len(dated)
        if not dated.empty:
            monthly = dated.dt.to_period("M").value_counts().sort_index()
            trend = pd.DataFrame({"Month": monthly.index.to_timestamp(), "Listings": monthly.values})

    role_column = "title" if "title" in matches else None
    roles = (
        matches[role_column].replace("", pd.NA).dropna().astype(str).value_counts().head(8)
        .rename_axis("Role").reset_index(name="Listings")
        if role_column
        else pd.DataFrame(columns=["Role", "Listings"])
    )
    location_column = "city" if "city" in matches else "country" if "country" in matches else None
    locations = (
        matches[location_column].replace("", pd.NA).dropna().astype(str).value_counts().head(8)
        .rename_axis("Location").reset_index(name="Listings")
        if location_column
        else pd.DataFrame(columns=["Location", "Listings"])
    )

    salary_median = None
    salary_fields = {"salary_min", "salary_max", "salary_currency", "salary_rate_unit"}
    if salary_fields.issubset(matches.columns):
        matching_salary = matches[
            (matches["salary_currency"].fillna("").astype(str).str.upper() == currency)
            & (matches["salary_rate_unit"] == period)
        ]
        midpoint = pd.concat([
            pd.to_numeric(matching_salary["salary_min"], errors="coerce"),
            pd.to_numeric(matching_salary["salary_max"], errors="coerce")
        ], axis=1).mean(axis=1)
        midpoint = midpoint[midpoint > 0]
        if not midpoint.empty:
            salary_median = float(midpoint.median())

    return {
        "jobs": len(matches),
        "dated_jobs": dated_jobs,
        "trend": trend,
        "roles": roles,
        "locations": locations,
        "salary_median": salary_median
    }


@st.cache_data
def skill_cooccurrence_matrix(skills, search, location, industry, experience, employment, company, salary_filter, currency, period, salary_range, date_range=None):
    skill_names = list(skills)
    positions = {skill.casefold(): index for index, skill in enumerate(skill_names)}
    matrix = [[0 for _ in skill_names] for _ in skill_names]
    filtered = filter_job_rows(
        load_jobs(), search, location, industry, experience, employment, company,
        salary_filter, currency, period, salary_range, date_range
    )

    for value in filtered.get("extracted_skills", pd.Series(dtype="string")).dropna():
        try:
            parsed = ast.literal_eval(str(value))
        except (ValueError, SyntaxError):
            continue
        if not isinstance(parsed, list):
            continue
        present = sorted({
            positions[str(skill).casefold()]
            for skill in parsed
            if str(skill).casefold() in positions
        })
        for left_index, first in enumerate(present):
            matrix[first][first] += 1
            for second in present[left_index + 1:]:
                matrix[first][second] += 1
                matrix[second][first] += 1

    return pd.DataFrame(matrix, index=skill_names, columns=skill_names)


def render_heading(kicker, title, subtitle):
    st.markdown(
        f'<div class="page-heading"><div class="page-kicker">{html.escape(kicker)}</div>'
        f'<div class="page-title">{html.escape(title)}</div>'
        f'<div class="page-subtitle">{html.escape(subtitle)}</div></div>',
        unsafe_allow_html=True
    )


def style_chart(figure, height=360):
    figure.update_layout(
        height=height,
        margin=dict(l=8, r=16, t=12, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#52665f", size=12),
        showlegend=False,
        transition=dict(duration=550, easing="cubic-in-out"),
        xaxis=dict(showgrid=True, gridcolor="#e8efeb", zeroline=False, title=None),
        yaxis=dict(showgrid=False, title=None)
    )
    return figure


def profile_candidate_jobs(profile_text, limit=10000):
    if len(active_jobs) <= limit:
        return active_jobs, False

    profile_skills = extract_skills(profile_text)
    if "extracted_skills" not in active_jobs.columns or not profile_skills:
        return active_jobs.sample(n=limit, random_state=42), True

    skill_text = active_jobs["extracted_skills"].fillna("").astype(str)
    overlap = pd.Series(0, index=active_jobs.index, dtype="int16")
    for skill in profile_skills:
        overlap += skill_text.str.contains(
            re.escape(skill),
            case=False,
            regex=True,
            na=False
        ).astype("int16")

    candidate_indexes = overlap[overlap > 0].index
    if len(candidate_indexes) == 0:
        return active_jobs.sample(n=limit, random_state=42), True

    candidates = active_jobs.loc[candidate_indexes]
    if len(candidates) > limit:
        candidates = (
            candidates
            .sample(frac=1, random_state=42)
            .assign(_skill_overlap=overlap.loc[candidate_indexes])
            .sort_values("_skill_overlap", ascending=False)
            .head(limit)
            .drop(columns="_skill_overlap")
        )

    return candidates, True


# --------------------------------------------------
# SIDEBAR AND NAVIGATION
# --------------------------------------------------

st.sidebar.markdown(
    '<div class="sidebar-brand"><div class="brand-stamp">JI</div>'
    '<div class="brand-name">JobInsight</div></div>',
    unsafe_allow_html=True
)

if st.sidebar.button("Refresh data", key="refresh_dataset"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

page = st.sidebar.radio(
    "Workspace",
    [
        "🏠 Home",
        "📊 Market Intelligence",
        "💼 Job Explorer",
        "🧠 Skills Intelligence",
        "📈 Skill Trends",
        "💰 Salary Intelligence",
        "📄 Resume Analyzer",
        "🎯 Job Matcher",
        "🧩 Skill Gap",
        "🚀 Career Recommendations",
        "🏢 Company Intelligence",
        "🗺️ Location Intelligence"
    ]
)

filter_widget_keys = [
    "global_search",
    "global_location",
    "global_industry",
    "global_experience",
    "global_employment",
    "global_company",
    "global_currency",
    "global_period",
    "global_salary_enabled",
    "global_posting_dates"
]
if st.sidebar.button("Reset filters", key="reset_global_filters"):
    for widget_key in filter_widget_keys:
        st.session_state.pop(widget_key, None)
    st.rerun()

industries = ["All"]
if "industry" in jobs_df:
    industries.extend(
        jobs_df["industry"].replace("", pd.NA).dropna().astype(str)
        .value_counts().head(60).index.tolist()
    )
experience_levels = ["All"]
if "experience_level" in jobs_df:
    experience_levels.extend(sorted(value for value in jobs_df["experience_level"].dropna().astype(str).unique() if value.strip()))
employment_types = ["All"]
if "employment_type" in jobs_df:
    employment_types.extend(sorted(value for value in jobs_df["employment_type"].dropna().astype(str).unique() if value.strip()))
currencies = ["USD"]
if "salary_currency" in jobs_df:
    currencies = sorted(jobs_df["salary_currency"].dropna().astype(str).str.upper().unique())
periods = ["year"]
if "salary_rate_unit" in jobs_df:
    periods = sorted(jobs_df["salary_rate_unit"].dropna().astype(str).unique())
date_values = pd.Series(dtype="datetime64[ns]")
if "date_posted" in jobs_df:
    date_values = pd.to_datetime(jobs_df["date_posted"], errors="coerce", format="mixed").dropna()
default_posting_dates = (
    (date_values.min().date(), date_values.max().date())
    if not date_values.empty
    else None
)

with st.sidebar.expander("Global filters", expanded=False):
    with st.form("global_filter_form"):
        st.text_input(
            "Search jobs",
            key="global_search",
            placeholder="Python jobs in Pune"
        )
        location_filter = st.text_input("Location", key="global_location", placeholder="City or country")
        industry_filter = st.selectbox("Job category / industry", industries, key="global_industry")
        experience_filter = st.selectbox("Experience level", experience_levels, key="global_experience")
        employment_filter = st.selectbox("Employment type", employment_types, key="global_employment")
        company_filter = st.text_input("Company", key="global_company", placeholder="Any employer")
        currency_filter = st.selectbox(
            "Salary currency",
            currencies,
            index=currencies.index("USD") if "USD" in currencies else 0,
            key="global_currency"
        )
        period_filter = st.selectbox(
            "Salary pay period",
            periods,
            index=periods.index("year") if "year" in periods else 0,
            key="global_period"
        )
        salary_filter_enabled = st.checkbox("Filter by salary range", key="global_salary_enabled")
        salary_range_filter = None
        if salary_filter_enabled and {"salary_min", "salary_max", "salary_currency", "salary_rate_unit"}.issubset(jobs_df.columns):
            salary_min_values = pd.to_numeric(jobs_df["salary_min"], errors="coerce")
            salary_max_values = pd.to_numeric(jobs_df["salary_max"], errors="coerce")
            salary_midpoints = pd.concat([salary_min_values, salary_max_values], axis=1).mean(axis=1)
            basis_mask = (
                (jobs_df["salary_currency"].fillna("").astype(str).str.upper() == currency_filter)
                & (jobs_df["salary_rate_unit"] == period_filter)
                & salary_midpoints.gt(0)
            )
            basis_values = salary_midpoints[basis_mask].dropna()
            if not basis_values.empty:
                range_min = float(basis_values.min())
                range_max = float(basis_values.quantile(.99))
                if range_max <= range_min:
                    range_max = range_min + 1
                salary_range_filter = st.slider(
                    f"Salary range ({currency_filter} / {period_filter})",
                    min_value=range_min,
                    max_value=range_max,
                    value=(range_min, range_max),
                    key=f"global_salary_range_{currency_filter}_{period_filter}"
                )
            else:
                st.caption("Salary range unavailable for this currency and pay period.")
        if default_posting_dates:
            selected_posting_dates = st.date_input(
                "Posting date range",
                value=default_posting_dates,
                min_value=default_posting_dates[0],
                max_value=default_posting_dates[1],
                key="global_posting_dates"
            )
            st.caption("Date filtering excludes undated listings only when the range is narrowed.")
        st.form_submit_button("Apply filters", type="primary", width="stretch")

global_search = st.session_state.get("global_search", "")
location_filter = st.session_state.get("global_location", "")
industry_filter = st.session_state.get("global_industry", "All")
experience_filter = st.session_state.get("global_experience", "All")
employment_filter = st.session_state.get("global_employment", "All")
company_filter = st.session_state.get("global_company", "")
currency_filter = st.session_state.get("global_currency", "USD")
period_filter = st.session_state.get("global_period", "year")
salary_filter_enabled = st.session_state.get("global_salary_enabled", False)
selected_posting_dates = st.session_state.get("global_posting_dates", default_posting_dates)
date_filter_range = (
    tuple(selected_posting_dates)
    if isinstance(selected_posting_dates, (tuple, list))
    and len(selected_posting_dates) == 2
    and tuple(selected_posting_dates) != default_posting_dates
    else None
)
salary_range_filter = st.session_state.get(
    f"global_salary_range_{currency_filter}_{period_filter}"
) if salary_filter_enabled else None

active_jobs = filter_job_rows(
    jobs_df,
    global_search,
    location_filter,
    industry_filter,
    experience_filter,
    employment_filter,
    company_filter,
    salary_filter_enabled,
    currency_filter,
    period_filter,
    salary_range_filter,
    date_filter_range
)
filters_active = any([
    global_search.strip(),
    location_filter.strip(),
    industry_filter != "All",
    experience_filter != "All",
    employment_filter != "All",
    company_filter.strip(),
    salary_filter_enabled,
    date_filter_range is not None
])
active_skill_df = (
    filtered_skill_frequency(
        global_search,
        location_filter,
        industry_filter,
        experience_filter,
        employment_filter,
        company_filter,
        salary_filter_enabled,
        currency_filter,
        period_filter,
        tuple(salary_range_filter) if salary_range_filter else None,
        date_filter_range
    )
    if filters_active
    else skill_df
)

date_updated = "Unavailable"
if "date_posted" in jobs_df:
    posted_dates = pd.to_datetime(jobs_df["date_posted"], errors="coerce", format="mixed")
    if posted_dates.notna().any():
        date_updated = posted_dates.max().strftime("%Y-%m-%d")

st.sidebar.markdown(
    '<div class="sidebar-footnote">LATEST POSTING: '
    f'{html.escape(date_updated)}<br>DATASET: '
    f'{html.escape(os.path.basename(JOBS_FILE))}<br>RECORDS: {len(active_jobs):,} / {len(jobs_df):,}<br>'
    f'SKILLS: {len(active_skill_df):,}</div>',
    unsafe_allow_html=True
)


# ==================================================
# DASHBOARD
# ==================================================

if page == "🏠 Home":

    render_heading(
        "Market overview",
        "Hiring pulse",
        "A snapshot of roles, employers, and skills across the supplied job market dataset."
    )

    company_count = active_jobs["company_name"].nunique() if "company_name" in active_jobs else None
    location_count = active_jobs["city"].nunique() if "city" in active_jobs else None
    salary_metrics = active_jobs
    if {"salary_min", "salary_max", "salary_currency", "salary_rate_unit"}.issubset(active_jobs.columns):
        salary_metrics = active_jobs[
            (active_jobs["salary_currency"].fillna("").astype(str).str.upper() == "USD")
            & (active_jobs["salary_rate_unit"] == "year")
        ].copy()
        salary_metrics["salary_midpoint"] = pd.concat([
            pd.to_numeric(salary_metrics["salary_min"], errors="coerce"),
            pd.to_numeric(salary_metrics["salary_max"], errors="coerce")
        ], axis=1).mean(axis=1)
        salary_metrics = salary_metrics[salary_metrics["salary_midpoint"] > 0]
    else:
        salary_metrics = pd.DataFrame()

    known_work_models = active_jobs["work_model"].fillna("").astype(str) if "work_model" in active_jobs else pd.Series(dtype="string")
    remote_share = (
        f"{known_work_models.str.contains('remote', case=False, na=False).sum() / known_work_models.ne('').sum() * 100:.1f}%"
        if known_work_models.ne("").any()
        else "Data unavailable"
    )
    dated_postings = int(
        pd.to_datetime(active_jobs["date_posted"], errors="coerce", format="mixed").notna().sum()
    ) if "date_posted" in active_jobs else None

    kpi_values = [
        ("Job listings", f"{len(active_jobs):,}"),
        ("Unique employers", f"{company_count:,}" if company_count is not None else "Data unavailable"),
        ("Unique cities", f"{location_count:,}" if location_count is not None else "Data unavailable"),
        ("Tracked skills", f"{len(active_skill_df):,}"),
        ("Average salary - USD/year", f"{salary_metrics['salary_midpoint'].mean():,.0f}" if not salary_metrics.empty else "Data unavailable"),
        ("Median salary - USD/year", f"{salary_metrics['salary_midpoint'].median():,.0f}" if not salary_metrics.empty else "Data unavailable"),
        ("Listings with posting dates", f"{dated_postings:,}" if dated_postings is not None else "Data unavailable"),
        ("Remote share of known models", remote_share)
    ]
    for offset in (0, 4):
        kpi_columns = st.columns(4)
        for column, (label, value) in zip(kpi_columns, kpi_values[offset:offset + 4]):
            with column:
                st.metric(label, value)

    st.markdown('<div class="section-label">Demand by category</div>', unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2, gap="large")

    title_column = "title" if "title" in jobs_df else "job_title"
    if not active_jobs.empty and title_column in active_jobs:
        with chart_col1:
            st.subheader("Most-listed roles")
            role_counts = (
                active_jobs[title_column]
                .dropna()
                .astype(str)
                .value_counts()
                .head(10)
                .rename_axis("Role")
                .reset_index(name="Listings")
            )
            role_figure = px.bar(
                role_counts,
                x="Listings",
                y="Role",
                orientation="h",
                color_discrete_sequence=["#176b59"]
            )
            role_figure.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(style_chart(role_figure, 390), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

    if not active_skill_df.empty:
        skill_col = next((col for col in active_skill_df if "skill" in col.lower()), None)
        count_col = next((col for col in active_skill_df if any(word in col.lower() for word in ["frequency", "count", "demand"])), None)
        if skill_col and count_col:
            with chart_col2:
                st.subheader("Most-requested skills")
                top_skills = active_skill_df.nlargest(10, count_col).sort_values(count_col)
                skill_figure = px.bar(
                    top_skills,
                    x=count_col,
                    y=skill_col,
                    orientation="h",
                    color_discrete_sequence=["#d66a43"]
                )
                skill_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(style_chart(skill_figure, 390), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

# ==================================================
# MARKET INTELLIGENCE
# ==================================================

elif page == "📊 Market Intelligence":

    render_heading(
        "Market signals",
        "Market intelligence",
        "Understand where hiring is concentrated and how employers describe work."
    )

    if active_jobs.empty:
        st.warning("The job dataset is unavailable.")
    else:
        country_column = "country" if "country" in active_jobs else None
        industry_column = "industry" if "industry" in active_jobs else None
        work_column = "work_model" if "work_model" in active_jobs else None
        metric_columns = st.columns(3)

        with metric_columns[0]:
            st.metric("Job records", f"{len(active_jobs):,}")
        with metric_columns[1]:
            st.metric("Employers", f"{active_jobs['company_name'].nunique():,}" if "company_name" in active_jobs else "N/A")
        with metric_columns[2]:
            st.metric("Skill signals", f"{len(active_skill_df):,}")

        chart_col1, chart_col2 = st.columns(2, gap="large")
        if country_column:
            with chart_col1:
                st.subheader("Listings by location")
                location_counts = (
                    active_jobs[country_column]
                    .dropna()
                    .astype(str)
                    .value_counts()
                    .head(12)
                    .rename_axis("Location")
                    .reset_index(name="Listings")
                    .sort_values("Listings")
                )
                location_figure = px.bar(
                    location_counts,
                    x="Listings",
                    y="Location",
                    orientation="h",
                    color_discrete_sequence=["#4c7e94"]
                )
                location_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(style_chart(location_figure, 420), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

        if work_column:
            with chart_col2:
                st.subheader("Work model mix")
                work_counts = (
                    active_jobs[work_column]
                    .replace("", pd.NA)
                    .dropna()
                    .astype(str)
                    .str.title()
                    .value_counts()
                    .rename_axis("Work model")
                    .reset_index(name="Listings")
                )
                work_figure = px.pie(
                    work_counts,
                    names="Work model",
                    values="Listings",
                    hole=.58,
                    color_discrete_sequence=["#176b59", "#d66a43", "#4c7e94", "#c9d8cf"]
                )
                work_figure.update_layout(
                    height=420,
                    margin=dict(l=8, r=16, t=12, b=8),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans, sans-serif", color="#52665f", size=12),
                    transition=dict(duration=550, easing="cubic-in-out")
                )
                st.plotly_chart(work_figure, width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

        if industry_column:
            st.subheader("Industry concentration")
            industry_counts = (
                active_jobs[industry_column]
                .replace("", pd.NA)
                .dropna()
                .astype(str)
                .value_counts()
                .head(12)
                .rename_axis("Industry")
                .reset_index(name="Listings")
            )
            st.dataframe(industry_counts, width="stretch", hide_index=True)

        if "company_name" in active_jobs:
            st.subheader("Top hiring companies")
            employer_counts = (
                active_jobs["company_name"].replace("", pd.NA).dropna().astype(str)
                .value_counts().head(12).sort_values()
                .rename_axis("Company").reset_index(name="Listings")
            )
            if not employer_counts.empty:
                employer_figure = px.bar(
                    employer_counts,
                    x="Listings",
                    y="Company",
                    orientation="h",
                    color_discrete_sequence=["#176b59"]
                )
                employer_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(style_chart(employer_figure, 390), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

        distribution_columns = st.columns(2, gap="large")
        if "employment_type" in active_jobs:
            employment_counts = (
                active_jobs["employment_type"].replace("", pd.NA).dropna().astype(str)
                .value_counts().head(10).sort_values()
                .rename_axis("Employment type").reset_index(name="Listings")
            )
            if not employment_counts.empty:
                with distribution_columns[0]:
                    st.subheader("Listings by employment type")
                    employment_figure = px.bar(
                        employment_counts,
                        x="Listings",
                        y="Employment type",
                        orientation="h",
                        color_discrete_sequence=["#176b59"]
                    )
                    employment_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                    st.plotly_chart(style_chart(employment_figure, 350), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

        if "experience_level" in active_jobs:
            experience_counts = (
                active_jobs["experience_level"].replace("", pd.NA).dropna().astype(str)
                .value_counts().head(10).sort_values()
                .rename_axis("Experience level").reset_index(name="Listings")
            )
            if not experience_counts.empty:
                with distribution_columns[1]:
                    st.subheader("Listings by experience level")
                    experience_figure = px.bar(
                        experience_counts,
                        x="Listings",
                        y="Experience level",
                        orientation="h",
                        color_discrete_sequence=["#4c7e94"]
                    )
                    experience_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                    st.plotly_chart(style_chart(experience_figure, 350), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

        st.markdown('<div class="section-label">Executive insights</div>', unsafe_allow_html=True)
        insights = []
        title_column = "title" if "title" in active_jobs else None
        if title_column and not active_jobs.empty:
            top_role = active_jobs[title_column].replace("", pd.NA).dropna().astype(str).value_counts()
            if not top_role.empty:
                insights.append(f"{top_role.index[0]} has the most listings ({top_role.iloc[0]:,}).")
        if not active_skill_df.empty and {"skill", "frequency"}.issubset(active_skill_df.columns):
            leading_skill = active_skill_df.iloc[0]
            share = leading_skill["frequency"] / max(len(active_jobs), 1) * 100
            insights.append(
                f"{leading_skill['skill']} appears in {leading_skill['frequency']:,} listings ({share:.1f}% of the current set)."
            )
        if "city" in active_jobs:
            top_city = active_jobs["city"].replace("", pd.NA).dropna().astype(str).value_counts()
            if not top_city.empty:
                insights.append(f"{top_city.index[0]} has the most city-tagged listings ({top_city.iloc[0]:,}).")
        salary_fields = {"title", "salary_min", "salary_max", "salary_currency", "salary_rate_unit"}
        if salary_fields.issubset(active_jobs.columns):
            insight_salary = active_jobs[
                (active_jobs["salary_currency"].fillna("").astype(str).str.upper() == currency_filter)
                & (active_jobs["salary_rate_unit"] == period_filter)
            ].copy()
            insight_salary["salary_midpoint"] = pd.concat([
                pd.to_numeric(insight_salary["salary_min"], errors="coerce"),
                pd.to_numeric(insight_salary["salary_max"], errors="coerce")
            ], axis=1).mean(axis=1)
            insight_salary = insight_salary[insight_salary["salary_midpoint"] > 0]
            paid_roles = insight_salary.groupby("title")["salary_midpoint"].agg(["median", "count"])
            paid_roles = paid_roles[paid_roles["count"] >= 20].sort_values("median", ascending=False)
            if not paid_roles.empty:
                insights.append(
                    f"{paid_roles.index[0]} has the highest median midpoint among roles with at least 20 disclosed {currency_filter}/{period_filter} salaries ({paid_roles.iloc[0]['median']:,.0f})."
                )

        if insights:
            insight_columns = st.columns(min(2, len(insights)))
            for index, insight in enumerate(insights):
                with insight_columns[index % len(insight_columns)]:
                    st.info(insight)
        else:
            st.caption("No insights can be calculated for the current filters.")

        with st.expander("Data quality and coverage"):
            quality_fields = [
                column for column in ["title", "company_name", "city", "country", "date_posted", "salary_min", "salary_max", "extracted_skills"]
                if column in active_jobs
            ]
            if active_jobs.empty or not quality_fields:
                st.info("Data quality metrics are unavailable for the current selection.")
            else:
                missing_rows = []
                missing_cell_count = 0
                for column in quality_fields:
                    values = active_jobs[column]
                    missing = values.isna()
                    if values.dtype == "object" or pd.api.types.is_string_dtype(values):
                        missing |= values.fillna("").astype(str).str.strip().str.lower().isin({"", "unknown", "[]", "nan"})
                    count = int(missing.sum())
                    missing_cell_count += count
                    missing_rows.append({
                        "Field": column.replace("_", " ").title(),
                        "Missing": count,
                        "Missing %": round(count / len(active_jobs) * 100, 1)
                    })

                quality_metrics = st.columns(6)
                with quality_metrics[0]:
                    st.metric("Records", f"{len(active_jobs):,}")
                with quality_metrics[1]:
                    st.metric("Missing field values", f"{missing_cell_count:,}")
                if {"title", "company_name", "city", "date_posted"}.issubset(active_jobs.columns):
                    repeated_keys = int(active_jobs.duplicated(subset=["title", "company_name", "city", "date_posted"]).sum())
                    with quality_metrics[2]:
                        st.metric("Repeated posting keys", f"{repeated_keys:,}")

                if {"salary_min", "salary_max"}.issubset(active_jobs.columns):
                    salary_missing = pd.to_numeric(active_jobs["salary_min"], errors="coerce").isna() & pd.to_numeric(active_jobs["salary_max"], errors="coerce").isna()
                    with quality_metrics[3]:
                        st.metric("No salary range", f"{salary_missing.mean() * 100:.1f}%")
                if {"city", "country"}.issubset(active_jobs.columns):
                    location_missing = active_jobs["city"].fillna("").astype(str).str.strip().eq("") & active_jobs["country"].fillna("").astype(str).str.strip().eq("")
                    with quality_metrics[4]:
                        st.metric("No location", f"{location_missing.mean() * 100:.1f}%")
                if "extracted_skills" in active_jobs:
                    skills_missing = active_jobs["extracted_skills"].fillna("").astype(str).str.strip().isin({"", "[]", "nan"})
                    with quality_metrics[5]:
                        st.metric("No extracted skills", f"{skills_missing.mean() * 100:.1f}%")

                st.dataframe(pd.DataFrame(missing_rows), width="stretch", hide_index=True)
                st.caption("Repeated posting keys use title, employer, city, and posting date; they are not asserted to be exact duplicate rows.")

# ==================================================
# RESUME ANALYZER
# ==================================================

elif page == "📄 Resume Analyzer":

    render_heading(
        "Candidate workspace",
        "Resume match",
        "Compare a candidate profile with the language and skills in current listings."
    )

    upload_col, status_col = st.columns([1.1, 1], gap="large")
    with upload_col:
        uploaded_file = st.file_uploader(
            "Resume file",
            type=["pdf", "docx", "txt"]
        )

    with status_col:
        if uploaded_file is None:
            st.markdown(
                '<div class="empty-state">PDF · DOCX · TXT</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div class="section-label">Selected document</div>', unsafe_allow_html=True)
            st.markdown(f"**{html.escape(uploaded_file.name)}**")

    if uploaded_file is not None:
        try:
            resume_text = read_resume(uploaded_file)
        except Exception as error:
            resume_text = ""
            st.error(f"Resume parsing failed: {error}")

        if resume_text:
            extracted_skills = extract_skills(resume_text)
            st.markdown('<div class="section-label">Detected skills</div>', unsafe_allow_html=True)

            if extracted_skills:
                skill_markup = "".join(
                    f'<span class="skill-tag">{html.escape(str(skill))}</span>'
                    for skill in extracted_skills
                )
                st.markdown(f'<div class="skill-tags">{skill_markup}</div>', unsafe_allow_html=True)
            else:
                st.caption("No skills from the current vocabulary were detected.")

            st.caption("The current parser extracts document text and matches a maintained skills vocabulary; it does not structurally identify education, project history, or certifications.")

            if not active_skill_df.empty and {"skill", "frequency"}.issubset(active_skill_df.columns):
                top_demand_skills = active_skill_df.nlargest(20, "frequency")
                detected = {skill.casefold() for skill in extracted_skills}
                covered_demand = top_demand_skills[
                    top_demand_skills["skill"].astype(str).str.casefold().isin(detected)
                ]["frequency"].sum()
                total_demand = top_demand_skills["frequency"].sum()
                coverage = covered_demand / total_demand * 100 if total_demand else 0
                missing_skills = top_demand_skills[
                    ~top_demand_skills["skill"].astype(str).str.casefold().isin(detected)
                ].head(5)
                score_columns = st.columns(3)
                with score_columns[0]:
                    st.metric("Skills detected", len(extracted_skills))
                with score_columns[1]:
                    st.metric("Top-20 demand coverage", f"{coverage:.1f}%")
                with score_columns[2]:
                    st.metric("High-demand gaps", len(missing_skills))
                if not missing_skills.empty:
                    recommended_markup = "".join(
                        f'<span class="skill-tag">{html.escape(str(skill))}</span>'
                        for skill in missing_skills["skill"]
                    )
                    st.markdown('<div class="section-label">High-demand skills not detected</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="skill-tags">{recommended_markup}</div>', unsafe_allow_html=True)

            with st.expander("Extracted document text"):
                st.text_area("Resume text", resume_text, height=220, label_visibility="collapsed")

            if st.button("Match resume to filtered jobs", type="primary", key="resume_match_button"):
                if active_jobs.empty:
                    st.warning("No job listings match the current global filters.")
                else:
                    try:
                        candidate_jobs, _ = profile_candidate_jobs(resume_text)
                        candidate_jobs = add_matching_text(candidate_jobs)
                        matches = match_resume_to_jobs(resume_text, candidate_jobs).head(10)
                        title_column = "title" if "title" in matches else "job_title"
                        company_column = "company_name" if "company_name" in matches else "company"
                        match_columns = [
                            column for column in [title_column, company_column, "country", "match_score"]
                            if column in matches
                        ]
                        st.caption("Match score is TF-IDF cosine similarity, not a hiring probability.")
                        st.dataframe(
                            matches[match_columns].rename(columns={
                                title_column: "Role",
                                company_column: "Employer",
                                "country": "Location",
                                "match_score": "Similarity %"
                            }),
                            width="stretch",
                            hide_index=True
                        )
                    except Exception as error:
                        st.error(f"Resume matching failed: {error}")

        else:
            st.warning("No readable text was found in this document.")


# ==================================================
# JOB MATCHER
# ==================================================

elif page == "🎯 Job Matcher":

    render_heading(
        "Profile matching",
        "Job matcher",
        "Score a candidate profile against relevant listings using TF-IDF similarity."
    )

    with st.form("job_match_form"):
        profile_text = st.text_area(
            "Candidate profile or resume text",
            height=210,
            placeholder="Paste resume text, skills, and experience..."
        )
        run_matching = st.form_submit_button("Find matching jobs", type="primary")

    if run_matching:
        if not profile_text.strip():
            st.warning("Add a resume or profile summary to find matching jobs.")
        elif active_jobs.empty:
            st.error("The job dataset is unavailable.")
        else:
            try:
                candidate_jobs, narrowed = profile_candidate_jobs(profile_text)
                st.caption(
                    f"Scoring {len(candidate_jobs):,} candidate listings from {len(active_jobs):,} filtered listings."
                )
                candidate_jobs = add_matching_text(candidate_jobs)
                matched_jobs = match_resume_to_jobs(profile_text, candidate_jobs).head(12)
                resume_skill_set = {skill.casefold() for skill in extract_skills(profile_text)}

                def calculate_skill_overlap(value):
                    try:
                        job_skills = ast.literal_eval(str(value))
                    except (ValueError, SyntaxError):
                        return 0.0
                    if not isinstance(job_skills, list) or not job_skills:
                        return 0.0
                    normalized_job_skills = {str(skill).casefold() for skill in job_skills}
                    return len(resume_skill_set & normalized_job_skills) / len(normalized_job_skills) * 100

                if "extracted_skills" in matched_jobs:
                    matched_jobs["skills_overlap"] = matched_jobs["extracted_skills"].apply(calculate_skill_overlap).round(1)
                title_column = "title" if "title" in matched_jobs else "job_title"
                company_column = "company_name" if "company_name" in matched_jobs else "company"
                results = matched_jobs[
                    [column for column in [title_column, company_column, "country", "match_score", "skills_overlap"] if column in matched_jobs]
                ].rename(columns={
                    title_column: "Role",
                    company_column: "Employer",
                    "country": "Location",
                    "match_score": "TF-IDF similarity %",
                    "skills_overlap": "Recognized skills overlap %"
                })
                st.caption("TF-IDF similarity compares resume and listing text; skill overlap is shared recognized skills divided by the listing's extracted skills. Neither score is a hiring probability.")
                st.dataframe(results, width="stretch", hide_index=True)
            except Exception as error:
                st.error(f"Job matching could not be completed: {error}")


# ==================================================
# SKILL GAP
# ==================================================

elif page == "🧩 Skill Gap":

    render_heading(
        "Capability planning",
        "Skill gap",
        "Compare a candidate's detected skills with the most requested capabilities."
    )

    with st.form("skill_gap_form"):
        profile_text = st.text_area(
            "Resume or skills summary",
            height=190,
            placeholder="Paste resume text or list your current skills..."
        )
        analyze_gaps = st.form_submit_button("Analyze skill gaps", type="primary")

    if analyze_gaps:
        candidate_skills = extract_skills(profile_text)
        if not profile_text.strip():
            st.warning("Add a resume or skill summary to see potential gaps.")
        elif not candidate_skills:
            st.info("No skills from the current extraction vocabulary were detected.")
        elif active_skill_df.empty:
            st.warning("Demand skill data is not available.")
        else:
            skill_column = next((column for column in active_skill_df if "skill" in column.lower()), None)
            frequency_column = next(
                (column for column in active_skill_df if any(word in column.lower() for word in ["frequency", "count", "demand"])),
                None
            )
            if skill_column and frequency_column:
                owned = {skill.casefold() for skill in candidate_skills}
                demand = active_skill_df.copy()
                demand["_normalized_skill"] = demand[skill_column].astype(str).str.casefold()
                gaps = demand[~demand["_normalized_skill"].isin(owned)].nlargest(12, frequency_column)
                metric_columns = st.columns(2)
                with metric_columns[0]:
                    st.metric("Detected skills", len(candidate_skills))
                with metric_columns[1]:
                    st.metric("Potential gaps", len(gaps))

                st.markdown('<div class="section-label">Skills detected in profile</div>', unsafe_allow_html=True)
                skill_markup = "".join(
                    f'<span class="skill-tag">{html.escape(skill)}</span>'
                    for skill in candidate_skills
                )
                st.markdown(f'<div class="skill-tags">{skill_markup}</div>', unsafe_allow_html=True)

                st.subheader("Frequently requested skills not detected")
                if gaps.empty:
                    st.success("All skills in the current demand list were detected in this profile.")
                else:
                    gap_figure = px.bar(
                        gaps.sort_values(frequency_column),
                        x=frequency_column,
                        y=skill_column,
                        orientation="h",
                        color_discrete_sequence=["#d66a43"]
                    )
                    gap_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                    st.plotly_chart(style_chart(gap_figure, 360), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})


# ==================================================
# CAREER RECOMMENDATIONS
# ==================================================

elif page == "🚀 Career Recommendations":

    render_heading(
        "Next-step planning",
        "Career recommendations",
        "Explore roles with strong language similarity to the candidate's experience."
    )

    with st.form("career_recommendation_form"):
        profile_text = st.text_area(
            "Candidate experience and interests",
            height=210,
            placeholder="Describe your experience, skills, and the work you want to do..."
        )
        recommend = st.form_submit_button("Recommend roles", type="primary")

    if recommend:
        if not profile_text.strip():
            st.warning("Add experience or interests to generate recommendations.")
        elif active_jobs.empty:
            st.error("The job dataset is unavailable.")
        else:
            try:
                candidate_jobs, narrowed = profile_candidate_jobs(profile_text)
                candidate_jobs = add_matching_text(candidate_jobs)
                matches = match_resume_to_jobs(profile_text, candidate_jobs)
                title_column = "title" if "title" in matches else "job_title"
                company_column = "company_name" if "company_name" in matches else "company"
                matches = matches.sort_values("match_score", ascending=False)
                recommendations = (
                    matches
                    .drop_duplicates(subset=[title_column])
                    .head(8)
                )
                st.caption(f"Recommendations ranked from {len(candidate_jobs):,} candidate listings.")
                recommendation_columns = [
                    column for column in [title_column, company_column, "country", "match_score"]
                    if column in recommendations
                ]
                st.dataframe(
                    recommendations[recommendation_columns].rename(columns={
                        title_column: "Recommended role",
                        company_column: "Employer",
                        "country": "Location",
                        "match_score": "Similarity %"
                    }),
                    width="stretch",
                    hide_index=True
                )

                candidate_skills = {skill.casefold() for skill in extract_skills(profile_text)}
                if not active_skill_df.empty:
                    skill_column = next((column for column in active_skill_df if "skill" in column.lower()), None)
                    frequency_column = next(
                        (column for column in active_skill_df if any(word in column.lower() for word in ["frequency", "count", "demand"])),
                        None
                    )
                    if skill_column and frequency_column:
                        focus_skills = active_skill_df.copy()
                        focus_skills["_normalized_skill"] = focus_skills[skill_column].astype(str).str.casefold()
                        focus_skills = focus_skills[~focus_skills["_normalized_skill"].isin(candidate_skills)]
                        focus_skills = focus_skills.nlargest(5, frequency_column)
                        if not focus_skills.empty:
                            st.markdown('<div class="section-label">Skills to strengthen for broader options</div>', unsafe_allow_html=True)
                            skill_markup = "".join(
                                f'<span class="skill-tag">{html.escape(str(skill))}</span>'
                                for skill in focus_skills[skill_column]
                            )
                            st.markdown(f'<div class="skill-tags">{skill_markup}</div>', unsafe_allow_html=True)
            except Exception as error:
                st.error(f"Recommendations could not be generated: {error}")


# ==================================================
# JOB MARKET
# ==================================================

elif page == "💼 Job Explorer":

    render_heading(
        "Listing explorer",
        "Job market",
        "Search roles and compare employers, locations, and working arrangements."
    )

    if active_jobs.empty:
        st.error("The job dataset is unavailable.")
    else:
        title_column = "title" if "title" in active_jobs else "job_title"
        company_column = "company_name" if "company_name" in active_jobs else "company"
        country_column = "country" if "country" in active_jobs else None
        filter_col1, filter_col2, filter_col3 = st.columns([1.2, 1, .8])

        with filter_col1:
            query = st.text_input("Role or employer", placeholder="Search listings")
        with filter_col2:
            location_options = ["All locations"]
            if country_column:
                location_options.extend(sorted(active_jobs[country_column].dropna().astype(str).unique()))
            selected_location = st.selectbox("Location", location_options)
        with filter_col3:
            row_limit = st.selectbox("Rows", [25, 50, 100], index=1)
        include_descriptions = st.checkbox("Search full descriptions", value=False)

        filtered_jobs = active_jobs
        if country_column and selected_location != "All locations":
            filtered_jobs = filtered_jobs[filtered_jobs[country_column].astype(str) == selected_location]
        if query:
            title_matches = filtered_jobs[title_column].astype(str).str.contains(query, case=False, na=False, regex=False)
            company_matches = filtered_jobs[company_column].astype(str).str.contains(query, case=False, na=False, regex=False)
            skill_matches = (
                filtered_jobs["extracted_skills"].astype(str).str.contains(query, case=False, na=False, regex=False)
                if "extracted_skills" in filtered_jobs
                else pd.Series(False, index=filtered_jobs.index)
            )
            query_matches = title_matches | company_matches | skill_matches
            if include_descriptions:
                description_matches = load_job_texts().reindex(filtered_jobs.index).fillna("").str.contains(
                    query, case=False, na=False, regex=False
                )
                query_matches |= description_matches
            filtered_jobs = filtered_jobs[query_matches]

        metric_col, spacer = st.columns([1, 3])
        with metric_col:
            st.metric("Matching listings", f"{len(filtered_jobs):,}")

        display_columns = [
            column for column in [title_column, company_column, "city", country_column, "employment_type", "work_model", "experience_level", "salary_min", "salary_max", "salary_currency", "salary_rate_unit", "date_posted"]
            if column and column in filtered_jobs
        ]
        detail_jobs = filtered_jobs.head(row_limit)
        st.dataframe(
            detail_jobs[display_columns],
            width="stretch",
            hide_index=True
        )

        if not detail_jobs.empty:
            detail_options = {}
            for row_index, row in detail_jobs.iterrows():
                label = f"{row.get(title_column, 'Job')} | {row.get(company_column, 'Employer')} | {row_index}"
                detail_options[label] = row_index
            selected_detail = st.selectbox("View details", list(detail_options), key="job_detail_selection")
            selected_index = detail_options[selected_detail]
            selected_row = filtered_jobs.loc[selected_index]
            with st.expander("Listing details"):
                st.markdown(f"### {html.escape(str(selected_row.get(title_column, 'Job')))}")
                st.write(f"Employer: {selected_row.get(company_column, 'Data unavailable')}")
                st.write(f"Location: {selected_row.get('city', 'Data unavailable')}, {selected_row.get(country_column, 'Data unavailable')}")
                st.write(f"Employment: {selected_row.get('employment_type', 'Data unavailable')} | Work model: {selected_row.get('work_model', 'Data unavailable')}")
                st.write(f"Experience: {selected_row.get('experience_level', 'Data unavailable')} | Years: {selected_row.get('years_experience_numeric', 'Data unavailable')}")
                salary_text = "Data unavailable"
                if pd.notna(selected_row.get("salary_min")) or pd.notna(selected_row.get("salary_max")):
                    salary_text = f"{selected_row.get('salary_min', 'N/A')} - {selected_row.get('salary_max', 'N/A')} {selected_row.get('salary_currency', '')} / {selected_row.get('salary_rate_unit', '')}"
                st.write(f"Salary: {salary_text}")
                try:
                    required_skills = ast.literal_eval(str(selected_row.get("extracted_skills", "[]")))
                except (ValueError, SyntaxError):
                    required_skills = []
                if required_skills:
                    st.write("Required skills: " + ", ".join(str(skill) for skill in required_skills))
                if st.button("Load full job description", key=f"job_description_{selected_index}"):
                    full_text = load_job_texts().get(selected_index, "")
                    st.text_area("Full job text", full_text, height=240, label_visibility="collapsed")


# ==================================================
# SKILL ANALYSIS
# ==================================================

elif page == "🧠 Skills Intelligence":

    render_heading(
        "Capability signals",
        "Skill demand",
        "Ranked mentions across the job descriptions and qualifications in this dataset."
    )

    if active_skill_df.empty:
        st.warning("No extracted skill records are available.")
    else:
        skill_column = next((column for column in active_skill_df if "skill" in column.lower()), None)
        frequency_column = next(
            (column for column in active_skill_df if any(word in column.lower() for word in ["frequency", "count", "demand"])),
            None
        )

        if skill_column and frequency_column:
            top_skill = active_skill_df.sort_values(frequency_column, ascending=False).iloc[0]
            metric_col, control_col = st.columns([1, 2])
            with metric_col:
                st.metric("Leading skill", str(top_skill[skill_column]))
            with control_col:
                skill_limit = st.slider("Skills shown", 5, min(30, max(5, len(active_skill_df))), min(15, max(5, len(active_skill_df))))

            chart_df = active_skill_df.nlargest(skill_limit, frequency_column).sort_values(frequency_column)
            skill_figure = px.bar(
                chart_df,
                x=frequency_column,
                y=skill_column,
                orientation="h",
                color_discrete_sequence=["#d66a43"]
            )
            skill_figure.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(style_chart(skill_figure, max(350, skill_limit * 27)), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})
            chart_df["Demand %"] = (chart_df[frequency_column] / max(len(active_jobs), 1) * 100).round(1)
            st.dataframe(
                chart_df.sort_values(frequency_column, ascending=False),
                width="stretch",
                hide_index=True
            )

            st.caption("The source dataset does not include a skill taxonomy; category and technology/soft-skill splits are unavailable.")
            with st.expander("Inspect a skill"):
                selected_skill = st.selectbox(
                    "Skill details",
                    active_skill_df[skill_column].astype(str).tolist(),
                    key="skill_detail_selection"
                )
                if st.button("Load skill profile", key="load_skill_profile"):
                    skill_summary = skill_trend_summary(
                        selected_skill,
                        global_search,
                        location_filter,
                        industry_filter,
                        experience_filter,
                        employment_filter,
                        company_filter,
                        salary_filter_enabled,
                        currency_filter,
                        period_filter,
                        tuple(salary_range_filter) if salary_range_filter else None,
                        date_filter_range
                    )
                    detail_metrics = st.columns(4)
                    with detail_metrics[0]:
                        st.metric("Job postings", f"{skill_summary['jobs']:,}")
                    with detail_metrics[1]:
                        st.metric("Demand", f"{skill_summary['jobs'] / max(len(active_jobs), 1) * 100:.1f}%")
                    with detail_metrics[2]:
                        st.metric("Top location count", f"{int(skill_summary['locations']['Listings'].sum()):,}" if not skill_summary["locations"].empty else "Data unavailable")
                    with detail_metrics[3]:
                        st.metric(
                            f"Median salary - {currency_filter}/{period_filter}",
                            f"{skill_summary['salary_median']:,.0f}" if skill_summary["salary_median"] is not None else "Data unavailable"
                        )
                    detail_col1, detail_col2 = st.columns(2)
                    with detail_col1:
                        st.markdown("**Common roles**")
                        st.dataframe(skill_summary["roles"], width="stretch", hide_index=True)
                    with detail_col2:
                        st.markdown("**Top locations**")
                        st.dataframe(skill_summary["locations"], width="stretch", hide_index=True)

            st.subheader("Skill co-occurrence")
            st.caption("Pair counts are calculated from postings that contain both selected skills.")
            cooccurrence_skills = tuple(
                active_skill_df.nlargest(min(10, skill_limit), frequency_column)[skill_column].astype(str)
            )
            if st.button("Calculate co-occurrence heatmap", key="calculate_skill_cooccurrence"):
                cooccurrence = skill_cooccurrence_matrix(
                    cooccurrence_skills,
                    global_search,
                    location_filter,
                    industry_filter,
                    experience_filter,
                    employment_filter,
                    company_filter,
                    salary_filter_enabled,
                    currency_filter,
                    period_filter,
                    tuple(salary_range_filter) if salary_range_filter else None,
                    date_filter_range
                )
                heatmap = px.imshow(
                    cooccurrence,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale=["#f1f6f3", "#176b59"]
                )
                heatmap.update_layout(
                    height=520,
                    margin=dict(l=8, r=16, t=12, b=8),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans, sans-serif", color="#52665f", size=11)
                )
                st.plotly_chart(heatmap, width="stretch", config={"displayModeBar": "hover", "displaylogo": False})


# ==================================================
# SALARY PREDICTION
# ==================================================

elif page == "📈 Skill Trends":

    render_heading(
        "Time-aware demand",
        "Skill trends",
        "Explore dated postings for a selected skill; historical coverage is limited to records with dates."
    )

    if active_skill_df.empty or not {"skill", "frequency"}.issubset(active_skill_df.columns):
        st.info("Skill trend data is unavailable for the current filters.")
    else:
        selected_skill = st.selectbox(
            "Skill",
            active_skill_df["skill"].astype(str).tolist(),
            key="skill_trend_selection"
        )
        skill_row = active_skill_df.loc[active_skill_df["skill"] == selected_skill].iloc[0]
        summary = skill_trend_summary(
            selected_skill,
            global_search,
            location_filter,
            industry_filter,
            experience_filter,
            employment_filter,
            company_filter,
            salary_filter_enabled,
            currency_filter,
            period_filter,
            tuple(salary_range_filter) if salary_range_filter else None,
            date_filter_range
        )
        skill_share = skill_row["frequency"] / max(len(active_jobs), 1) * 100
        trend_metrics = st.columns(4)
        with trend_metrics[0]:
            st.metric("Skill demand", f"{skill_share:.1f}% of listings")
        with trend_metrics[1]:
            st.metric("Tagged job count", f"{summary['jobs']:,}")
        with trend_metrics[2]:
            st.metric("Dated skill listings", f"{summary['dated_jobs']:,}")
        with trend_metrics[3]:
            st.metric(
                f"Median salary - {currency_filter}/{period_filter}",
                f"{summary['salary_median']:,.0f}" if summary["salary_median"] is not None else "Data unavailable"
            )

        trend_columns = st.columns(2, gap="large")
        with trend_columns[0]:
            st.subheader("Demand over time")
            if summary["trend"].empty:
                st.info("Historical demand is unavailable because matching listings do not have parseable posting dates.")
            else:
                trend_figure = px.line(
                    summary["trend"],
                    x="Month",
                    y="Listings",
                    markers=True,
                    color_discrete_sequence=["#176b59"]
                )
                st.plotly_chart(style_chart(trend_figure, 360), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})
                coverage = summary["dated_jobs"] / max(summary["jobs"], 1) * 100
                st.caption(f"Partial historical coverage: {summary['dated_jobs']:,} of {summary['jobs']:,} tagged listings ({coverage:.1f}%).")

        with trend_columns[1]:
            st.subheader("Common roles")
            if summary["roles"].empty:
                st.info("Role breakdown unavailable.")
            else:
                st.dataframe(summary["roles"], width="stretch", hide_index=True)

            st.subheader("Top locations")
            if summary["locations"].empty:
                st.info("Location breakdown unavailable.")
            else:
                st.dataframe(summary["locations"], width="stretch", hide_index=True)


elif page == "💰 Salary Intelligence":

    render_heading(
        "Compensation toolkit",
        "Salary intelligence",
        "Compare disclosed salary ranges on a consistent currency and pay-period basis."
    )

    salary_columns = {"salary_min", "salary_max", "salary_currency", "salary_rate_unit"}
    if not active_jobs.empty and salary_columns.issubset(active_jobs.columns):
        salary_data_columns = [
            column for column in [
                "salary_min", "salary_max", "salary_currency", "salary_rate_unit",
                "title", "city", "years_experience_numeric", "employment_type", "extracted_skills"
            ]
            if column in active_jobs
        ]
        salary_data = active_jobs[salary_data_columns].copy()
        salary_data["salary_min"] = pd.to_numeric(salary_data["salary_min"], errors="coerce")
        salary_data["salary_max"] = pd.to_numeric(salary_data["salary_max"], errors="coerce")
        salary_data["salary_currency"] = (
            salary_data["salary_currency"]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.upper()
        )
        salary_data["salary_rate_unit"] = normalize_pay_period(salary_data["salary_rate_unit"])
        salary_data["salary_midpoint"] = salary_data[["salary_min", "salary_max"]].mean(axis=1)
        salary_data = salary_data[salary_data["salary_midpoint"] > 0]

        if not salary_data.empty:
            salary_filter_col1, salary_filter_col2 = st.columns(2)
            currencies = sorted(salary_data["salary_currency"].unique())
            rate_units = sorted(salary_data["salary_rate_unit"].unique())
            default_currency = currencies.index("USD") if "USD" in currencies else 0
            default_rate = rate_units.index("year") if "year" in rate_units else 0

            with salary_filter_col1:
                selected_currency = st.selectbox("Currency", currencies, index=default_currency)
            with salary_filter_col2:
                selected_rate = st.selectbox("Pay period", rate_units, index=default_rate)

            comparable_salary = salary_data[
                (salary_data["salary_currency"] == selected_currency)
                & (salary_data["salary_rate_unit"] == selected_rate)
            ]

            if comparable_salary.empty:
                st.info("No salary records are available for this combination.")
            else:
                salary_metric_col1, salary_metric_col2, salary_metric_col3, salary_metric_col4, salary_metric_col5 = st.columns(5)
                with salary_metric_col1:
                    st.metric("Disclosed records", f"{len(comparable_salary):,}")
                with salary_metric_col2:
                    st.metric("Average midpoint", f"{comparable_salary['salary_midpoint'].mean():,.0f}")
                with salary_metric_col3:
                    st.metric("Median midpoint", f"{comparable_salary['salary_midpoint'].median():,.0f}")
                with salary_metric_col4:
                    st.metric("Minimum observed", f"{comparable_salary['salary_midpoint'].min():,.0f}")
                with salary_metric_col5:
                    st.metric("Maximum observed", f"{comparable_salary['salary_midpoint'].max():,.0f}")
                st.caption(f"Comparison basis: {selected_currency} / {selected_rate}.")

                lower_bound = comparable_salary["salary_midpoint"].quantile(.01)
                upper_bound = comparable_salary["salary_midpoint"].quantile(.99)
                chart_data = comparable_salary[
                    comparable_salary["salary_midpoint"].between(lower_bound, upper_bound)
                ]
                salary_figure = px.histogram(
                    chart_data,
                    x="salary_midpoint",
                    nbins=32,
                    color_discrete_sequence=["#4c7e94"]
                )
                salary_figure.update_layout(
                    height=350,
                    margin=dict(l=8, r=16, t=12, b=8),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans, sans-serif", color="#52665f", size=12),
                    xaxis=dict(title=f"Salary midpoint ({selected_currency} / {selected_rate})", showgrid=False),
                    yaxis=dict(title="Listings", showgrid=True, gridcolor="#e8efeb"),
                    transition=dict(duration=550, easing="cubic-in-out")
                )
                st.plotly_chart(salary_figure, width="stretch", config={"displayModeBar": "hover", "displaylogo": False})
                st.caption("The histogram trims the outer 1% at each end for readability; the median uses all selected records.")

                salary_chart_columns = st.columns(2, gap="large")
                if "title" in comparable_salary:
                    by_role = comparable_salary.groupby("title")["salary_midpoint"].agg(["median", "count"])
                    by_role = by_role[by_role["count"] >= 20].nlargest(10, "median").sort_values("median")
                    if not by_role.empty:
                        with salary_chart_columns[0]:
                            st.subheader("Median by role")
                            role_figure = px.bar(
                                by_role.reset_index(),
                                x="median",
                                y="title",
                                orientation="h",
                                color_discrete_sequence=["#176b59"]
                            )
                            role_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                            st.plotly_chart(style_chart(role_figure, 350), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

                if "city" in comparable_salary:
                    by_city = comparable_salary.groupby("city")["salary_midpoint"].agg(["median", "count"])
                    by_city = by_city[by_city["count"] >= 20].nlargest(10, "median").sort_values("median")
                    if not by_city.empty:
                        with salary_chart_columns[1]:
                            st.subheader("Median by city")
                            city_figure = px.bar(
                                by_city.reset_index(),
                                x="median",
                                y="city",
                                orientation="h",
                                color_discrete_sequence=["#4c7e94"]
                            )
                            city_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                            st.plotly_chart(style_chart(city_figure, 350), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

                breakdown_columns = st.columns(2, gap="large")
                if "employment_type" in comparable_salary:
                    by_employment = comparable_salary.groupby("employment_type")["salary_midpoint"].agg(["median", "count"])
                    by_employment = by_employment[by_employment["count"] >= 20].nlargest(10, "median").reset_index()
                    if not by_employment.empty:
                        with breakdown_columns[0]:
                            st.subheader("Median by employment type")
                            employment_figure = px.bar(
                                by_employment,
                                x="employment_type",
                                y="median",
                                color_discrete_sequence=["#d66a43"]
                            )
                            st.plotly_chart(style_chart(employment_figure, 350), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

                if "years_experience_numeric" in comparable_salary:
                    by_experience = comparable_salary.copy()
                    by_experience["years_experience_numeric"] = pd.to_numeric(by_experience["years_experience_numeric"], errors="coerce")
                    by_experience = by_experience.dropna(subset=["years_experience_numeric"])
                    if not by_experience.empty:
                        by_experience["Experience band"] = pd.cut(
                            by_experience["years_experience_numeric"],
                            bins=[-0.01, 1, 3, 5, 10, float("inf")],
                            labels=["0-1", "1-3", "3-5", "5-10", "10+"]
                        )
                        experience_summary = by_experience.groupby("Experience band", observed=True)["salary_midpoint"].agg(["median", "count"]).reset_index()
                        experience_summary = experience_summary[experience_summary["count"] >= 20]
                        if not experience_summary.empty:
                            with breakdown_columns[1]:
                                st.subheader("Median by experience")
                                experience_figure = px.bar(
                                    experience_summary,
                                    x="Experience band",
                                    y="median",
                                    color_discrete_sequence=["#176b59"]
                                )
                                st.plotly_chart(style_chart(experience_figure, 350), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

                if "extracted_skills" in comparable_salary and "skill" in active_skill_df:
                    skill_salary_rows = []
                    for skill in active_skill_df["skill"].astype(str).head(10):
                        skill_pattern = re.compile(r"['\"]" + re.escape(skill) + r"['\"]", re.IGNORECASE)
                        matched_skill_salary = comparable_salary[
                            comparable_salary["extracted_skills"].fillna("").astype(str).str.contains(skill_pattern)
                        ]
                        if len(matched_skill_salary) >= 20:
                            skill_salary_rows.append({
                                "Skill": skill,
                                "Median": matched_skill_salary["salary_midpoint"].median(),
                                "Listings": len(matched_skill_salary)
                            })
                    if skill_salary_rows:
                        st.subheader("Median by extracted skill")
                        skill_salary_frame = pd.DataFrame(skill_salary_rows).sort_values("Median")
                        skill_salary_figure = px.bar(
                            skill_salary_frame,
                            x="Median",
                            y="Skill",
                            orientation="h",
                            color_discrete_sequence=["#4c7e94"]
                        )
                        skill_salary_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                        st.plotly_chart(style_chart(skill_salary_figure, 350), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

                with st.expander("Compare salary by role, location, experience, and skill"):
                    compare_col1, compare_col2 = st.columns(2)
                    role_options = ["All"] + (
                        comparable_salary["title"].dropna().astype(str).value_counts().head(100).index.tolist()
                        if "title" in comparable_salary else []
                    )
                    city_options = ["All"] + (
                        comparable_salary["city"].dropna().astype(str).value_counts().head(100).index.tolist()
                        if "city" in comparable_salary else []
                    )
                    with compare_col1:
                        role_filter = st.selectbox("Role", role_options, key="salary_compare_role")
                        city_filter = st.selectbox("City", city_options, key="salary_compare_city")
                    with compare_col2:
                        experience_bounds = None
                        if "years_experience_numeric" in comparable_salary:
                            experience_values = pd.to_numeric(comparable_salary["years_experience_numeric"], errors="coerce").dropna()
                            if not experience_values.empty:
                                experience_min = float(experience_values.min())
                                experience_max = float(experience_values.quantile(.99))
                                if experience_max <= experience_min:
                                    experience_max = experience_min + 1
                                experience_bounds = st.slider(
                                    "Years of experience",
                                    min_value=experience_min,
                                    max_value=experience_max,
                                    value=(experience_min, experience_max),
                                    key="salary_compare_experience"
                                )
                        skill_filter = st.selectbox(
                            "Skill",
                            ["All"] + (active_skill_df["skill"].astype(str).head(50).tolist() if "skill" in active_skill_df else []),
                            key="salary_compare_skill"
                        )

                    comparison = comparable_salary
                    if role_filter != "All" and "title" in comparison:
                        comparison = comparison[comparison["title"].astype(str) == role_filter]
                    if city_filter != "All" and "city" in comparison:
                        comparison = comparison[comparison["city"].astype(str) == city_filter]
                    if experience_bounds and "years_experience_numeric" in comparison:
                        numeric_experience = pd.to_numeric(comparison["years_experience_numeric"], errors="coerce")
                        comparison = comparison[numeric_experience.between(*experience_bounds)]
                    if skill_filter != "All" and "extracted_skills" in comparison:
                        exact_skill = re.compile(r"['\"]" + re.escape(skill_filter) + r"['\"]", re.IGNORECASE)
                        comparison = comparison[comparison["extracted_skills"].fillna("").astype(str).str.contains(exact_skill)]

                    if comparison.empty:
                        st.info("No salary records match this comparison.")
                    else:
                        comparison_metrics = st.columns(4)
                        with comparison_metrics[0]:
                            st.metric("Records", f"{len(comparison):,}")
                        with comparison_metrics[1]:
                            st.metric("Average", f"{comparison['salary_midpoint'].mean():,.0f}")
                        with comparison_metrics[2]:
                            st.metric("Median", f"{comparison['salary_midpoint'].median():,.0f}")
                        with comparison_metrics[3]:
                            st.metric("Observed range", f"{comparison['salary_midpoint'].min():,.0f} - {comparison['salary_midpoint'].max():,.0f}")
        else:
            st.info("No positive salary ranges are available in the dataset.")

    st.markdown('<div class="section-label">Prediction model</div>', unsafe_allow_html=True)

    if salary_model is None:

        st.warning(
            "salary_model.joblib was not found "
            "or could not be loaded."
        )

    else:

        st.caption("MODEL READY · Prediction is reported in the model's training target units.")

        feature_names = list(
            getattr(salary_model, "feature_names_in_", [])
        )

        if not feature_names:
            st.error("The loaded salary model does not expose its input features.")
            st.stop()

        preprocessor = getattr(
            getattr(salary_model, "named_steps", {}),
            "get",
            lambda *_: None
        )("preprocessor")
        numeric_features = set()
        categorical_defaults = {}

        for transformer_name, transformer, columns in getattr(
            preprocessor,
            "transformers_",
            []
        ):
            columns = [columns] if isinstance(columns, str) else list(columns)

            if "numeric" in transformer_name.lower():
                numeric_features.update(columns)

            encoder = getattr(transformer, "named_steps", {}).get(
                "encoder",
                transformer
            )
            categories = getattr(encoder, "categories_", [])

            for column, values in zip(columns, categories):
                if len(values):
                    categorical_defaults[column] = str(values[0])

        with st.form("salary_estimator"):
            feature_values = {}
            input_columns = st.columns(2)

            for index, feature in enumerate(feature_names):
                label = feature.replace("_", " ").title()

                with input_columns[index % 2]:
                    if feature in numeric_features:
                        feature_values[feature] = st.number_input(
                            label,
                            min_value=0.0,
                            value=1.0,
                            key=f"salary_{feature}"
                        )
                    else:
                        feature_values[feature] = st.text_input(
                            label,
                            value=categorical_defaults.get(feature, ""),
                            key=f"salary_{feature}"
                        )

            submitted = st.form_submit_button("Calculate estimate", type="primary")

        if submitted:
            try:
                input_data = pd.DataFrame([feature_values], columns=feature_names)
                prediction = salary_model.predict(input_data)
                st.metric("Estimated target units", f"{prediction[0]:,.2f}")
            except Exception as error:
                st.error(f"Salary prediction failed: {error}")


elif page == "🏢 Company Intelligence":

    render_heading(
        "Employer profiles",
        "Company intelligence",
        "Explore hiring volume, common roles, skills, locations, and disclosed pay by employer."
    )

    if active_jobs.empty or "company_name" not in active_jobs:
        st.info("Company-level data is unavailable for the current filters.")
    else:
        company_counts = active_jobs["company_name"].replace("", pd.NA).dropna().astype(str).value_counts()
        company_options = company_counts.head(200).index.tolist()
        if not company_options:
            st.info("No employers are present in the current selection.")
        else:
            selected_company = st.selectbox("Company", company_options, key="company_intelligence_selection")
            company_jobs = active_jobs[active_jobs["company_name"].astype(str) == selected_company]
            title_column = "title" if "title" in company_jobs else None
            role_count = company_jobs[title_column].nunique() if title_column else 0
            location_count = company_jobs["city"].nunique() if "city" in company_jobs else 0
            company_salary = company_jobs
            salary_fields = {"salary_min", "salary_max", "salary_currency", "salary_rate_unit"}
            if salary_fields.issubset(company_jobs.columns):
                company_salary = company_jobs[
                    (company_jobs["salary_currency"].fillna("").astype(str).str.upper() == currency_filter)
                    & (company_jobs["salary_rate_unit"] == period_filter)
                ].copy()
                company_salary["salary_midpoint"] = pd.concat([
                    pd.to_numeric(company_salary["salary_min"], errors="coerce"),
                    pd.to_numeric(company_salary["salary_max"], errors="coerce")
                ], axis=1).mean(axis=1)
                company_salary = company_salary[company_salary["salary_midpoint"] > 0]
            else:
                company_salary = pd.DataFrame()

            company_metrics = st.columns(4)
            with company_metrics[0]:
                st.metric("Job listings", f"{len(company_jobs):,}")
            with company_metrics[1]:
                st.metric("Distinct roles", f"{role_count:,}")
            with company_metrics[2]:
                st.metric("Cities represented", f"{location_count:,}")
            with company_metrics[3]:
                st.metric(
                    f"Median salary - {currency_filter}/{period_filter}",
                    f"{company_salary['salary_midpoint'].median():,.0f}" if not company_salary.empty else "Data unavailable"
                )

            role_col, skill_col = st.columns(2, gap="large")
            if title_column:
                with role_col:
                    st.subheader("Top roles")
                    role_counts = company_jobs[title_column].dropna().astype(str).value_counts().head(10).sort_values()
                    role_frame = role_counts.rename_axis("Role").reset_index(name="Listings")
                    role_figure = px.bar(role_frame, x="Listings", y="Role", orientation="h", color_discrete_sequence=["#176b59"])
                    role_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                    st.plotly_chart(style_chart(role_figure, 360), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

            if "extracted_skills" in company_jobs:
                company_skill_counts = {}
                for value in company_jobs["extracted_skills"].dropna():
                    try:
                        parsed = ast.literal_eval(str(value))
                    except (ValueError, SyntaxError):
                        continue
                    if isinstance(parsed, list):
                        for skill in parsed:
                            company_skill_counts[str(skill)] = company_skill_counts.get(str(skill), 0) + 1
                if company_skill_counts:
                    with skill_col:
                        st.subheader("Top extracted skills")
                        company_skill_frame = pd.Series(company_skill_counts).nlargest(10).sort_values().rename_axis("Skill").reset_index(name="Listings")
                        skill_figure = px.bar(company_skill_frame, x="Listings", y="Skill", orientation="h", color_discrete_sequence=["#d66a43"])
                        skill_figure.update_layout(yaxis={"categoryorder": "total ascending"})
                        st.plotly_chart(style_chart(skill_figure, 360), width="stretch", config={"displayModeBar": "hover", "displaylogo": False})

            if "city" in company_jobs:
                st.subheader("Hiring locations")
                city_counts = company_jobs["city"].replace("", pd.NA).dropna().astype(str).value_counts().head(12)
                st.dataframe(city_counts.rename_axis("City").reset_index(name="Listings"), width="stretch", hide_index=True)


elif page == "🗺️ Location Intelligence":

    render_heading(
        "Geographic demand",
        "Location intelligence",
        "Compare hiring concentration using the cities and coordinates present in the dataset."
    )

    geo_fields = {"city", "country", "latitude", "longitude", "title"}
    if active_jobs.empty or not geo_fields.issubset(active_jobs.columns):
        st.info("Geographic data is unavailable for the current selection.")
    else:
        geographic_jobs = active_jobs.copy()
        geographic_jobs["latitude"] = pd.to_numeric(geographic_jobs["latitude"], errors="coerce")
        geographic_jobs["longitude"] = pd.to_numeric(geographic_jobs["longitude"], errors="coerce")
        geographic_jobs = geographic_jobs[
            geographic_jobs["latitude"].between(-90, 90)
            & geographic_jobs["longitude"].between(-180, 180)
        ]

        if geographic_jobs.empty:
            st.info("No valid coordinates are available for the current filters.")
        else:
            location_summary = (
                geographic_jobs
                .groupby(["city", "country"], dropna=False)
                .agg(
                    Latitude=("latitude", "median"),
                    Longitude=("longitude", "median"),
                    Listings=("title", "size"),
                    **{"Top role": ("title", lambda values: values.dropna().astype(str).value_counts().index[0] if values.notna().any() else "Data unavailable")}
                )
                .reset_index()
            )
            location_summary["Location"] = (
                location_summary["city"].fillna("Unknown city").astype(str)
                + ", "
                + location_summary["country"].fillna("Unknown country").astype(str)
            )
            location_summary = location_summary.sort_values("Listings", ascending=False)
            map_data = location_summary.head(750)
            st.caption(f"Mapped {len(map_data):,} highest-volume city/country points with valid coordinates.")
            map_figure = px.scatter_mapbox(
                map_data,
                lat="Latitude",
                lon="Longitude",
                size="Listings",
                color="Listings",
                hover_name="Location",
                hover_data={"Top role": True, "Listings": True, "Latitude": False, "Longitude": False},
                color_continuous_scale=["#b8dbcd", "#176b59"],
                size_max=22,
                zoom=1,
                mapbox_style="open-street-map"
            )
            map_figure.update_layout(
                height=560,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans, sans-serif", color="#52665f", size=12)
            )
            st.plotly_chart(map_figure, width="stretch", config={"displayModeBar": "hover", "displaylogo": False})
            st.subheader("Highest-demand locations")
            st.dataframe(
                location_summary[["Location", "Listings", "Top role"]].head(25),
                width="stretch",
                hide_index=True
            )

            selected_location = st.selectbox(
                "Inspect a location",
                location_summary["Location"].head(100).tolist(),
                key="location_intelligence_selection"
            )
            selected_location_row = location_summary.loc[
                location_summary["Location"] == selected_location
            ].iloc[0]
            selected_city = selected_location_row["city"]
            selected_country = selected_location_row["country"]
            city_mask = (
                active_jobs["city"].isna()
                if pd.isna(selected_city)
                else active_jobs["city"].astype(str) == str(selected_city)
            )
            country_mask = (
                active_jobs["country"].isna()
                if pd.isna(selected_country)
                else active_jobs["country"].astype(str) == str(selected_country)
            )
            selected_location_jobs = active_jobs[city_mask & country_mask]
            selected_location_metrics = st.columns(3)
            with selected_location_metrics[0]:
                st.metric("Job demand", f"{len(selected_location_jobs):,}")
            with selected_location_metrics[1]:
                st.metric("Distinct roles", f"{selected_location_jobs['title'].nunique():,}")

            location_salary_median = None
            location_salary_fields = {"salary_min", "salary_max", "salary_currency", "salary_rate_unit"}
            if location_salary_fields.issubset(selected_location_jobs.columns):
                location_salary = selected_location_jobs[
                    (selected_location_jobs["salary_currency"].fillna("").astype(str).str.upper() == currency_filter)
                    & (selected_location_jobs["salary_rate_unit"] == period_filter)
                ]
                location_midpoints = pd.concat([
                    pd.to_numeric(location_salary["salary_min"], errors="coerce"),
                    pd.to_numeric(location_salary["salary_max"], errors="coerce")
                ], axis=1).mean(axis=1)
                location_midpoints = location_midpoints[location_midpoints > 0]
                if not location_midpoints.empty:
                    location_salary_median = location_midpoints.median()
            with selected_location_metrics[2]:
                st.metric(
                    f"Median - {currency_filter}/{period_filter}",
                    f"{location_salary_median:,.0f}" if location_salary_median is not None else "Data unavailable"
                )

            location_detail_columns = st.columns(2)
            with location_detail_columns[0]:
                st.markdown("**Top roles**")
                top_location_roles = selected_location_jobs["title"].value_counts().head(10)
                st.dataframe(top_location_roles.rename_axis("Role").reset_index(name="Listings"), width="stretch", hide_index=True)
            with location_detail_columns[1]:
                st.markdown("**Top extracted skills**")
                location_skill_counts = {}
                for value in selected_location_jobs.get("extracted_skills", pd.Series(dtype="string")).dropna():
                    try:
                        parsed_skills = ast.literal_eval(str(value))
                    except (ValueError, SyntaxError):
                        continue
                    if isinstance(parsed_skills, list):
                        for skill in parsed_skills:
                            location_skill_counts[str(skill)] = location_skill_counts.get(str(skill), 0) + 1
                top_location_skills = pd.Series(location_skill_counts).nlargest(10)
                if top_location_skills.empty:
                    st.info("Skill breakdown unavailable.")
                else:
                    st.dataframe(top_location_skills.rename_axis("Skill").reset_index(name="Listings"), width="stretch", hide_index=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="page-footer"><span>JobInsight</span>'
    '<span>Dataset-backed analysis</span></div>',
    unsafe_allow_html=True
)