from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from src.pattern_analysis import analyze_journal_entries
from src.llm_insights import generate_llm_report


app = FastAPI(title="MindTrace AI Backend")

# Enable CORS (important for Streamlit later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Request Schema
class JournalEntry(BaseModel):
    date: str
    text: str


class JournalRequest(BaseModel):
    journal_entries: List[JournalEntry]


# API Endpoint

@app.post("/analyze")
def analyze(request: JournalRequest):

    # Convert Pydantic model to dict list
    journal_data = [
        {"date": entry.date, "text": entry.text}
        for entry in request.journal_entries
    ]

    # Run core AI engine
    analysis_output = analyze_journal_entries(journal_data)

    # Generate LLM report
    llm_report = generate_llm_report(analysis_output)

    # Return full structured response
    return {
        "analysis": analysis_output,
        "llm_report": llm_report
    }


@app.get("/")
def root():
    return {"message": "MindTrace AI Backend Running"}