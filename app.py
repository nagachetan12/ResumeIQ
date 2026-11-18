
import streamlit as st
import fitz
from docx import Document
import re
from pathlib import Path

# =====================================
# resume IQ - PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="resume IQ",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# LOAD CUSTOM CSS
# =====================================

css_path = Path(__file__).parent / "assets" / "style.css"

if css_path.exists():
    css = css_path.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )
else:
    st.warning("CSS file not found. Please check assets/style.css")

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.title("🚀 ResumeIQ")
    st.caption("YOUR AI CAREER COMPANION")
    st.divider()


# =====================================
# RESUMEIQ USER LOGIN & REGISTRATION
# =====================================

import sqlite3
import hashlib
import secrets
import hmac
from pathlib import Path

auth_db_path = (
    Path(__file__).parent
    / "database"
    / "interview_questions.db"
)
from database.setup_database import setup_database

setup_database()
import runpy

connection = sqlite3.connect(auth_db_path)
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM career_roles")
role_count = cursor.fetchone()[0]

connection.close()

if role_count == 0:
    runpy.run_path(
        str(
            Path(__file__).parent
            / "database"
            / "populate_database.py"
        )
    )
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if not st.session_state["logged_in"]:

    st.title("🔐 Welcome to ResumeIQ")

    st.write("Login or create an account to access your career dashboard.")

    login_tab, register_tab = st.tabs(
        ["🔑 Login", "📝 Create Account"]
    )

    with register_tab:

        st.subheader("Create Your ResumeIQ Account")

        with st.form("registration_form"):

            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email Address")
            new_password = st.text_input(
                "Password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            register_button = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

        if register_button:

            if not new_name.strip() or not new_email.strip():
                st.error("Please enter your name and email.")

            elif "@" not in new_email or "." not in new_email:
                st.error("Please enter a valid email address.")

            elif len(new_password) < 8:
                st.error("Password must contain at least 8 characters.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:
                salt = secrets.token_hex(16)

                password_hash = hashlib.pbkdf2_hmac(
                    "sha256",
                    new_password.encode("utf-8"),
                    salt.encode("utf-8"),
                    200000
                ).hex()

                stored_password = salt + "$" + password_hash

                try:
                    connection = sqlite3.connect(auth_db_path)
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        INSERT INTO users
                        (full_name, email, password_hash)
                        VALUES (?, ?, ?)
                        """,
                        (
                            new_name.strip(),
                            new_email.strip().lower(),
                            stored_password
                        )
                    )

                    connection.commit()
                    connection.close()

                    st.success(
                        "Account created successfully! "
                        "Please log in."
                    )

                except sqlite3.IntegrityError:
                    st.error("An account with this email already exists.")

                except sqlite3.Error as error:
                    st.error(f"Registration error: {error}")

    with login_tab:

        st.subheader("Login to ResumeIQ")

        with st.form("login_form"):

            login_email = st.text_input("Email Address")

            login_password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_button:

            try:
                connection = sqlite3.connect(auth_db_path)
                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT id, full_name, password_hash
                    FROM users
                    WHERE email = ?
                    """,
                    (login_email.strip().lower(),)
                )

                user = cursor.fetchone()
                connection.close()

                if user:

                    user_id, full_name, stored_password = user

                    salt, saved_hash = stored_password.split("$", 1)

                    entered_hash = hashlib.pbkdf2_hmac(
                        "sha256",
                        login_password.encode("utf-8"),
                        salt.encode("utf-8"),
                        200000
                    ).hex()

                    if hmac.compare_digest(entered_hash, saved_hash):

                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = user_id
                        st.session_state["user_name"] = full_name

                        st.success("Login successful!")
                        st.rerun()

                    else:
                        st.error("Incorrect email or password.")

                else:
                    st.error("Incorrect email or password.")

            except (sqlite3.Error, ValueError):
                st.error("Login failed. Please try again.")

    st.stop()

# RESUMEIQ USER PROFILE

if st.session_state.get("logged_in"):

    st.sidebar.success(
        f"Welcome, {st.session_state.get('user_name', 'User')}!"
    )

    if st.sidebar.button("🚪 Logout", use_container_width=True):

        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state.pop("user_name", None)

        st.rerun()
    
page = st.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "Resume Analyzer",
        "AI Resume Doctor",
        "AI Resume Builder",
        "Skill Gap & Roadmap",
        "Interview Preparation",
        "Job Finder",
        "Resume History"
    ]
)


st.divider()
st.caption("resume IQ | Version 2.0")

# =====================================
# DASHBOARD
# =====================================



if page == "Dashboard":

    st.title("Welcome to ResumeIQ 👋")

    st.subheader("Your AI-Powered Career Assistant")

    st.write(
        "Build a stronger resume, improve your skills, "
        "prepare for interviews and discover career opportunities."
    )

    st.divider()

    # LIVE PROJECT STATISTICS

    col1, col2, col3 = st.columns(3)

    with col1:
        resume_score = st.session_state.get("resume_score")

        score_display = (
            f"{resume_score}/100"
            if resume_score is not None else "--"
        )

        st.metric("Resume Score", score_display)

    with col2:
        st.metric(
            "Skills Identified",
            st.session_state.get("skills_count", 0)
        )

    with col3:
        interview_questions = st.session_state.get(
            "interview_questions", []
        )

        st.metric(
            "Interview Questions",
            len(interview_questions)
        )

    st.divider()

    # CAREER PROFILE

    st.subheader("👤 Your Career Profile")

    career_options = [
        "Python Developer",
        "Data Scientist",
        "Web Developer",
        "Data Analyst",
        "AI / ML Engineer"
    ]

    current_career = st.session_state.get(
        "selected_career",
        st.session_state.get(
            "roadmap_career",
            st.session_state.get(
                "interview_career",
                "Python Developer"
            )
        )
    )

    if current_career not in career_options:
        current_career = "Python Developer"

    if "dashboard_career" not in st.session_state:
        st.session_state["dashboard_career"] = current_career

    career = st.selectbox(
        "🎯 Select Your Career Goal",
        career_options,
        key="dashboard_career"
    )

    # SHARE SELECTED CAREER WITH OTHER MODULES

    st.session_state["selected_career"] = career
    st.session_state["roadmap_career"] = career
    st.session_state["interview_career"] = career

    resume_status = (
        "Uploaded"
        if st.session_state.get("resume_text")
        else "Not uploaded"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"🎯 **Career Goal:** {career}")

    with col2:
        st.info(f"📄 **Resume Status:** {resume_status}")

    st.success(
        f"Your ResumeIQ career goal is set to {career}!"
    )

    # CAREER TOOLS

    st.divider()

    st.subheader("🚀 Explore Your Career Tools")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "📄 **Resume Analyzer**\n\n"
            "Analyze your resume and check ATS compatibility."
        )

        st.info(
            "🩺 **AI Resume Doctor**\n\n"
            "Discover ways to improve your resume."
        )

        st.info(
            "🎯 **Skill Gap & Roadmap**\n\n"
            "Identify missing skills and plan your career."
        )

        st.info(
            "✨ **AI Resume Builder**\n\n"
            "Create a professional resume with customizable templates."
        )

    with col2:
        st.info(
            "🎤 **Interview Preparation**\n\n"
            "Practice interview questions and take quizzes."
        )

        st.info(
            "💼 **Job Finder**\n\n"
            "Explore career opportunities and track applications."
        )

        st.info(
            "📂 **Resume History**\n\n"
            "Review your previously uploaded resumes."
        )

    st.divider()

    st.caption(
        "ResumeIQ | Your Career. Your Future. 🚀"
    )


# =====================================
# RESUME ANALYZER
# =====================================



