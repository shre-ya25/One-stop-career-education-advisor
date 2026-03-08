import streamlit as st
import os
import json
def set_sci_fi_theme():
    css = """
    <style>

    /* Main background */
    body, .stApp {
        background-color: #000010;
        background-image:
            radial-gradient(#E6E6FA 1px, transparent 1px),
            radial-gradient(#66ffcc 1px, transparent 1px),
            radial-gradient(#ff66cc 1px, transparent 1px);
        background-size: 50px 50px;
        animation: starsMove 20s linear infinite;
        color: #c0ffee;
        font-family: 'Orbitron', sans-serif;
    }

    @keyframes starsMove {
        0% {background-position: 0 0, 50px 50px, 100px 100px;}
        50% {background-position: 100px 100px, 0 0, 50px 50px;}
        100% {background-position: 0 0, 50px 50px, 100px 100px;}
    }

    /* Glass cards */
    .css-1d391kg, .stContainer {
        background: rgba(0, 0, 40, 0.75);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 0 25px rgba(0,255,255,0.4);
        transition: 0.5s;
    }

    /* Neon buttons */
    .stButton > button {
        background: #0ff;
        color: #000;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 25px;
        box-shadow: 0 0 15px #0ff, 0 0 30px #66ffcc;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px #0ff, 0 0 50px #66ffcc;
    }

    /* Skill badges */
    .skill-node {
        display: inline-block;
        background-color: #0ff;
        color: #000;
        padding: 8px 20px;
        margin: 4px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 0 10px #0ff, 0 0 20px #66ffcc;
        animation: floatNode 3s ease-in-out infinite;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

from career_simulator import simulate_future
from resume_improver import improve_summary
from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from job_roles import JOB_SKILLS
from skill_gap import find_skill_gap
from resume_scoring import calculate_resume_score
from ats_score import calculate_ats_score
from similarity import calculate_job_match
from report_generator import generate_report
from agent_chat import agent_reply
from agent import resume_agent
from roadmap import generate_roadmap
set_sci_fi_theme()


# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users" not in st.session_state:
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            st.session_state.users = json.load(f)
    else:
        st.session_state.users = {}

if "forgot_mode" not in st.session_state:
    st.session_state.forgot_mode = False

# -------- Agent Memory (NO history) --------
if "agent_memory" not in st.session_state:
    st.session_state.agent_memory = {
        "best_resume_score": 0,
        "best_ats_score": 0,
        "best_job_match": 0
    }

# -------- Agent Personality --------
if "agent_personality" not in st.session_state:
    st.session_state.agent_personality = {
        "name": "CareerBot",
        "greeting": "Hi! I'm CareerBot 🤖 — your AI career companion.",
        "closing": "Keep improving. Your future is bright 🚀"
    }

if "agent_actions" not in st.session_state:
    st.session_state.agent_actions = []

# ---------------- AUTH UI ----------------
def auth_ui():
    st.markdown("## 🔐 Welcome to AI Resume Analyzer")

    if st.session_state.forgot_mode:
        st.subheader("🔑 Reset Password")

        email = st.text_input("Registered Email")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            if email in st.session_state.users:
                st.session_state.users[email]["password"] = new_pass
                with open("users.json", "w") as f:
                    json.dump(st.session_state.users, f)
                st.success("Password reset successful!")
                st.session_state.forgot_mode = False
            else:
                st.error("Email not found")

        if st.button("⬅ Back to Login"):
            st.session_state.forgot_mode = False
        return

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email in st.session_state.users and st.session_state.users[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("Forgot Password?"):
            st.session_state.forgot_mode = True
            st.rerun()

    with tab2:
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if new_email in st.session_state.users:
                st.warning("Account already exists")
            else:
                st.session_state.users[new_email] = {"password": new_password}
                with open("users.json", "w") as f:
                    json.dump(st.session_state.users, f)
                st.success("Account created!")

if not st.session_state.logged_in:
    auth_ui()
    st.stop()


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.subheader("Account")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- AGENT GREETING ----------------
agent = st.session_state.agent_personality
st.info(agent["greeting"])

# ---------------- UI ----------------
st.title("🚀 AI Career Companion: Resume Analyzer & Advisor")

job_role = st.selectbox("Select Job Role", list(JOB_SKILLS.keys()))
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

def clean_resume_text(text):
    import re
    clean = re.sub(r'<.*?>', '', text)
    clean = re.sub(r'\n{3,}', '\n\n', clean)
    return clean.strip()

if uploaded_file:
    with st.spinner("Analyzing resume..."):
        text = extract_text_from_pdf(uploaded_file)
        skills = extract_skills(text)
        required_skills = JOB_SKILLS[job_role]
        missing_skills = find_skill_gap(skills, required_skills)

        with st.expander("📄 View Extracted Resume (Smart Viewer)", expanded=False):
          cleaned_text = clean_resume_text(text)

          st.markdown(
        f"""
        <div style="
            background: rgba(120, 0, 200, 0.15);
            border: 1px solid rgba(200, 120, 255, 0.4);
            box-shadow: 0 0 15px rgba(180, 0, 255, 0.4);
            border-radius: 15px;
            padding: 15px;
            color: #e9d5ff;
            font-family: monospace;
            white-space: pre-wrap;
            line-height: 1.5;
            max-height: 400px;
            overflow-y: auto;
            margin-top: 0px;
        ">
{cleaned_text}
        </div>
        """,
        unsafe_allow_html=True)
        resume_score = calculate_resume_score(text, skills)
        ats_score = calculate_ats_score(skills, required_skills)
        job_match = calculate_job_match(ats_score, resume_score)
        simulation = simulate_future(job_match, missing_skills)
        agent_actions = resume_agent(resume_score, ats_score, job_match, missing_skills)

        mem = st.session_state.agent_memory
        mem["best_resume_score"] = max(mem["best_resume_score"], resume_score)
        mem["best_ats_score"] = max(mem["best_ats_score"], ats_score)
        mem["best_job_match"] = max(mem["best_job_match"], job_match)

        st.session_state.agent_actions = agent_actions

        if resume_score < 75:
            improved_summary = improve_summary(text, job_role)
        else:
            improved_summary = None

        section_feedback = []
        if resume_score < 70:
            section_feedback.append("Improve resume structure.")
        if ats_score < 70:
            section_feedback.append("Add job keywords.")
        if missing_skills:
            section_feedback.append("Learn missing skills.")

        if not section_feedback:
            section_feedback.append("Resume is well optimized.")

        report_text = generate_report(
            st.session_state.user_email,
            job_role,
            resume_score,
            ats_score,
            job_match,
            skills,
            missing_skills,
            section_feedback
        )

    st.success("Resume analyzed successfully 🎉")

    # ---------------- DASHBOARD ----------------
    st.subheader("🧠 AI Agent Memory Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Best Resume Score", f"{mem['best_resume_score']}/100")
    c2.metric("Best ATS Score", f"{mem['best_ats_score']}%")
    c3.metric("Best Job Match", f"{mem['best_job_match']}%")

    # ---------------- SCORES ----------------
    st.subheader("📊 Score Meters")
    st.progress(resume_score / 100)
    st.progress(ats_score / 100)
    st.progress(job_match / 100)

    # ---------------- SKILLS ----------------
    st.subheader("✅ Your Skills")
    st.write(", ".join(skills))

    st.subheader("❌ Missing Skills")
    st.write(", ".join(missing_skills))

    # ---------------- ROADMAP ----------------
    st.subheader("🗺️ AI Skill Roadmap")
    roadmap = generate_roadmap(missing_skills)
    for step in roadmap:
        st.write("👉", step)

    # ---------------- AGENT ACTIONS ----------------
    st.subheader("🤖 AI Agent Decisions")
    for act in agent_actions:
        st.success(act)

    # ---------------- RESUME IMPROVER ----------------
    st.subheader("🛠 Resume Improvement")
    if improved_summary:
        st.text_area("Suggested Summary", improved_summary, height=150)
    else:
        st.success("Your resume summary is strong!")

    # ---------------- CHAT ----------------
    st.subheader("💬 Chat with CareerBot")

    user_msg = st.text_input("Ask me anything about your career...")

    if user_msg:
     reply = agent_reply(user_msg, st.session_state.agent_memory)

     st.markdown(
        f"""
        <div style="
            background: rgba(120, 0, 200, 0.2);
            border: 1px solid rgba(200, 120, 255, 0.45);
            box-shadow: 0 0 18px rgba(180, 0, 255, 0.6);
            border-radius: 18px;
            padding: 18px;
            color: #f3e8ff;
            margin-top: 10px;
            font-size: 15px;
            line-height: 1.6;
        ">
        🤖 <b>CareerBot</b><br><br>
        {reply}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ---------------- SIMULATION ----------------
    st.subheader("🔮 Career Simulation")
    st.info(simulation["message"])

    # ---------------- VERDICT ----------------
    st.subheader("🧠 Verdict")
    if job_match >= 80:
        st.success("Excellent match 🚀")
    elif job_match >= 60:
        st.warning("Good match 👍")
    else:
        st.error("Needs improvement ⚠️")

    # ---------------- REPORT ----------------
st.subheader("📄 AI Generated Report")

if "show_report" not in st.session_state:
    st.session_state.show_report = False

# Generate Report Button
if st.button("📝 Generate Report"):
    st.session_state.show_report = True

# Show report only after clicking Generate
if st.session_state.show_report:
    st.markdown(
        f"""
        <div style="
            background: rgba(120, 0, 200, 0.18);
            border: 1px solid rgba(200, 120, 255, 0.45);
            box-shadow: 0 0 20px rgba(180, 0, 255, 0.5);
            border-radius: 18px;
            padding: 22px;
            color: #e9d5ff;
            font-family: monospace;
            white-space: pre-wrap;
            line-height: 1.6;
            max-height: 420px;
            overflow-y: auto;
        ">
{report_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.download_button(
        "⬇️ Download Report",
        report_text,
        file_name="AI_Career_Companion_Report.txt"
    )
