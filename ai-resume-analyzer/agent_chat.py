import subprocess
import json

def agent_reply(user_input, memory):
    """
    ChatGPT-like AI Career Agent using Ollama
    """

    if not user_input.strip():
        return "I'm listening 😊 Ask me anything about your resume, skills, or career."

    # ----- Build smart context -----
    context = f"""
You are CareerBot, an intelligent AI Career Companion.

You help users with:
- Resume improvement
- ATS optimization
- Skill gap analysis
- Career roadmap
- Interview and job guidance

User context:
- Best Resume Score: {memory.get("best_resume_score", 0)}/100
- Best ATS Score: {memory.get("best_ats_score", 0)}%
- Best Job Match: {memory.get("best_job_match", 0)}%

Rules:
- Be friendly and encouraging
- Respond like ChatGPT
- Give clear, practical advice
- Do NOT repeat generic responses
- Do NOT mention being an AI model
"""

    prompt = f"""
{context}

User question:
{user_input}

Answer clearly and helpfully:
"""

    try:
        # Call Ollama (phi3:mini is lightweight)
        result = subprocess.run(
            ["ollama", "run", "phi3:mini"],
            input=prompt,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            return "⚠️ CareerBot is temporarily unavailable. Please try again."

        response = result.stdout.strip()

        # Safety fallback
        if not response:
            return "🤔 I need a bit more detail. Could you rephrase your question?"

        return response

    except FileNotFoundError:
        return (
            "❌ Ollama is not running.\n\n"
            "Please start Ollama and run:\n"
            "`ollama run phi3:mini`"
        )