elif page == "Resume Analyzer":

    st.title("📄 Resume Analyzer")
    st.write("Upload your resume to get an ATS-style analysis.")

    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"],
        key="resume_uploader"
    )

    if uploaded_file:
        if uploaded_file.name.lower().endswith(".pdf"):
            pdf = fitz.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            )
            resume_text = "\n".join(
                page.get_text("text") for page in pdf
            )
            pdf.close()
        else:
            doc = Document(uploaded_file)
            paragraphs = [p.text for p in doc.paragraphs]
            table_text = [
                cell.text
                for table in doc.tables
                for row in table.rows
                for cell in row.cells
            ]
            resume_text = "\n".join(paragraphs + table_text)

        
        if resume_text.strip():
            st.session_state["resume_text"] = resume_text
            st.session_state["resume_filename"] = uploaded_file.name
            st.success("Resume uploaded and text extracted!")

            import sqlite3
            from pathlib import Path

            db_path = (
                Path(__file__).parent
                / "database"
                / "interview_questions.db"
            )

            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_filename TEXT NOT NULL,
        ats_score INTEGER,
        skills_count INTEGER,
        resume_text TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
            connection.commit()

            cursor.execute(
                """
                INSERT INTO resume_history
                (resume_filename, resume_text)
                VALUES (?, ?)
                """,
                (uploaded_file.name, resume_text)
            )

            connection.commit()
            connection.close()

        else:
            st.warning("No readable text found. Try another PDF or DOCX file.")
            resume_text = ""

    else:
        resume_text = st.session_state.get("resume_text", "")

        if resume_text:
            st.success("Your previous resume is still saved in this session.")
            st.write(
                "Previously uploaded:",
                st.session_state.get("resume_filename", "Resume")
            )

    if resume_text.strip():

        st.success(
            f"Resume loaded: {st.session_state.get('resume_filename', 'Saved resume')}"
        )

        skills = [
            "python", "java", "html", "css", "javascript",
            "sql", "machine learning", "communication",
            "teamwork", "excel", "react", "data analysis"
        ]

        found = [s for s in skills if s in resume_text.lower()]
        missing = [s for s in skills if s not in resume_text.lower()]

        sections = [
            "education", "experience", "skills",
            "projects", "certifications"
        ]

        present = [
            s for s in sections if s in resume_text.lower()
        ]

        score = min(100, len(found) * 5 + len(present) * 8)

        st.session_state["resume_score"] = score
        st.session_state["skills_count"] = len(found)

        import sqlite3
        from pathlib import Path

        db_path = (
            Path(__file__).parent
            / "database"
            / "interview_questions.db"
        )

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE resume_history
            SET ats_score = ?, skills_count = ?
            WHERE id = (
                SELECT MAX(id)
                FROM resume_history
            )
            """,
            (score, len(found))
        )

        connection.commit()
        connection.close()


        st.subheader("📊 Resume Analysis")

        st.metric("ATS-style Score", f"{score}/100")
        st.metric("Skills Found", len(found))
        st.metric("Sections Found", len(present))

        st.subheader("✅ Skills Identified")

        if found:
            st.success(" | ".join(found))
        else:
            st.info("No listed skills found.")

        st.subheader("🎯 Skills to Consider Adding")

        if missing:
            st.warning(" | ".join(missing))
        else:
            st.success("Great! No missing skills from our checklist.")

        st.subheader("📁 Resume Sections")

        st.write(
            ", ".join(present)
            if present else "No standard sections detected."
        )

        st.info(
            "This is an educational ATS-style score, "
            "not a score from an actual employer's ATS."
        )

        st.subheader("🎯 Job Description Matching")

        job_description = st.text_area(
            "Paste the job description here",
            height=180,
            key="job_description"
        )

        match_score = None
        matched = []
        missing_keywords = []

        if st.button("Compare Resume with Job"):

            if job_description.strip():

                stop_words = {
                    "a", "an", "the", "and", "or", "to", "of",
                    "in", "for", "with", "is", "are", "be",
                    "we", "our", "you", "your", "this", "that",
                    "on", "at", "as"
                }

                resume_words = set(
                    re.findall(
                        r"\b[a-z][a-z+#.]*\b",
                        resume_text.lower()
                    )
                ) - stop_words

                job_words = set(
                    re.findall(
                        r"\b[a-z][a-z+#.]*\b",
                        job_description.lower()
                    )
                ) - stop_words

                matched = sorted(resume_words & job_words)
                missing_keywords = sorted(job_words - resume_words)

                match_score = round(
                    len(matched) / max(len(job_words), 1) * 100
                )

                st.session_state["match_score"] = match_score
                st.session_state["matched_keywords"] = matched
                st.session_state["missing_keywords"] = missing_keywords

                st.metric(
                    "Job Description Match",
                    f"{match_score}%"
                )

                st.write("Matching keywords:", ", ".join(matched[:40]))
                st.write(
                    "Missing keywords:",
                    ", ".join(missing_keywords[:40])
                )

            else:
                st.warning("Please paste a job description first.")

        # DOWNLOAD REPORT

        st.divider()
        st.subheader("📥 Download Your Resume Report")

        report = f"""
RESUMEIQ - RESUME ANALYSIS REPORT
=================================

Resume: {st.session_state.get('resume_filename', 'Resume')}

ATS-STYLE SCORE: {score}/100

SKILLS IDENTIFIED:
{', '.join(found) if found else 'None'}

SKILLS TO CONSIDER ADDING:
{', '.join(missing) if missing else 'None'}

RESUME SECTIONS DETECTED:
{', '.join(present) if present else 'None'}

JOB DESCRIPTION MATCH:
{st.session_state.get('match_score', 'Not calculated')}{'%' if st.session_state.get('match_score') is not None else ''}

MATCHING KEYWORDS:
{', '.join(st.session_state.get('matched_keywords', []))}

MISSING JOB KEYWORDS:
{', '.join(st.session_state.get('missing_keywords', []))}

