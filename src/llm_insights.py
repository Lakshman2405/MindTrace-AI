import requests
from src.config import HF_TOKEN
from src.config import OPENROUTER_API

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


def generate_llm_report(analysis_output):

    if not OPENROUTER_API:
        return {"error": "OPENROUTER_API not found."}

    prompt = build_llm_prompt(analysis_output)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a responsible AI emotional awareness assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.15,
        "max_tokens": 700
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return {"error": response.text}

    result = response.json()
    return result["choices"][0]["message"]["content"]