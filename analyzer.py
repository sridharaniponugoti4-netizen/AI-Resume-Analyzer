import re
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


JOB_SKILLS = {
    "Python Developer": [
        "python", "sql", "git", "github", "django",
        "flask", "rest api", "pandas", "numpy"
    ],
    "Java Developer": [
        "java", "sql", "git", "github", "spring",
        "spring boot", "hibernate", "rest api"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react",
        "git", "github", "rest api", "sql"
    ],
    "Data Scientist": [
        "python", "sql", "machine learning",
        "pandas", "numpy", "matplotlib",
        "scikit-learn", "statistics"
    ],
    "AI/ML Engineer": [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch", "numpy",
        "pandas", "scikit-learn"
    ],
    "Software Developer": [
        "python", "java", "c++", "sql",
        "git", "github", "data structures",
        "algorithms", "oops"
    ]
}


def clean_text(text):
    return re.sub(r"\s+", " ", text.lower())


def find_skills(resume_text, skills):
    resume_text = clean_text(resume_text)

    return [
        skill for skill in skills
        if skill.lower() in resume_text
    ]


def calculate_job_match(resume_text, job_role):
    skills = JOB_SKILLS.get(
        job_role,
        JOB_SKILLS["Software Developer"]
    )

    found_skills = find_skills(resume_text, skills)

    match_percentage = int(
        (len(found_skills) / len(skills)) * 100
    )

    return match_percentage, found_skills, skills


def calculate_ats_score(resume_text):
    text = clean_text(resume_text)

    keywords = [
        "education",
        "skills",
        "projects",
        "experience",
        "certifications",
        "python",
        "java",
        "sql",
        "github",
        "linkedin"
    ]

    found = sum(
        1 for keyword in keywords
        if keyword in text
    )

    return int((found / len(keywords)) * 100)


def analyze_resume(resume_text, job_role):

    if not resume_text.strip():
        return {
            "score": 0,
            "match": 0,
            "skills": [],
            "missing_skills": [],
            "ats_score": 0,
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }

    match, found_skills, required_skills = calculate_job_match(
        resume_text,
        job_role
    )

    missing_skills = [
        skill for skill in required_skills
        if skill not in found_skills
    ]

    ats_score = calculate_ats_score(resume_text)

    overall_score = int(
        (match * 0.6) + (ats_score * 0.4)
    )

    strengths = []

    if found_skills:
        strengths.append(
            "Relevant technical skills were detected."
        )

    if "projects" in clean_text(resume_text):
        strengths.append(
            "Projects section is present."
        )

    if "education" in clean_text(resume_text):
        strengths.append(
            "Education details are included."
        )

    weaknesses = []

    if not found_skills:
        weaknesses.append(
            "Very few relevant technical skills were detected."
        )

    if "experience" not in clean_text(resume_text):
        weaknesses.append(
            "Work experience section was not detected."
        )

    if ats_score < 60:
        weaknesses.append(
            "The resume could be improved for ATS keyword matching."
        )

    suggestions = []

    if missing_skills:
        suggestions.append(
            "Consider learning or adding relevant skills: "
            + ", ".join(missing_skills)
        )

    if "github" not in clean_text(resume_text):
        suggestions.append(
            "Add your GitHub profile if you have relevant projects."
        )

    if "projects" not in clean_text(resume_text):
        suggestions.append(
            "Add 2–3 relevant projects."
        )

    if "certifications" not in clean_text(resume_text):
        suggestions.append(
            "Add relevant certifications or courses."
        )

    return {
        "score": overall_score,
        "match": match,
        "skills": found_skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }