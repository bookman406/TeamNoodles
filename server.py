from typing import List, Dict
import json

import faiss
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from policy import brightspace_grades_reply

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # demo
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Optional: Load index if present (not required for demo prompts) ----
INDEX_PATH = "data/faiss.index"
META_PATH = "data/meta.json"

index = None
CHUNKS: List[str] = []
META: List[Dict] = []

try:
    index = faiss.read_index(INDEX_PATH)
    store = json.load(open(META_PATH, "r", encoding="utf-8"))
    CHUNKS = store.get("chunks", [])
    META = store.get("meta", [])
except Exception:
    # If index isn't present, demo still works
    index = None

# ---- Demo GPA rules (simple, fast) ----
GPA_RULES_DEMO = {
    "BIT": (
        "GPA rules for **BIT (Bachelor of Information Technology)** depend on Carleton’s academic regulations "
        "and your program requirements.\n\n"
        "**Demo answer (for project):**\n"
        "- Your *CGPA* is used to determine academic standing.\n"
        "- If your CGPA drops below required thresholds, students may be placed on academic warning/probation "
        "(exact thresholds depend on the calendar/regulations).\n\n"
        "**Official sources to verify (recommended):**\n"
        "- Undergraduate Calendar – Academic Regulations: https://calendar.carleton.ca/undergrad/regulations/\n"
        "- Undergraduate Calendar home: https://calendar.carleton.ca/undergrad/\n\n"
        "If you tell me your year/level (1st/2nd/3rd/4th), I can narrow down what sections to check in the calendar."
    ),
    "ENG": (
        "GPA/standing rules for **Engineering** are governed by Carleton’s academic regulations + any faculty/program rules.\n\n"
        "**Official sources to verify:**\n"
        "- Undergraduate Calendar – Academic Regulations: https://calendar.carleton.ca/undergrad/regulations/\n"
        "- Undergraduate Calendar home: https://calendar.carleton.ca/undergrad/\n\n"
        "If you tell me your specific engineering stream (Electrical/Mechanical/etc.), I can point to what to look for."
    ),
}

def normalize_program(text: str) -> str:
    t = (text or "").lower()

    # BIT
    if "bit" in t or "information technology" in t:
        return "BIT"

    # Engineering (broad demo)
    if "engineering" in t or t.strip() in {"eng", "engr"}:
        return "ENG"
    if "elec" in t or "electrical" in t:
        return "ENG"
    if "mech" in t or "mechanical" in t:
        return "ENG"
    if "civil" in t:
        return "ENG"
    if "software eng" in t or "software engineering" in t:
        return "ENG"

    return ""

def looks_like_gpa_question(text: str) -> bool:
    t = (text or "").lower()
    return ("gpa" in t) or ("cgpa" in t) or ("academic standing" in t) or ("probation" in t)

# Very simple “state” for demo: remembers that user is in the middle of GPA flow
WAITING_FOR_PROGRAM = False

class ChatIn(BaseModel):
    message: str
    k: int = 5

@app.post("/chat")
def chat(req: ChatIn):
    global WAITING_FOR_PROGRAM

    q = (req.message or "").strip()
    ql = q.lower()

    # ---- DEMO PROMPT 1: Private grades ----
    if "check my grades" in ql or "see my grades" in ql or ("my grades" in ql and "gpa" not in ql):
        WAITING_FOR_PROGRAM = False
        return {"answer": brightspace_grades_reply(), "sources": []}

    # ---- DEMO PROMPT 2: GPA rules flow ----
    # If they ask about GPA and didn't mention program → ask for program
    if looks_like_gpa_question(q) and not normalize_program(q):
        WAITING_FOR_PROGRAM = True
        return {
            "answer": (
                "Okay — GPA rules depend on your program.\n"
                "What program are you in? (Example: **BIT** or **Engineering**)\n\n"
                "Reply with just the program name."
            ),
            "sources": []
        }

    # If we were waiting for program and they reply with one
    if WAITING_FOR_PROGRAM:
        prog = normalize_program(q)
        WAITING_FOR_PROGRAM = False
        if prog:
            return {"answer": GPA_RULES_DEMO.get(prog, "I don’t have demo GPA rules for that program yet."), "sources": []}
        return {
            "answer": "I didn’t recognize that program. For the demo, try replying with **BIT** or **Engineering**.",
            "sources": []
        }

    # If they directly include program in their GPA question
    prog_direct = normalize_program(q)
    if prog_direct and looks_like_gpa_question(q):
        WAITING_FOR_PROGRAM = False
        return {"answer": GPA_RULES_DEMO.get(prog_direct, "I don’t have demo GPA rules for that program yet."), "sources": []}

    # ---- Default demo response ----
    WAITING_FOR_PROGRAM = False
    return {
        "answer": (
            "Demo mode: Try one of these:\n"
            "1) **check my grades**\n"
            "2) **what are the GPA rules?**"
        ),
        "sources": []
    }
