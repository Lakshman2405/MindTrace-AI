import requests
from src.config import HF_TOKEN
from src.config import OPENROUTER_API_KEY

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"


def build_llm_prompt(analysis_output):

    structured = analysis_output["structured_insight"]

    return f"""
You are an AI-powered Mental-State Awareness Companion.

Interpret the provided emotional pattern and trajectory exactly as given.
Do NOT contradict them.
Do NOT invent information.
Do NOT diagnose.
Address the user directly like you are his/her personal wellbring assistant
Write a supportive emotional awareness companion
Avoid third person refernces such as "the individual".
Consider that user is seeking emotional comfort in your report,
Change your tone according to situation, be empathetic and supportive.
Only talk to user as his/her mental wellbeing assistant, They shouldn't know about that, You just keep it in consideration.
They should only see purely your narrative which eases their mind.
Don't mention anywhere in the report that you  are an support system , bettter be consider yourself as user's friend than their aassistant.  
Use human friendly language and words, don't go too technical words, be more empathetic and supportive in your tone.

Pattern Type: {analysis_output["pattern_type"]}
Trajectory: {analysis_output["trajectory_type"]}
Risk Level: {analysis_output["risk_level"]}

Structured Insight:
Summary: {structured["summary"]}
Behavior: {structured["behavior"]}
Recommendation: {structured["recommendation"]}

Generate a professional emotional awareness report with the following headings:

Title: Mental-State Awareness Report

Emotional State Overview
Risk Interpretation
Behavioral Pattern Analysis
Emotional Resilience Perspective
Reflection & Growth Recommendations
Ongoing Awareness Guidance
"""


HF_ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"


def generate_llm_report(analysis_output):

    if not HF_TOKEN:
        return "LLM report unavailable: HF_TOKEN not configured."

    prompt = build_llm_prompt(analysis_output)

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a responsible AI emotional awareness assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.15,
        "max_tokens": 600
    }

    try:
        response = requests.post(
            HF_ROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"HF Router Error ({response.status_code}): {response.text}"

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]

        return "HF Router response received but content missing."

    except Exception as e:
        return f"HF Router request failed: {str(e)}"