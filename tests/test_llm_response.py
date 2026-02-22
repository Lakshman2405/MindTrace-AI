from src.pattern_analysis import analyze_journal_entries
from src.llm_insights import generate_llm_report
import json
'''
# Test Case 1: Mixed Sentiment with Moderate Risk
journal_entries1 = [
    {"date": "2026-02-01", "text": "I am very happy today!"},
    {"date": "2026-02-02", "text": "Work was stressful and exhausting."},
    {"date": "2026-02-03", "text": "I feel calm and relaxed."},
    {"date": "2026-02-04", "text": "I feel terrible and hopeless."}
]

analysis1 = analyze_journal_entries(journal_entries1)
print(json.dumps(analysis1, indent=4))
report1 = generate_llm_report(analysis1)
print(report1)


# Test Case2 : High risk downward spiral
journal_entries2 = [
    {"date": "2026-03-01", "text": "I feel exhausted and overwhelmed. Nothing seems to work."},
    {"date": "2026-03-02", "text": "Today was worse. I felt anxious all day and couldn't focus."},
    {"date": "2026-03-03", "text": "I keep thinking I am failing at everything."},
    {"date": "2026-03-04", "text": "I avoided everyone. I just wanted to stay alone."},
    {"date": "2026-03-05", "text": "I don't feel hopeful about tomorrow."}
]

analysis2 = analyze_journal_entries(journal_entries2)
print(json.dumps(analysis2, indent=4))
report2 = generate_llm_report(analysis2)
print(report2)

'''
# Test case 3: High Emotional Volatility
journal_entries3 = [
    {"date": "2026-03-01", "text": "I was extremely happy today! Everything felt perfect."},
    {"date": "2026-03-02", "text": "Suddenly I felt anxious and unsure about everything."},
    {"date": "2026-03-03", "text": "I felt proud and confident about my progress."},
    {"date": "2026-03-04", "text": "I got irritated over small things and felt annoyed."},
    {"date": "2026-03-05", "text": "I feel hopeful and optimistic again."}
]

analysis3 = analyze_journal_entries(journal_entries3)
print(json.dumps(analysis3, indent=4))
report3 = generate_llm_report(analysis3)
print(report3)

'''
# Test case 4: Clear Emotional Recovery
journal_entries4 = [
    {"date": "2026-03-01", "text": "I felt stressed and worried about work."},
    {"date": "2026-03-02", "text": "Still anxious but trying to manage it."},
    {"date": "2026-03-03", "text": "Today was slightly better. I felt calmer."},
    {"date": "2026-03-04", "text": "I felt hopeful and motivated."},
    {"date": "2026-03-05", "text": "I am proud of how I handled things this week."}
]
analysis4 = analyze_journal_entries(journal_entries4)
print(json.dumps(analysis4, indent=4))
report4 = generate_llm_report(analysis4)
print(report4)

'''