=================================
Generated by ResumeIQ
Educational ATS-style analysis only.
"""

        st.download_button(
            label="📄 Download Resume Analysis Report",
            data=report,
            file_name="ResumeIQ_Analysis_Report.txt",
            mime="text/plain"
        )

    else:
        st.info("Upload your resume to begin analysis.")
 
        
# =====================================
# AI RESUME DOCTOR
# =====================================




elif page == "AI Resume Doctor":

    import re

    st.title("🩺 AI Resume Doctor")
    st.write("Improve your resume with professional suggestions and rewriting.")

    if "doctor_resume_input" not in st.session_state:
        st.session_state["doctor_resume_input"] = st.session_state.get(
            "resume_text", ""
        )

    resume_text = st.text_area(
        "Paste your resume content",
        height=200,
        placeholder="Your extracted resume will appear here...",
        key="doctor_resume_input"
    )

    if resume_text.strip():
        st.session_state["resume_text"] = resume_text

        text = resume_text.strip()
        words = text.split()
        suggestions = []

        # RESUME REVIEW

        required_sections = {
            "Professional Summary": ["summary", "professional summary"],
            "Technical Skills": ["technical skills", "skills"],
            "Projects": ["projects", "project"],
            "Education": ["education"],
            "Certifications": ["certifications", "certificates"]
        }

        for section, keywords in required_sections.items():
            if not any(keyword in text.lower() for keyword in keywords):
                suggestions.append(
                    f"Consider adding a {section} section."
                )

        if len(words) < 50:
            suggestions.append(
                "Add more details about your education, skills, projects and experience."
            )

        if "python" in text.lower():
            suggestions.append(
                "Mention specific Python libraries or tools you have used."
            )

        if "project" in text.lower():
            suggestions.append(
                "Explain what your project does, which technologies you used, and your contribution."
            )

        if not any(char.isdigit() for char in text):
            suggestions.append(
                "Add measurable achievements or project results where possible."
            )

        suggestions.append(
            "Use strong action words such as Developed, Created, Designed and Implemented."
        )

        suggestions.append(
            "Organize your resume into Summary, Skills, Education and Projects sections."
        )

        st.session_state["doctor_suggestions"] = suggestions

        # PROFESSIONAL RESUME REWRITING

        st.divider()
        st.subheader("✨ Professional Resume Rewriting")

        replacements = {
            r"\bresponsible for\b": "Managed",
            r"\bworked on\b": "Contributed to",
            r"\bhelped with\b": "Supported",
            r"\bhelped\b": "Assisted with",
            r"\bmade\b": "Created",
            r"\bdid\b": "Performed",
            r"\bused\b": "Applied",
            r"\bworked with\b": "Collaborated with",
            r"\binvolved in\b": "Contributed to",
            r"\bgot\b": "Achieved",
            r"\bhandled\b": "Managed",
            r"\bwas in charge of\b": "Led"
        }

        def rewrite_resume_line(line):
            original = line.strip()

            if not original:
                return line

            # Preserve section headings
            if original.isupper() or original.endswith(":"):
                return line

            # Rewrite bullet points and action statements
            bullet = ""
            content = original

            if content.startswith(("-", "•", "*")):
                bullet = content[0] + " "
                content = content[1:].strip()

            rewritten = content

            for pattern, replacement in replacements.items():
                rewritten = re.sub(
                    pattern,
                    replacement,
                    rewritten,
                    flags=re.IGNORECASE
                )

            return bullet + rewritten

        improved_lines = [
            rewrite_resume_line(line)
            for line in text.splitlines()
        ]

        improved_resume = "\n".join(improved_lines)

        st.info(
            "Review the rewritten content carefully. "
            "This assistant improves wording while preserving your original information. "
            "It does not invent qualifications or achievements."
        )

        improved_resume = st.text_area(
            "Your improved resume (editable)",
            value=improved_resume,
            height=350,
            key="doctor_rewritten_resume"
        )

        st.download_button(
            label="📥 Download Improved Resume",
            data=improved_resume,
            file_name="ResumeIQ_Improved_Resume.txt",
            mime="text/plain"
        )

    else:
        suggestions = []
        st.info(
            "Upload your resume in Resume Analyzer or paste your resume here."
        )

    # IMPROVEMENT SUGGESTIONS

    if suggestions:

        st.divider()
        st.subheader("✨ Resume Improvement Suggestions")

        for i, suggestion in enumerate(suggestions, 1):
            st.write(f"**{i}.** {suggestion}")

        st.success("Your resume review is complete!")

        st.divider()
        st.subheader("📥 Download Your Improvement Report")

        report = f"""
RESUMEIQ - AI RESUME DOCTOR REPORT
=================================

RESUME: {st.session_state.get('resume_filename', 'Resume')}

IMPROVEMENT SUGGESTIONS:

{chr(10).join(
    f"{i}. {suggestion}"
    for i, suggestion in enumerate(suggestions, 1)
)}

=================================
Generated by ResumeIQ
Educational resume improvement suggestions.
"""

        st.download_button(
            label="📄 Download AI Resume Doctor Report",
            data=report,
            file_name="ResumeIQ_Improvement_Report.txt",
            mime="text/plain"
        )

elif page == "AI Resume Builder":

    import io
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor

    st.title("🚀 AI Resume Builder")
    st.write(
        "Create a professional resume by entering your details "
        "and choosing your preferred design."
    )

    st.divider()

    # TEMPLATE SELECTION

    st.subheader("🎨 Choose Your Resume Template")

    template = st.selectbox(
        "Select a design",
        ["Modern", "Classic", "Minimal"],
        key="builder_template"
    )

    # PERSONAL INFORMATION

    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")

    with col2:
        location = st.text_input("Location")
        linkedin = st.text_input("LinkedIn Profile")
        github = st.text_input("GitHub / Portfolio")

    summary = st.text_area(
    "Professional Summary",
    value=st.session_state.get("builder_summary", ""),
    placeholder="Write a short introduction about yourself...",
    key="builder_summary_input"
)

    # EDUCATION

    st.divider()
    st.subheader("🎓 Education")

    education = st.text_area(
        "Education Details",
        placeholder="Degree, college, graduation year, marks or CGPA..."
    )

    # SKILLS

    st.divider()
    st.subheader("💻 Skills")

    skills = st.text_area(
        "Your Skills",
        placeholder="Python, SQL, HTML, CSS, Machine Learning..."
    )

    # EXPERIENCE

    st.divider()
    st.subheader("💼 Work Experience")

    experience = st.text_area(
        "Experience Details",
        placeholder="Job title, company, duration and responsibilities..."
    )

    # PROJECTS

    st.divider()
    st.subheader("🛠️ Projects")

    projects = st.text_area(
        "Your Projects",
        placeholder="Project name, technologies used and your contribution..."
    )

    # CERTIFICATIONS

    st.divider()
    st.subheader("📜 Certifications")

    certifications = st.text_area(
        "Your Certifications",
        placeholder="Certification name and issuing organization..."
    )

    # AI-STYLE PROFESSIONAL SUMMARY GENERATOR

    st.divider()
    st.subheader("✨ Professional Summary Generator")

    if st.button("🤖 Generate Professional Summary"):

        summary_parts = []

        if skills.strip():
            skill_list = [
                skill.strip()
                for skill in skills.replace("\n", ",").split(",")
                if skill.strip()
            ]

            summary_parts.append(
                "Skilled in " + ", ".join(skill_list[:6])
            )

        if education.strip():
            summary_parts.append(
                "with an educational background in " +
                education.split("\n")[0]
            )

        if projects.strip():
            summary_parts.append(
                "with practical project experience in " +
                projects.split("\n")[0]
            )

        if experience.strip():
            summary_parts.append(
                "and experience in " +
                experience.split("\n")[0]
            )

        if summary_parts:
            generated_summary = (
                full_name + " is a motivated professional " +
                " ".join(summary_parts) +
                ". Passionate about learning, problem-solving, "
                "and contributing to meaningful projects."
            )

            st.session_state["generated_professional_summary"] = (
                generated_summary
            )
        else:
            st.warning(
                "Please enter your skills, education, projects, "
                "or experience first."
            )

    if st.session_state.get("generated_professional_summary"):

        generated_summary = st.text_area(
            "Generated Professional Summary (You can edit it)",
            value=st.session_state["generated_professional_summary"],
            height=150,
            key="editable_generated_summary"
        )

        if st.button("✅ Use This Summary"):
            st.session_state["builder_summary"] = generated_summary
            st.success("Professional summary saved!")

    # ATS KEYWORD OPTIMIZER

    st.divider()
    st.subheader("🎯 ATS Keyword Optimizer")

    job_description = st.text_area(
        "Paste the target job description",
        placeholder="Paste the job description here...",
        height=180,
        key="builder_job_description"
    )

    if st.button("🔍 Analyze ATS Keywords"):

        if not job_description.strip():
            st.warning("Please paste a job description first.")

        else:
            import re

            resume_content = " ".join([
                full_name,
                summary,
                education,
                skills,
                experience,
                projects,
                certifications
            ]).lower()

            job_content = job_description.lower()

            stop_words = {
                "the", "and", "for", "with", "you", "your",
                "are", "our", "will", "this", "that", "from",
                "have", "has", "who", "what", "their", "they",
                "about", "into", "using", "such", "must",
                "work", "working", "role", "job", "team",
                "years", "year", "experience", "skills",
                "ability", "strong", "good", "excellent"
            }

            job_keywords = set(
                re.findall(r"\b[a-zA-Z][a-zA-Z+#.]{1,}\b", job_content)
            )

            job_keywords = {
                word for word in job_keywords
                if word not in stop_words and len(word) > 2
            }

            resume_words = set(
                re.findall(r"\b[a-zA-Z][a-zA-Z+#.]{1,}\b", resume_content)
            )

            matched_keywords = sorted(
                job_keywords.intersection(resume_words)
            )

            missing_keywords = sorted(
                job_keywords.difference(resume_words)
            )

            total_keywords = len(job_keywords)

            ats_score = (
                round(len(matched_keywords) / total_keywords * 100)
                if total_keywords else 0
            )

            st.session_state["builder_ats_score"] = ats_score
            st.session_state["builder_matched_keywords"] = matched_keywords
            st.session_state["builder_missing_keywords"] = missing_keywords

    if "builder_ats_score" in st.session_state:

        ats_score = st.session_state["builder_ats_score"]
        matched_keywords = st.session_state["builder_matched_keywords"]
        missing_keywords = st.session_state["builder_missing_keywords"]

        st.divider()
        st.subheader("📊 ATS Analysis Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("ATS Keyword Score", f"{ats_score}%")
        col2.metric("Matched Keywords", len(matched_keywords))
        col3.metric("Missing Keywords", len(missing_keywords))

        st.progress(ats_score / 100)

        st.subheader("✅ Matching Keywords")

        if matched_keywords:
            st.write(", ".join(matched_keywords))
        else:
            st.info("No matching keywords found.")

        st.subheader("⚠️ Missing Keywords")

        if missing_keywords:
            st.write(", ".join(missing_keywords))
            st.info(
                "Add relevant missing skills only if you genuinely "
                "have those skills or experience."
            )
        else:
            st.success("All extracted keywords are present!")

        ats_report = f"""
