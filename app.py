import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import HRFlowable
from io import BytesIO
import sys

from src.pattern_analysis import analyze_journal_entries
from src.llm_insights import generate_llm_report

#from src.mindtrace-ai.src.pattern_analysis #import analyze_journal_entries

#from src.mindtrace-ai.src.llm_insights #import generate_llm_report


# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="MindTrace AI", page_icon="🧠", layout="wide")

API_URL =os.getenv("API_URL")
USE_BACKEND = API_URL is not None
HISTORY_FILE = "analysis_history.json"


# =========================================================
# PERSISTENCE
# =========================================================
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# =========================================================
# SESSION STATE INIT
# =========================================================
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = load_history()

# =========================================================
# RISK COLOR
# =========================================================
def get_risk_color(score):
    if score < 25:
        return "#16a34a"
    elif score < 50:
        return "#eab308"
    elif score < 75:
        return "#f97316"
    else:
        return "#ef4444"

#=============================================================
# GENERATE PDF REPORT
#=============================================================
def generate_pdf_report(analysis, report):
    if not report:
        report = "LLM report not available."

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("MindTrace AI - Mental Awareness Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(HRFlowable(width="100%"))
    elements.append(Spacer(1, 0.3 * inch))

    # Risk Summary
    elements.append(Paragraph("Risk Summary", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    risk_points = [
        f"Risk Score: {analysis.get('risk_score')}",
        f"Risk Level: {analysis.get('risk_level')}",
        f"Trajectory: {analysis.get('trajectory_type')}",
        f"Pattern Type: {analysis.get('pattern_type')}"
    ]

    elements.append(ListFlowable(
        [ListItem(Paragraph(point, styles["Normal"])) for point in risk_points],
        bulletType='bullet'
    ))

    elements.append(Spacer(1, 0.4 * inch))

    # Behavioral Metrics
    elements.append(Paragraph("Behavioral Metrics", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    metric_points = [
        f"Emotional Volatility: {analysis.get('emotional_volatility')}",
        f"Behavioral Drift: {analysis.get('behavioral_drift')}",
        f"Longest Negative Streak: {analysis.get('longest_negative_streak')}",
        f"Current Negative Streak: {analysis.get('current_negative_streak')}"
    ]

    elements.append(ListFlowable(
        [ListItem(Paragraph(point, styles["Normal"])) for point in metric_points],
        bulletType='bullet'
    ))

    elements.append(Spacer(1, 0.4 * inch))

    # AI Report
    elements.append(Paragraph("AI Reflection", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(report.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer

# =========================================================
# HERO HEADER
# =========================================================
analysis = st.session_state.analysis_result

if analysis:
    risk_score = analysis["analysis"]["risk_score"]
    risk_level = analysis["analysis"]["risk_level"]
    trajectory = analysis["analysis"]["trajectory_type"]
    color = get_risk_color(risk_score)
else:
    risk_score = 0
    risk_level = "No Analysis"
    trajectory = "—"
    color = "#1e293b"

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {color}, #111827);
    padding: 60px;
    border-radius: 20px;
    color: white;
    text-align:center;
    margin-bottom:40px;
">
    <h1>🧠 MindTrace AI</h1>
    <p>Hybrid Emotional Intelligence & Mental Awareness Platform</p>
    <h3>Risk Level: {risk_level}</h3>
    <h4>Trajectory: {trajectory}</h4>
</div>
""", unsafe_allow_html=True)

# =========================================================
# EARLY WARNING PANEL (ALWAYS VISIBLE VERSION)
# =========================================================
if st.session_state.analysis_result:

    analysis_data = st.session_state.analysis_result.get("analysis", {})

    risk_score = analysis_data.get("risk_score", 0)
    trajectory = analysis_data.get("trajectory_type", "stable")
    current_streak = analysis_data.get("current_negative_streak", 0)
    volatility = analysis_data.get("emotional_volatility", 0)

    alerts = []

    if risk_score >= 75:
        alerts.append(("🔴 Critical Risk Level Detected", "error"))
    elif risk_score >= 50:
        alerts.append(("🟠 High Emotional Risk Observed", "warning"))

    if trajectory == "declining":
        alerts.append(("📉 Downward Emotional Trajectory", "warning"))

    if current_streak >= 3:
        alerts.append(("⚠ Sustained Negative Streak Detected", "warning"))

    if volatility > 0.2:
        alerts.append(("⚡ Elevated Emotional Volatility", "warning"))

    if trajectory == "improving":
        alerts.append(("🟢 Emotional Recovery Trend Observed", "success"))

    st.markdown("## 🚨 Early Insight Signals")

    if alerts:
        for message, level in alerts:
            if level == "error":
                st.error(message)
            elif level == "warning":
                st.warning(message)
            else:
                st.success(message)
    else:
        st.success("🟢 No critical early warning signals detected. Emotional state appears stable.")

    st.markdown("---")


# =========================================================
# JOURNAL BUILDER
# =========================================================
st.markdown("## 📓 Journal Entry Builder")

left, right = st.columns(2)

with left:
    entry_date = st.date_input("Date", value=date.today())
    entry_text = st.text_area("Write your thoughts...", height=150)

    c1, c2 = st.columns(2)

    if c1.button("➕ Add Entry"):
        if entry_text.strip():
            st.session_state.journal_entries.append({
                "date": str(entry_date),
                "text": entry_text.strip()
            })
            st.success("Entry Added")

    if c2.button("🗑 Clear Entries"):
        st.session_state.journal_entries = []
        st.session_state.analysis_result = None
        st.info("Entries Cleared")

with right:
    st.markdown("### 📋 Current Entries")
    if st.session_state.journal_entries:
        for e in st.session_state.journal_entries:
            st.markdown(f"""
            <div style="
                background:#f3f4f6;
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;
                border-left:5px solid #3b82f6;
            ">
                <strong>{e['date']}</strong><br>
                {e['text']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No entries yet.")

# =========================================================
# ANALYZE BUTTON
# =========================================================
st.markdown("---")

if st.button("🔍 Analyze Mental State", use_container_width=True):
    if not st.session_state.journal_entries:
        st.warning("Add journal entries before analyzing.")
    else:
        try:
            with st.spinner("🧠 Analyzing mental state..."):

                # ===============================
                # MODE 1: LOCAL (FASTAPI BACKEND)
                # ===============================
                if USE_BACKEND:
                    response = requests.post(
                        API_URL,
                        json={"journal_entries": st.session_state.journal_entries}
                    )
                    result = response.json()

                # ===============================
                # MODE 2: CLOUD (DIRECT EXECUTION)
                # ===============================
                else:
                    analysis_output = analyze_journal_entries(
                        st.session_state.journal_entries
                    )

                    llm_report = generate_llm_report(analysis_output)

                    result = {
                        "analysis": analysis_output,
                        "llm_report": llm_report
                    }

            session_record = {
                "session_name": f"Session {len(st.session_state.analysis_history)+1}",
                "journal_entries": st.session_state.journal_entries.copy(),
                "analysis": result["analysis"],
                "llm_report": result["llm_report"]
            }

            st.session_state.analysis_result = session_record
            st.session_state.analysis_history.append(session_record)
            save_history(st.session_state.analysis_history)

            st.success("Analysis Completed")

        except Exception as e:
            st.error("Analysis failed.")
            st.exception(e)

# =========================================================
# SESSION HISTORY
# =========================================================
st.sidebar.header("🗂 Session History")

for idx, session in enumerate(st.session_state.analysis_history):

    # Safe session name fallback
    session_name = session.get("session_name", f"Session {idx+1}")

    with st.sidebar.expander(session_name):

        if "analysis" in session:
            st.write(f"Risk: {session['analysis'].get('risk_score', '—')}")

        # LOAD SESSION
        if st.button("Load", key=f"load_{idx}"):
            st.session_state.analysis_result = session

            if "journal_entries" in session:
                st.session_state.journal_entries = session["journal_entries"].copy()
            else:
                st.session_state.journal_entries = []

        # RENAME
        new_name = st.text_input(
            "Rename",
            value=session_name,
            key=f"rename_{idx}"
        )

        if st.button("Save Name", key=f"save_{idx}"):
            st.session_state.analysis_history[idx]["session_name"] = new_name
            save_history(st.session_state.analysis_history)
            st.success("Renamed")

        # DELETE
        if st.button("Delete Session", key=f"delete_{idx}"):
            st.session_state.analysis_history.pop(idx)
            save_history(st.session_state.analysis_history)
            st.success("Deleted")
            st.experimental_rerun()

# CLEAR ALL
if st.sidebar.button("Clear All History"):
    st.session_state.analysis_history = []
    save_history([])
    st.success("All history cleared")
    st.experimental_rerun()

# =========================================================
# DASHBOARD
# =========================================================
if st.session_state.analysis_result:
    data = st.session_state.analysis_result
    analysis = data["analysis"]
    report = data["llm_report"]
    raw = analysis["raw_results"]

    df = pd.DataFrame(raw)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    tabs = st.tabs([
        "📝 AI Report",
        "📊 Risk Overview",
        "📈 Emotional Trends",
        "🧠 Behavioral Intelligence",
        "🧭 Session Analytics",
        "📄 Structured Analysis"
    ])

    # ================= RISK =================
    with tabs[1]:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=analysis["risk_score"],
            gauge={"axis": {"range": [0, 100]}}
        ))
        st.plotly_chart(gauge, use_container_width=True)

        # EXPLAINABLE RISK CONTRIBUTION BOX (BACKEND-DRIVEN)

        st.markdown("### 🧠 Risk Score Breakdown")

        breakdown = analysis.get("risk_breakdown", {})

        if breakdown:
            total = 0
            for label, value in breakdown.items():
                st.info(f"➕ {label}: +{value}")
                total += value

            st.markdown(f"**Calculated Total Risk: {round(total, 2)}**")
            st.markdown(f"**Final Risk Score: {analysis.get('risk_score', 0)}**")
        else:
            st.success("🟢 Minimal contributing risk factors detected.")

    # ================= TRENDS =================
    with tabs[2]:
        df["moving_avg"] = df["sentiment_score"].rolling(3, min_periods=1).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"], y=df["sentiment_score"],
                                 mode="lines+markers", name="Sentiment"))
        fig.add_trace(go.Scatter(x=df["date"], y=df["moving_avg"],
                                 mode="lines", name="Moving Avg",
                                 line=dict(dash="dash")))
        st.plotly_chart(fig, use_container_width=True)

        # EMOTIONAL CALENDAR HEATMAP

        st.markdown("### 🗓 Emotional Calendar Heatmap")

        heatmap_df = df.copy()

        # Convert sentiment_score into visual intensity
        heatmap_df["intensity"] = heatmap_df["sentiment_score"]

        # Create calendar-style heatmap using Plotly
        fig_heatmap = go.Figure(data=go.Heatmap(
            x=heatmap_df["date"],
            y=["Emotional State"] * len(heatmap_df),
            z=heatmap_df["intensity"],
            colorscale=[
                [0.0, "#dc2626"],   # red for negative
                [0.5, "#facc15"],   # yellow for neutral
                [1.0, "#16a34a"]    # green for positive
            ],
            zmin=-1,
            zmax=1,
            showscale=True
        ))

        fig_heatmap.update_layout(
            height=200,
            yaxis=dict(showticklabels=False),
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

    # ================= INTELLIGENCE =================
    with tabs[3]:

        st.metric("Emotional Volatility", analysis["emotional_volatility"])
        st.metric("Behavioral Drift", analysis["behavioral_drift"])

        emotion_counts = {}
        for entry in raw:
            for emotion, score in entry["emotion_scores"]:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + score

        if emotion_counts:
            pie = px.pie(
                names=list(emotion_counts.keys()),
                values=list(emotion_counts.values())
            )
            st.plotly_chart(pie, use_container_width=True)

        combined_text = " ".join(
            [e["text"] for e in st.session_state.journal_entries]
        ).strip()

        if combined_text:
            wc = WordCloud(width=800, height=400,
                           background_color="white").generate(combined_text)
            fig_wc, ax = plt.subplots()
            ax.imshow(wc)
            ax.axis("off")
            st.pyplot(fig_wc)

    # ================= SESSION ANALYTICS =================
    with tabs[4]:

        st.subheader("Session Pattern Classification")

        st.metric("Pattern Type", analysis.get("pattern_type", "—"))
        st.metric("Trajectory Type", analysis.get("trajectory_type", "—"))

        st.markdown("---")

        st.subheader("Sentiment Distribution")

        sentiment_counts = df["sentiment_score"].value_counts()

        labels = []
        values = []

        for score, count in sentiment_counts.items():
            if score == 1:
                labels.append("Positive")
            elif score == -1:
                labels.append("Negative")
            else:
                labels.append("Neutral")

            values.append(count)

        if values:
            fig_sent = px.pie(
                names=labels,
                values=values,
                title="Sentiment Breakdown"
            )
            st.plotly_chart(fig_sent, use_container_width=True)

        st.markdown("---")

        st.subheader("Session Summary Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("Longest Negative Streak", analysis["longest_negative_streak"])
        col2.metric("Current Negative Streak", analysis["current_negative_streak"])
        col3.metric("Sentiment Momentum", round(analysis["sentiment_momentum"], 3))

    # ================= AI REPORT =================
    with tabs[0]:
        st.markdown(report)

    # ================= STRUCTURED ANALYSIS =================
    with tabs[5]:
        st.subheader("Structured Analytical Output")
        # Copy analysis safely
        structured_data = analysis.copy()
        # Separate raw results
        raw_results = structured_data.pop("raw_results", [])
        # Show structured core metrics
        st.json(structured_data)
        st.download_button(
            label="Download Structured Analysis JSON",
            data=json.dumps(structured_data, indent=4),
            file_name="structured_analysis.json",
            mime="application/json"
        )
        st.markdown("---")
        st.subheader("Raw Emotional Results")
        st.json(raw_results)
        st.download_button(
            label="Download Raw Emotional Results JSON",
            data=json.dumps(raw_results, indent=4),
            file_name="raw_emotional_results.json",
            mime="application/json"
        )
        pdf_buffer = generate_pdf_report(analysis, report)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name="MindTrace_Report.pdf",
            mime="application/pdf"
        )