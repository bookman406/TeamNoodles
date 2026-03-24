import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/data")
async def get_data():
    return {"message": "This is data from FastAPI backend!"}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_path = os.path.join(BASE_DIR, "assets")
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
async def read_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path)

class Question(BaseModel):
    message: str

@app.post("/chat")
def chat(question: Question):

    q = question.message.lower()

    if any(word in q for word in ["register", "registration", "enroll", "enrol", "sign up", "add course", "add class", "pick course", "pick class", "select course", "choose course"]):
        return {"answer": """To register for courses, log in to Carleton Central and follow these steps:

1. Click "Getting Started" under the Registration section.
2. Choose the term appropriate to you.
3. Check your personalized time-ticket — this tells you when you can begin registering.

Things to keep in mind:
- If your Student Status or Academic Standing prevents registration, contact the Registrar's Office or Graduate Studies.
- If you have holds, click "View Holds" to see details and contact the originator.

Once everything is confirmed, you may move to the next step."""}

    if any(word in q for word in ["tuition", "fees", "fee", "cost", "how much", "price", "pay", "expensive", "computer science"]):
        return {"answer": """Tuition fees for first-year Computer Science students (Fall 2025 - Winter 2026):

- Ontario: $10,549.48
- Rest of Canada: $12,633.62
- International: $56,273.62"""}

    if any(word in q for word in ["residence", "res", "dorm", "housing", "live on campus", "room", "move in", "on campus"]):
        return {"answer": """To accept your residence offer, follow these steps:

1. Login to the Carleton Housing Portal using your MyCarletonOne credentials.
2. Go to the housing application tab.
3. Complete the process in the portal.
4. Pay the $700 non-refundable Residence Advanced Payment (RAP).
5. Click "Save & Complete" when finished."""}

    if any(word in q for word in ["advising", "advisor", "adviser", "academic help", "academic support", "guidance", "degree help", "academic advising"]):
        return {"answer": """You can contact Academic Advising here:
https://carleton.ca/academicadvising/aac-request-form/

Scroll to the bottom of the page and fill out:
- Name
- Student Number
- Degree Program
- Carleton Email Address
- Phone Number

Then click Submit and an advisor will follow up with you."""}

    if any(word in q for word in ["certificate", "enrolment", "enrollment", "proof of enrollment", "proof of enrolment", "verification", "student status"]):
        return {"answer": """To request a certificate of enrolment:

1. Visit Carleton Central.
2. Go to 'Student Online Applications'.
3. Click 'Request a Transcript/Certificate of Enrolment/Verification of Student Status'.
4. Click 'Certificate of Enrolment Request'.
5. Choose the options and terms needed.
6. Choose your delivery option.
7. Click Continue."""}

    if any(word in q for word in ["intramural", "intramurals", "sport", "sports", "league", "leagues", "recreation", "recreational", "athletics", "gym", "fitness", "campus sport"]):
        return {"answer": """You can find intramural activities here:
https://athletics.carleton.ca/students/leagues-intramurals/

- Click 'Visit Page' to view all available sports and leagues.
- You can register as an individual or as part of a team depending on the activity."""}

    if any(word in q for word in ["drop", "withdraw", "withdrawal", "unenroll", "remove course", "remove class", "cancel course", "cancel class", "leave course", "leave class"]):
        return {"answer": """To drop a class:

1. Go to Carleton Central.
2. Go to the Registration section.
3. Click 'Add/Drop Classes'.
4. Choose 'Drop' under the Action dropdown.
5. Click Submit.

Important deadlines can be found here:
https://calendar.carleton.ca/academicyear/"""}

    if any(word in q for word in ["osap", "financial aid", "student loan", "loan", "bursary", "funding", "scholarship", "grant", "money for school", "financial help", "financial"]):
        return {"answer": """For information about OSAP and other financial aid options, visit:
https://carleton.ca/awards/government-financial-aid/osap/

This page covers:
- How to apply
- What you may be eligible for
- Important deadlines you should be aware of"""}

    if any(word in q for word in ["password", "mycarletonone", "mco", "login", "log in", "locked out", "forgot", "reset password", "change password", "account", "credentials", "cant log in", "can't log in"]):
        return {"answer": """MyCarletonOne password requirements:

- 8-15 characters with no spaces
- At least 1 lowercase and 1 uppercase letter
- At least 1 number
- Allowed special characters: ! . _
- Cannot contain your username
- Cannot reuse previous 5 passwords
- Cannot be changed within 1 day of last change

More info:
https://carleton.ca/its/help-centre/accounts-and-passwords/"""}

    return {"answer": """I'm sorry, I didn't quite understand that. I can help you with questions about:

- Course registration
- Tuition fees
- Residence
- Academic advising
- Certificates of enrolment
- Intramurals
- Dropping courses
- OSAP
- MyCarletonOne passwords

Try rephrasing your question and I'll do my best to help!"""}