RESUMEIQ - ATS KEYWORD ANALYSIS
================================

ATS KEYWORD SCORE: {ats_score}%

MATCHED KEYWORDS:
{", ".join(matched_keywords)}

MISSING KEYWORDS:
{", ".join(missing_keywords)}

================================
Generated by ResumeIQ
"""

        st.download_button(
            "📥 Download ATS Analysis Report",
            data=ats_report,
            file_name="ResumeIQ_ATS_Report.txt",
            mime="text/plain"
        )

    # AI ACHIEVEMENT ENHANCER

    st.divider()
    st.subheader("🏆 AI Achievement Enhancer")

    achievement_input = st.text_area(
        "Enter your resume achievement or work description",
        placeholder="Example: Worked on a Python project and made a website...",
        height=120,
        key="achievement_input"
    )

    if st.button("✨ Enhance My Achievement"):

        if not achievement_input.strip():
            st.warning("Please enter a description first.")

        else:
            import re

            replacements = {
                r"\bworked on\b": "Contributed to the development of",
                r"\bhelped\b": "Supported",
                r"\bmade\b": "Created",
                r"\bdid\b": "Performed",
                r"\bused\b": "Applied",
                r"\bresponsible for\b": "Managed",
                r"\bhandled\b": "Managed",
                r"\bparticipated in\b": "Contributed to",
                r"\blearned\b": "Developed knowledge of",
                r"\bcreated\b": "Developed",
                r"\bimproved\b": "Enhanced"
            }

            enhanced = achievement_input.strip()

            for pattern, replacement in replacements.items():
                enhanced = re.sub(
                    pattern,
                    replacement,
                    enhanced,
                    flags=re.IGNORECASE
                )

            if enhanced and enhanced[-1] not in ".!?":
                enhanced += "."

            st.session_state["enhanced_achievement"] = enhanced

    if st.session_state.get("enhanced_achievement"):

        enhanced = st.text_area(
            "Enhanced Achievement (Editable)",
            value=st.session_state["enhanced_achievement"],
            height=120,
            key="editable_achievement"
        )

        st.download_button(
            "📥 Download Enhanced Achievement",
            data=enhanced,
            file_name="ResumeIQ_Enhanced_Achievement.txt",
            mime="text/plain"
        )

        st.caption(
            "Review the wording before using it. Add real results or "
            "numbers only when they reflect your actual experience."
        )

    # JOB-SPECIFIC RESUME TAILORING

    st.divider()
    st.subheader("🎯 Job-Specific Resume Tailoring")

    if st.button("✨ Tailor My Resume for This Job"):

        job_description = st.session_state.get(
            "builder_job_description", ""
        )

        if not job_description.strip():
            st.warning(
                "Please paste a job description in the ATS Keyword Optimizer first."
            )

        else:
            import re

            resume_content = " ".join([
                summary,
                skills,
                education,
                experience,
                projects,
                certifications
            ])

            job_words = set(
                re.findall(
                    r"\b[a-zA-Z][a-zA-Z+#.]{1,}\b",
                    job_description.lower()
                )
            )

            resume_words = set(
                re.findall(
                    r"\b[a-zA-Z][a-zA-Z+#.]{1,}\b",
                    resume_content.lower()
                )
            )

            stop_words = {
                "the", "and", "for", "with", "you", "your",
                "are", "our", "will", "this", "that", "from",
                "have", "has", "who", "their", "they", "about",
                "into", "using", "such", "must", "work", "working",
                "role", "job", "team", "years", "year", "experience",
                "skills", "ability", "strong", "good", "excellent"
            }

            relevant_keywords = sorted(
                word for word in job_words
                if word in resume_words and word not in stop_words
            )

            tailored_summary = (
                f"{full_name} is a motivated candidate"
            )

            if relevant_keywords:
                tailored_summary += (
                    " with knowledge of "
                    + ", ".join(relevant_keywords[:8])
                )

            if experience.strip():
                tailored_summary += (
                    ". Brings practical experience in "
                    + experience.split("\n")[0]
                )

            elif projects.strip():
                tailored_summary += (
                    ". Has practical project exposure through "
                    + projects.split("\n")[0]
                )

            tailored_summary += (
                ". Interested in applying these skills "
                "to contribute to the target role."
            )

            tailored_resume = (
                f"JOB-SPECIFIC RESUME\n"
                f"{'=' * 40}\n\n"
                f"NAME: {full_name}\n"
                f"EMAIL: {email}\n"
                f"PHONE: {phone}\n"
                f"LOCATION: {location}\n\n"
                f"PROFESSIONAL SUMMARY\n"
                f"{tailored_summary}\n\n"
                f"EDUCATION\n{education}\n\n"
                f"SKILLS\n{skills}\n\n"
                f"EXPERIENCE\n{experience}\n\n"
                f"PROJECTS\n{projects}\n\n"
                f"CERTIFICATIONS\n{certifications}\n\n"
                f"RELEVANT MATCHING KEYWORDS\n"
                f"{', '.join(relevant_keywords)}\n"
            )

            st.session_state["tailored_resume"] = tailored_resume
            st.success("Your job-focused resume draft is ready!")

    if st.session_state.get("tailored_resume"):

        st.text_area(
            "Tailored Resume Draft",
            value=st.session_state["tailored_resume"],
            height=350,
            key="tailored_resume_preview"
        )

        st.download_button(
            "📥 Download Tailored Resume",
            data=st.session_state["tailored_resume"],
            file_name="ResumeIQ_Tailored_Resume.txt",
            mime="text/plain"
        )

        st.caption(
            "Review the draft carefully. Only include skills and "
            "experience that genuinely reflect your background."
        )

    # GENERATE RESUME

    st.divider()

    if st.button("✨ Generate My Resume", type="primary"):

        if not full_name.strip():
            st.error("Please enter your full name.")

        elif not email.strip():
            st.error("Please enter your email address.")

        else:
            resume_data = {
                "Name": full_name,
                "Email": email,
                "Phone": phone,
                "Location": location,
                "LinkedIn": linkedin,
                "GitHub": github,
                "Summary": summary,
                "Education": education,
                "Skills": skills,
                "Experience": experience,
                "Projects": projects,
                "Certifications": certifications
            }

            st.session_state["builder_resume_data"] = resume_data
            st.session_state["builder_template_selected"] = template

            st.success("Your resume has been generated!")

    # PREVIEW AND DOWNLOAD

    if st.session_state.get("builder_resume_data"):

        data = st.session_state["builder_resume_data"]
        selected_template = st.session_state.get(
            "builder_template_selected", "Modern"
        )

        st.divider()
        st.subheader("📄 Resume Preview")

        if selected_template == "Modern":
            st.markdown(
                "<h2 style='color:#00cfff;'>"
                + data["Name"]
                + "</h2>",
                unsafe_allow_html=True
            )

        elif selected_template == "Classic":
            st.markdown(
                "<h2 style='text-align:center;'>"
                + data["Name"]
                + "</h2>",
                unsafe_allow_html=True
            )

        else:
            st.markdown("## " + data["Name"])

        contact = " | ".join(
            value for value in [
                data["Email"],
                data["Phone"],
                data["Location"]
            ] if value.strip()
        )

        st.write(contact)

        if data["LinkedIn"]:
            st.write("LinkedIn:", data["LinkedIn"])

        if data["GitHub"]:
            st.write("Portfolio:", data["GitHub"])

        preview_sections = [
            ("PROFESSIONAL SUMMARY", "Summary"),
            ("EDUCATION", "Education"),
            ("SKILLS", "Skills"),
            ("WORK EXPERIENCE", "Experience"),
            ("PROJECTS", "Projects"),
            ("CERTIFICATIONS", "Certifications")
        ]

        for heading, key in preview_sections:
            if data[key].strip():
                st.markdown(f"### {heading}")
                st.write(data[key])

        # CREATE WORD DOCUMENT

        document = Document()

        section = document.sections[0]
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

        title = document.add_heading(data["Name"], 0)
        title.alignment = 1 if selected_template == "Classic" else 0

        if selected_template == "Modern":
            for run in title.runs:
                run.font.color.rgb = RGBColor(0, 150, 200)

        contact_details = [
            data["Email"],
            data["Phone"],
            data["Location"]
        ]

        contact_line = " | ".join(
            item for item in contact_details if item.strip()
        )

        if contact_line:
            document.add_paragraph(contact_line)

        if data["LinkedIn"]:
            document.add_paragraph("LinkedIn: " + data["LinkedIn"])

        if data["GitHub"]:
            document.add_paragraph("Portfolio: " + data["GitHub"])

        for heading, key in preview_sections:

            if data[key].strip():

                document.add_heading(heading, level=1)

                paragraph = document.add_paragraph(data[key])

                for run in paragraph.runs:
                    run.font.size = Pt(10)

        # DOWNLOAD

        file_buffer = io.BytesIO()
        document.save(file_buffer)
        file_buffer.seek(0)

        st.download_button(
            label="📥 Download My Resume (Word)",
            data=file_buffer.getvalue(),
            file_name="ResumeIQ_Professional_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# =====================================
# SKILL GAP & ROADMAP
# =====================================


elif page == "Skill Gap & Roadmap":

    import sqlite3
    from pathlib import Path

    st.title("🎯 Skill Gap & Career Roadmap")

    st.write(
        "Choose your career goal and explore personalized "
        "learning resources and practical projects."
    )

    career_options = [
        "Data Scientist",
        "Python Developer",
        "Web Developer",
        "Data Analyst",
        "AI / ML Engineer"
    ]

    career = st.selectbox(
        "Choose your career goal",
        career_options,
        key="roadmap_career"
    )

    st.session_state["selected_career"] = career

    st.success(f"Your selected career goal: {career}")

    db_path = (
        Path(__file__).parent
        / "database"
        / "interview_questions.db"
    )

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM career_roles
            WHERE LOWER(TRIM(role_name)) = LOWER(TRIM(?))
            """,
            (career,)
        )

        role_result = cursor.fetchone()

        if role_result:

            role_id = role_result[0]

            # LEARNING ROADMAP

            st.divider()
            st.subheader("🗺️ Your Personalized Learning Roadmap")

            cursor.execute(
                """
                SELECT skills.id,
                       skills.skill_name,
                       learning_roadmap.learning_order,
                       learning_roadmap.estimated_days
                FROM learning_roadmap
                JOIN skills
                ON learning_roadmap.skill_id = skills.id
                WHERE learning_roadmap.role_id = ?
                ORDER BY learning_roadmap.learning_order
                """,
                (role_id,)
            )

            roadmap = cursor.fetchall()

            if roadmap:

                total_days = sum(item[3] for item in roadmap)

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Total Skills", len(roadmap))

                with col2:
                    st.metric("Estimated Learning Time", f"{total_days} days")

                for number, item in enumerate(roadmap, 1):

                    skill_id, skill, order, days = item

                    with st.expander(
                        f"Step {number}: {skill} — {days} days"
                    ):

                        st.write(f"**Skill:** {skill}")
                        st.write(f"**Estimated time:** {days} days")

                        cursor.execute(
                            """
                            SELECT resource_name,
                                   resource_url,
                                   resource_type
                            FROM learning_resources
                            WHERE skill_id = ?
                            """,
                            (skill_id,)
                        )

                        resources = cursor.fetchall()

                        st.markdown("**📚 Learning Resources**")

                        if resources:
                            for resource in resources:
                                name, url, resource_type = resource

                                st.write(
                                    f"**{name}** ({resource_type})"
                                )
                                st.link_button(
                                    f"Open {name}",
                                    url
                                )
                        else:
                            st.info(
                                "No learning resources available for this skill."
                            )

            else:
                st.warning("No roadmap found for this career.")

            # CAREER PROJECTS

            st.divider()
            st.subheader("🚀 Recommended Career Projects")

            cursor.execute(
                """
                SELECT project_name, description, difficulty
                FROM career_projects
                WHERE role_id = ?
                ORDER BY
                    CASE difficulty
                        WHEN 'Beginner' THEN 1
                        WHEN 'Intermediate' THEN 2
                        WHEN 'Advanced' THEN 3
                        ELSE 4
                    END
                """,
                (role_id,)
            )

            projects = cursor.fetchall()

            if projects:

                for number, project in enumerate(projects, 1):

                    project_name, description, difficulty = project

                    with st.container(border=True):

                        st.subheader(
                            f"💡 Project {number}: {project_name}"
                        )

                        st.write(description)

                        st.caption(
                            f"Difficulty Level: {difficulty}"
                        )

            else:
                st.info(
                    "No project recommendations available for this career."
                )

        else:
            st.warning("Career role not found in the database.")

        connection.close()

    except sqlite3.Error as error:
        st.error(f"Database error: {error}")

