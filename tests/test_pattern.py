from src.llm_insights import generate_llm_report
from src.pattern_analysis import analyze_journal_entries
import json

journal_entries = [
    {"date": "2026-02-01", "text": "I am very happy today!"},
    {"date": "2026-02-02", "text": "Work was stressful and exhausting."},
    {"date": "2026-02-03", "text": "I feel calm and relaxed."},
    {"date": "2026-02-04", "text": "I feel terrible and hopeless."}
]

analysis = analyze_journal_entries(journal_entries)

print(json.dumps(analysis, indent=4))


