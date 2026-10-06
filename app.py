import streamlit as st
import tempfile
import os

from utils.resume_parser import extract_resume_text
from utils.analyzer import analyze_resume


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume and get an AI-powered resume analysis "
    "without using an API key."
)

st.divider()


# Resume upload
uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"]
)


# Job role selection
job_role = st.selectbox(
    "Select Target Job Role",
    [
        "Python Developer",
        "Java Developer",
        "Web Developer",
        "Data Scientist",
        "AI/ML Engineer",
        "Software Developer"
    ]
)


if uploaded_file is not None:

    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )


    if st.button("🔍 Analyze Resume"):

        with st.spinner("Analyzing your resume..."):

            file_extension = os.path.splitext(
                uploaded_file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_path = temp_file.name


            try:

                # Extract resume text
                resume_text = extract_resume_text(
                    temp_path
                )

                if not resume_text.strip():

                    st.error(
                        "Could not extract text from this resume."
                    )

                else:

                    # Analyze resume
                    result = analyze_resume(
                        resume_text,
                        job_role
                    )


                    st.divider()

                    st.header("📊 Resume Analysis")


                    # Score section
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Overall Score",
                            f"{result['score']}/100"
                        )

                    with col2:
                        st.metric(
                            "Job Match",
                            f"{result['match']}%"
                        )

                    with col3:
                        st.metric(
                            "ATS Score",
                            f"{result['ats_score']}%"
                        )


                    st.divider()


                    # Skills
                    st.subheader("🛠️ Detected Skills")

                    if result["skills"]:

                        st.write(
                            ", ".join(result["skills"])
                        )

                    else:

                        st.write(
                            "No relevant skills detected."
                        )


                    # Missing skills
                    st.subheader("❌ Missing Skills")

                    if result["missing_skills"]:

                        for skill in result["missing_skills"]:
                            st.write(f"• {skill}")

                    else:

                        st.write(
                            "No major missing skills detected."
                        )


                    # Strengths
                    st.subheader("💪 Strengths")

                    if result["strengths"]:

                        for item in result["strengths"]:
                            st.write(f"✅ {item}")

                    else:

                        st.write(
                            "No specific strengths detected."
                        )


                    # Weaknesses
                    st.subheader("⚠️ Areas to Improve")

                    if result["weaknesses"]:

                        for item in result["weaknesses"]:
                            st.write(f"• {item}")

                    else:

                        st.write(
                            "No major weaknesses detected."
                        )


                    # Suggestions
                    st.subheader("💡 Suggestions")

                    if result["suggestions"]:

                        for item in result["suggestions"]:
                            st.write(f"💡 {item}")

                    else:

                        st.write(
                            "Your resume looks good!"
                        )


                    # Extracted text
                    with st.expander(
                        "📃 View Extracted Resume Text"
                    ):

                        st.text(resume_text)


            finally:

                if os.path.exists(temp_path):
                    os.remove(temp_path)