# =====================================
# INTERVIEW PREPARATION
# =====================================


elif page == "Interview Preparation":

    import sqlite3
    import random
    from pathlib import Path

    st.title("🎤 Interview Preparation")
    st.write("Practice questions, take quizzes and track your preparation.")

    role_options = [
        "Data Scientist",
        "Python Developer",
        "Web Developer",
        "Data Analyst",
        "AI / ML Engineer"
    ]

    role = st.selectbox(
        "Choose your target career role",
        role_options,
        key="interview_career"
    )

    st.session_state["selected_career"] = role

    db_path = (
        Path(__file__).parent
        / "database"
        / "interview_questions.db"
    )

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM career_roles
            WHERE LOWER(TRIM(role_name)) = LOWER(TRIM(?))
            """,
            (role,)
        )

        role_result = cursor.fetchone()

        if role_result:
            cursor.execute(
                """
                SELECT question, answer, category, difficulty
                FROM interview_questions
                WHERE role_id = ?
                ORDER BY category, difficulty
                """,
                (role_result[0],)
            )

            interview_questions = cursor.fetchall()
            st.session_state["interview_questions"] = interview_questions
            st.session_state["interview_questions_role"] = role

        else:
            interview_questions = []
            st.warning("Role not found in the database.")

        connection.close()

        if role_result and interview_questions:

            # INTERVIEW PREPARATION PROGRESS

            progress_key = f"completed_interview_{role}"

            if progress_key not in st.session_state:
                st.session_state[progress_key] = []

            completed = st.session_state[progress_key]
            total = len(interview_questions)
            completed_count = len(completed)
            remaining = total - completed_count

            st.success(
                f"Found {total} interview questions for {role}!"
            )

            st.subheader("📊 Your Interview Preparation Progress")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Questions", total)
            col2.metric("Completed", completed_count)
            col3.metric("Remaining", remaining)

            progress = completed_count / total if total else 0
            st.progress(progress)
            st.write(f"**Progress: {progress * 100:.1f}%**")

            if completed_count == total:
                st.success("🎉 You completed all practice questions!")

            st.divider()

            # INTERACTIVE INTERVIEW QUIZ

            st.subheader("🧠 Interview Quiz")

            st.write(
                "Test your knowledge with 10 randomly selected "
                "multiple-choice questions."
            )

            quiz_role_key = "interview_quiz_role"

            if st.session_state.get(quiz_role_key) != role:
                st.session_state.pop("interview_quiz", None)
                st.session_state.pop("interview_quiz_result", None)
                st.session_state[quiz_role_key] = role

            if st.button(
                "🎯 Start New Quiz",
                type="primary",
                key="start_interview_quiz"
            ):

                valid_questions = [
                    item for item in interview_questions
                    if item[0] and item[1]
                ]

                if len(valid_questions) < 4:
                    st.warning(
                        "Not enough questions with answers to create a quiz."
                    )

                else:
                    quiz_size = min(10, len(valid_questions))

                    selected_questions = random.sample(
                        valid_questions,
                        quiz_size
                    )

                    quiz = []

                    all_answers = list({
                        item[1].strip()
                        for item in valid_questions
                        if item[1] and item[1].strip()
                    })

                    for question, answer, category, difficulty in selected_questions:

                        distractors = [
                            other for other in all_answers
                            if other != answer.strip()
                        ]

                        distractors = random.sample(
                            distractors,
                            min(3, len(distractors))
                        )

                        options = distractors + [answer.strip()]
                        random.shuffle(options)

                        quiz.append({
                            "question": question,
                            "answer": answer.strip(),
                            "category": category,
                            "difficulty": difficulty,
                            "options": options
                        })

                    st.session_state["interview_quiz"] = quiz
                    st.session_state.pop(
                        "interview_quiz_result", None
                    )

                    st.rerun()

            # DISPLAY QUIZ

            if st.session_state.get("interview_quiz"):

                quiz = st.session_state["interview_quiz"]

                if "interview_quiz_result" not in st.session_state:

                    st.info(
                        f"Your quiz contains {len(quiz)} questions. "
                        "Choose one answer for each question."
                    )

                    with st.form("interview_quiz_form"):

                        quiz_answers = []

                        for index, item in enumerate(quiz):

                            st.markdown(
                                f"**Question {index + 1}: "
                                f"{item['question']}**"
                            )

                            st.caption(
                                f"Category: {item['category']} | "
                                f"Difficulty: {item['difficulty']}"
                            )

                            selected_answer = st.radio(
                                "Choose your answer:",
                                item["options"],
                                index=None,
                                key=f"quiz_answer_{role}_{index}"
                            )

                            quiz_answers.append(selected_answer)

                            st.divider()

                        submitted = st.form_submit_button(
                            "✅ Submit Quiz"
                        )

                    if submitted:

                        if any(answer is None for answer in quiz_answers):
                            st.warning(
                                "Please answer every question before submitting."
                            )

                        else:
                            score = 0
                            results = []

                            for index, item in enumerate(quiz):

                                is_correct = (
                                    quiz_answers[index].strip()
                                    == item["answer"].strip()
                                )

                                if is_correct:
                                    score += 1

                                results.append({
                                    "question": item["question"],
                                    "your_answer": quiz_answers[index],
                                    "correct_answer": item["answer"],
                                    "is_correct": is_correct,
                                    "explanation": item["answer"]
                                })

                            percentage = round(
                                score / len(quiz) * 100
                            )

                            st.session_state[
                                "interview_quiz_result"
                            ] = {
                                "score": score,
                                "total": len(quiz),
                                "percentage": percentage,
                                "results": results
                            }

                            st.rerun()

                # QUIZ RESULTS

                if st.session_state.get("interview_quiz_result"):

                    result = st.session_state[
                        "interview_quiz_result"
                    ]

                    st.divider()
                    st.subheader("🏆 Your Quiz Results")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Correct Answers",
                        result["score"]
                    )

                    col2.metric(
                        "Total Questions",
                        result["total"]
                    )

                    col3.metric(
                        "Your Score",
                        f"{result['percentage']}%"
                    )

                    st.progress(result["percentage"] / 100)

                    if result["percentage"] >= 80:
                        st.success(
                            "Excellent work! You have a strong understanding."
                        )
                    elif result["percentage"] >= 50:
                        st.info(
                            "Good effort! Keep practising to improve."
                        )
                    else:
                        st.warning(
                            "Keep learning and try the quiz again."
                        )

                    st.subheader("📝 Answer Review")

                    for index, item in enumerate(
                        result["results"], 1
                    ):

                        with st.expander(
                            f"Question {index}: "
                            f"{'✅ Correct' if item['is_correct'] else '❌ Incorrect'}"
                        ):

                            st.write("**Question:**")
                            st.write(item["question"])

                            st.write("**Your answer:**")
                            st.write(item["your_answer"])

                            st.write("**Correct answer:**")
                            st.success(item["correct_answer"])

                            st.write("**Explanation:**")
                            st.info(item["explanation"])

                    if st.button(
                        "🔄 Try Another Quiz",
                        key="another_interview_quiz"
                    ):
                        st.session_state.pop(
                            "interview_quiz", None
                        )
                        st.session_state.pop(
                            "interview_quiz_result", None
                        )

                        for index in range(10):
                            key = f"quiz_answer_{role}_{index}"
                            if key in st.session_state:
                                del st.session_state[key]

                        st.rerun()

            st.divider()

            # PRACTICE QUESTIONS

            st.subheader("📚 Practice Interview Questions")

            for number, item in enumerate(interview_questions, 1):

                question, answer, category, difficulty = item

                with st.container(border=True):

                    st.markdown(f"**Q{number}. {question}**")

                    st.caption(
                        f"Category: {category} | Difficulty: {difficulty}"
                    )

                    is_completed = st.checkbox(
                        "Mark as completed",
                        value=number in completed,
                        key=f"interview_done_{role}_{number}"
                    )

                    if is_completed and number not in completed:
                        completed.append(number)

                    elif not is_completed and number in completed:
                        completed.remove(number)

                    with st.expander("Show Answer"):
                        st.info(answer)

            st.session_state[progress_key] = completed

            if st.button("Reset My Progress", key=f"reset_{role}"):

                st.session_state[progress_key] = []

                for number in range(1, total + 1):
                    checkbox_key = f"interview_done_{role}_{number}"

                    if checkbox_key in st.session_state:
                        del st.session_state[checkbox_key]

                st.rerun()

    except sqlite3.Error as error:
        st.error(f"Database error: {error}")


# =====================================
# JOB FINDER
# =====================================




elif page == "Job Finder":

    from urllib.parse import quote_plus
    import sqlite3
    from pathlib import Path
    from datetime import date

    st.title("💼 Job Finder")
    st.write(
        "Discover job opportunities and manage your job applications "
        "in one place."
    )

    db_path = (
        Path(__file__).parent
        / "database"
        / "interview_questions.db"
    )

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # CREATE APPLICATION TRACKER TABLE

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                job_title TEXT NOT NULL,
                location TEXT,
                application_date TEXT,
                status TEXT DEFAULT 'Applied',
                job_link TEXT,
                notes TEXT
            )
        """)

        connection.commit()

        st.divider()
        st.subheader("🔎 Customize Your Job Search")

        keyword = st.selectbox(
            "Choose your target job role",
            [
                "Data Scientist",
                "Python Developer",
                "Web Developer",
                "Data Analyst",
                "AI / ML Engineer"
            ],
            key="job_search_role"
        )

        location = st.text_input(
            "Preferred location",
            placeholder="Example: Bengaluru",
            key="job_search_location"
        )

        experience = st.selectbox(
            "Select your experience level",
            [
                "Fresher / Entry Level",
                "1-3 Years Experience",
                "3-5 Years Experience",
                "5+ Years Experience"
            ],
            key="job_search_experience"
        )

        st.divider()
        st.subheader("📋 Your Job Search Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"💻 **Job Role:** {keyword}")
            st.info(
                f"📍 **Location:** "
                f"{location.strip() or 'Any Location'}"
            )

        with col2:
            st.info(f"⭐ **Experience:** {experience}")

        # PREPARE SEARCH LINKS

        search_keyword = quote_plus(f"{keyword} {experience}")
        search_location = quote_plus(location.strip())

        linkedin_url = (
            "https://www.linkedin.com/jobs/search/"
            f"?keywords={search_keyword}&location={search_location}"
        )

        indeed_url = (
            "https://in.indeed.com/jobs"
            f"?q={search_keyword}&l={search_location}"
        )

        google_url = (
            "https://www.google.com/search"
            f"?q={search_keyword}%20jobs%20in%20{search_location}"
        )

        # SAVE SEARCH HISTORY

        if "job_search_history" not in st.session_state:
            st.session_state["job_search_history"] = []

        st.divider()
        st.subheader("🚀 Explore Job Opportunities")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.link_button(
                "🔵 LinkedIn Jobs",
                linkedin_url,
                use_container_width=True
            )

        with col2:
            st.link_button(
                "🟢 Indeed Jobs",
                indeed_url,
                use_container_width=True
            )

        with col3:
            st.link_button(
                "🔍 Google Jobs",
                google_url,
                use_container_width=True
            )

        if st.button(
            "💾 Save This Job Search",
            use_container_width=True
        ):

            search_record = {
                "role": keyword,
                "location": location.strip() or "Any Location",
                "experience": experience
            }

            if search_record not in st.session_state["job_search_history"]:
                st.session_state["job_search_history"].append(search_record)
                st.success("Your job search has been saved!")
            else:
                st.info("This search is already saved.")

        # SEARCH HISTORY

        st.divider()
        st.subheader("🕘 Your Saved Job Searches")

        history = st.session_state["job_search_history"]

        if history:
            for number, search in enumerate(reversed(history), 1):
                st.write(
                    f"**{number}. {search['role']}**"
                    f" | {search['location']}"
                    f" | {search['experience']}"
                )
        else:
            st.info("Your saved job searches will appear here.")

        # JOB APPLICATION TRACKER

        st.divider()
        st.title("📌 Job Application Tracker")

        st.write(
            "Save the jobs you apply for and monitor your application progress."
        )

        # ADD NEW APPLICATION

        st.subheader("➕ Add a Job Application")

        with st.form("add_job_application_form"):

            company = st.text_input("Company Name")
            job_title = st.text_input("Job Title")
            application_location = st.text_input(
                "Job Location",
                value=location.strip()
            )

            application_date = st.date_input(
                "Application Date",
                value=date.today()
            )

            application_status = st.selectbox(
                "Application Status",
                [
                    "Applied",
                    "Interview",
                    "Selected",
                    "Rejected"
                ]
            )

            job_link = st.text_input(
                "Job Posting Link (Optional)"
            )

            notes = st.text_area(
                "Notes (Optional)",
                placeholder="Recruiter details, interview date, follow-up notes..."
            )

            add_application = st.form_submit_button(
                "➕ Save Application",
                use_container_width=True
            )

        if add_application:

            if not company.strip() or not job_title.strip():
                st.error("Please enter both company name and job title.")

            else:
                cursor.execute(
                    """
                    INSERT INTO job_applications
                    (
                        company,
                        job_title,
                        location,
                        application_date,
                        status,
                        job_link,
                        notes
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        company.strip(),
                        job_title.strip(),
                        application_location.strip(),
                        application_date.isoformat(),
                        application_status,
                        job_link.strip(),
                        notes.strip()
                    )
                )

                connection.commit()
                st.success("Job application saved successfully!")
                st.rerun()

        # FETCH APPLICATIONS

        cursor.execute("""
            SELECT
                id,
                company,
                job_title,
                location,
                application_date,
                status,
                job_link,
                notes
            FROM job_applications
            ORDER BY id DESC
        """)

        applications = cursor.fetchall()

        # APPLICATION STATISTICS

        st.divider()
        st.subheader("📊 Application Dashboard")

        total_applications = len(applications)

        applied_count = sum(
            1 for item in applications if item[5] == "Applied"
        )

        interview_count = sum(
            1 for item in applications if item[5] == "Interview"
        )

        selected_count = sum(
            1 for item in applications if item[5] == "Selected"
        )

        rejected_count = sum(
            1 for item in applications if item[5] == "Rejected"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Applications", total_applications)
        col2.metric("Interviews", interview_count)
        col3.metric("Selected", selected_count)

        col4, col5 = st.columns(2)

        col4.metric("Applied", applied_count)
        col5.metric("Rejected", rejected_count)

        # APPLICATION LIST AND EDITING

        st.divider()
        st.subheader("📂 Your Job Applications")

        if applications:

            for application in applications:

                (
                    app_id,
                    app_company,
                    app_title,
                    app_location,
                    app_date,
                    app_status,
                    app_link,
                    app_notes
                ) = application

                with st.expander(
                    f"🏢 {app_company} — {app_title} | {app_status}"
                ):

                    st.write(f"**Application ID:** {app_id}")

                    # EDIT APPLICATION

                    st.markdown("**✏️ Edit Application Details**")

                    with st.form(f"edit_application_{app_id}"):

                        edited_company = st.text_input(
                            "Company",
                            value=app_company,
                            key=f"edit_company_{app_id}"
                        )

                        edited_title = st.text_input(
                            "Job Title",
                            value=app_title,
                            key=f"edit_title_{app_id}"
                        )

                        edited_location = st.text_input(
                            "Location",
                            value=app_location or "",
                            key=f"edit_location_{app_id}"
                        )

                        try:
                            saved_date = date.fromisoformat(app_date)
                        except (ValueError, TypeError):
                            saved_date = date.today()

                        edited_date = st.date_input(
                            "Application Date",
                            value=saved_date,
                            key=f"edit_date_{app_id}"
                        )

                        status_options = [
                            "Applied",
                            "Interview",
                            "Selected",
                            "Rejected"
                        ]

                        edited_status = st.selectbox(
                            "Status",
                            status_options,
                            index=(
                                status_options.index(app_status)
                                if app_status in status_options
                                else 0
                            ),
                            key=f"edit_status_{app_id}"
                        )

                        edited_link = st.text_input(
                            "Job Link",
                            value=app_link or "",
                            key=f"edit_link_{app_id}"
                        )

                        edited_notes = st.text_area(
                            "Notes",
                            value=app_notes or "",
                            key=f"edit_notes_{app_id}"
                        )

                        update_application = st.form_submit_button(
                            "💾 Update Application",
                            use_container_width=True
                        )

                    if update_application:

                        if not edited_company.strip() or not edited_title.strip():
                            st.error(
                                "Company and job title cannot be empty."
                            )

                        else:
                            cursor.execute(
                                """
                                UPDATE job_applications
                                SET
                                    company = ?,
                                    job_title = ?,
                                    location = ?,
                                    application_date = ?,
                                    status = ?,
                                    job_link = ?,
                                    notes = ?
                                WHERE id = ?
                                """,
                                (
                                    edited_company.strip(),
                                    edited_title.strip(),
                                    edited_location.strip(),
                                    edited_date.isoformat(),
                                    edited_status,
                                    edited_link.strip(),
                                    edited_notes.strip(),
                                    app_id
                                )
                            )

                            connection.commit()
                            st.success("Application updated!")
                            st.rerun()

                    if app_link:
                        st.link_button(
                            "🔗 Open Job Posting",
                            app_link
                        )

                    # DELETE APPLICATION

                    if st.button(
                        "🗑️ Delete Application",
                        key=f"delete_application_{app_id}"
                    ):

                        cursor.execute(
                            "DELETE FROM job_applications WHERE id = ?",
                            (app_id,)
                        )

                        connection.commit()
                        st.success("Application deleted.")
                        st.rerun()

        else:
            st.info(
                "No job applications saved yet. "
                "Add your first application above!"
            )

        connection.close()

    except sqlite3.Error as error:
        st.error(f"Database error: {error}")

    st.caption(
        "Job listings open on external websites. "
        "Your job applications are stored in your local SQLite database."
    )


# =====================================
# RESUME HISTORY
# =====================================


elif page == "Resume History":

    import sqlite3
    from pathlib import Path

    st.title("📚 Resume History")

    st.write(
        "View previous resume versions, track ATS scores "
        "and compare your improvements."
    )

    st.divider()

    db_path = (
        Path(__file__).parent
        / "database"
        / "interview_questions.db"
    )

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, resume_filename, ats_score,
                   skills_count, uploaded_at, resume_text
            FROM resume_history
            ORDER BY id DESC
            """
        )

        history = cursor.fetchall()
        connection.close()

        if history:

            st.subheader("📊 Resume Upload Statistics")

            scores = [
                row[2] for row in history
                if row[2] is not None
            ]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Uploads", len(history))

            with col2:
                st.metric(
                    "Latest ATS Score",
                    f"{history[0][2]}/100"
                    if history[0][2] is not None else "--"
                )

            with col3:
                st.metric(
                    "Latest Skills Found",
                    history[0][3]
                    if history[0][3] is not None else 0
                )

            st.divider()

            # RESUME HISTORY

            st.subheader("📄 Previous Resume Versions")

            for row in history:

                resume_id, filename, score, skills_count, uploaded_at, resume_text = row

                with st.expander(f"📄 {filename} — Version {resume_id}"):

                    st.write(f"**Upload date:** {uploaded_at}")

                    st.write(
                        f"**ATS Score:** {score}/100"
                        if score is not None
                        else "**ATS Score:** Not calculated"
                    )

                    st.write(
                        f"**Skills identified:** "
                        f"{skills_count if skills_count is not None else 'Not calculated'}"
                    )

            # ATS SCORE HISTORY

            if len(scores) >= 2:

                st.divider()
                st.subheader("📈 ATS Score History")

                st.line_chart(list(reversed(scores)))

            # RESUME VERSION COMPARISON

            st.divider()
            st.subheader("🔄 Compare Resume Versions")

            if len(history) >= 2:

                older_version = st.selectbox(
                    "Select older resume version",
                    history,
                    index=len(history) - 1,
                    format_func=lambda row: (
                        f"Version {row[0]} - {row[1]} ({row[4]})"
                    ),
                    key="older_resume_version"
                )

                newer_version = st.selectbox(
                    "Select newer resume version",
                    history,
                    index=0,
                    format_func=lambda row: (
                        f"Version {row[0]} - {row[1]} ({row[4]})"
                    ),
                    key="newer_resume_version"
                )

                if st.button("Compare My Resumes"):

                    if older_version[0] == newer_version[0]:

                        st.warning(
                            "Please select two different resume versions."
                        )

                    else:

                        skills_list = [
                            "python", "java", "html", "css",
                            "javascript", "sql", "machine learning",
                            "communication", "teamwork", "excel",
                            "react", "data analysis"
                        ]

                        old_text = (older_version[5] or "").lower()
                        new_text = (newer_version[5] or "").lower()

                        old_skills = [
                            skill for skill in skills_list
                            if skill in old_text
                        ]

                        new_skills = [
                            skill for skill in skills_list
                            if skill in new_text
                        ]

                        old_score = older_version[2]
                        new_score = newer_version[2]

                        if old_score is None:
                            old_sections = [
                                section for section in [
                                    "education", "experience", "skills",
                                    "projects", "certifications"
                                ] if section in old_text
                            ]
                            old_score = min(
                                100,
                                len(old_skills) * 5 + len(old_sections) * 8
                            )

                        if new_score is None:
                            new_sections = [
                                section for section in [
                                    "education", "experience", "skills",
                                    "projects", "certifications"
                                ] if section in new_text
                            ]
                            new_score = min(
                                100,
                                len(new_skills) * 5 + len(new_sections) * 8
                            )

                        score_difference = new_score - old_score

                        st.subheader("📊 Comparison Results")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric(
                                "Older ATS Score",
                                f"{old_score}/100"
                            )

                        with col2:
                            st.metric(
                                "Newer ATS Score",
                                f"{new_score}/100"
                            )

                        with col3:
                            st.metric(
                                "Score Change",
                                f"{score_difference:+d}",
                                delta=f"{score_difference:+d} points"
                            )

                        st.subheader("🧠 Skills Comparison")

                        gained_skills = [
                            skill for skill in new_skills
                            if skill not in old_skills
                        ]

                        lost_skills = [
                            skill for skill in old_skills
                            if skill not in new_skills
                        ]

                        col1, col2 = st.columns(2)

                        with col1:
                            st.write("**✅ Skills Gained**")

                            if gained_skills:
                                st.success(", ".join(gained_skills))
                            else:
                                st.info("No new skills detected.")

                        with col2:
                            st.write("**⚠️ Skills No Longer Detected**")

                            if lost_skills:
                                st.warning(", ".join(lost_skills))
                            else:
                                st.success("No skills lost.")

                        if score_difference > 0:
                            st.success(
                                "🎉 Your newer resume has improved its ATS-style score!"
                            )
                        elif score_difference < 0:
                            st.warning(
                                "Your newer resume has a lower ATS-style score."
                            )
                        else:
                            st.info(
                                "Both resume versions have the same ATS-style score."
                            )

            else:
                st.info(
                    "Upload at least two resume versions to compare them."
                )

        else:
            st.info(
                "No resume history available yet. "
                "Upload a resume in Resume Analyzer to get started."
            )

    except sqlite3.Error as error:
        st.error(f"Resume history database error: {error}")


# =====================================
# FOOTER
# =====================================

st.divider()

st.caption(
    "© 2026 ResumeIQ | Your Career. Your Future. 🚀"
)
