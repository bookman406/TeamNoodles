import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",  # React default port
    "http://localhost:8001"   # port used for this project
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc)
    allow_headers=["*"],  # allow all request headers
)

# Simulate an API interface for calling JS
@app.get("/api/data")
async def get_data():
    return {"message": "This is data from FastAPI backend!"}

# Mount static folder so that web browser can access .js file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_path = os.path.join(BASE_DIR, "assets")
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# Set route for first page, and return to index.html
@app.get("/")
async def read_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path)

class Question(BaseModel):
    message: str

# Chat endpoint — matches user input to a topic and returns the appropriate answer
@app.post("/chat")
def chat(question: Question):

    q = question.message.lower()

    if any(word in q for word in [
        "register", "registration", "enroll", "enrol", "sign up", "add course", "add class",
        "pick course", "pick class", "select course", "choose course",
        "how do i register", "how do i sign up", "how can i register",
        "where do i register", "how to register for", "i want to register",
        "i want to enroll", "i need to register", "can i register",
        "when can i register", "how do i add a course", "how do i add a class"]):
        return {"answer": """To register for courses, log in to Carleton Central and follow these steps:

1. Click "Getting Started" under the Registration section.
2. Choose the term appropriate to you.
3. Check your personalized time-ticket — this tells you when you can begin registering.

Things to keep in mind:
- If your Student Status or Academic Standing prevents registration, contact the Registrar's Office or Graduate Studies.
- If you have holds, click "View Holds" to see details and contact the originator.

Once everything is confirmed, you may move to the next step."""}

    if any(word in q for word in [
        "tuition", "fees", "fee", "cost", "how much", "price", "pay", "expensive", "engineering ", "Information Technology ", "Information Technology Fee ", 
        "how much is tuition", "how much does it cost", "what is the tuition",
        "what are the fees", "how much do i pay", "how much is carleton",
        "how much is the program", "what does carleton cost", "how much is first year",
        "how much is computer science", "what is the cost of"]):
        return {"answer": """
Full-fee Domestic Undergraduate Status
(2.0 or more billing hours per term, Fall + Winter combined, UPASS included)
Note: Compulsory miscellaneous fees are included in all quoted fees.

Bachelor of Engineering:
- First Year:  $12,007.32 
- Second Year: $11,996.58
- Third Year:  $11,996.58
- Fourth Year: $11,997.08

For a full list of fees, visit:
https://carleton.ca/studentaccounts/tuition-fees/"""}

    if any(word in q for word in [
        "residence", "res", "dorm", "housing", "live on campus", "room", "move in", "on campus",
        "how do i get into residence", "how do i accept residence", "where do i live",
        "how do i apply for residence", "how do i get a dorm", "i want to live on campus",
        "how do i move into residence", "where can i live", "student housing",
        "how do i get housing", "do i need to pay for residence"]):
        return {"answer": """To accept your residence offer, follow these steps:

1. Login to the Carleton Housing Portal using your MyCarletonOne credentials.
2. Go to the housing application tab.
3. Complete the process in the portal.
4. Pay the $700 non-refundable Residence Advanced Payment (RAP).
5. Click "Save & Complete" when finished."""}

    if any(word in q for word in [
        "advising", "advisor", "adviser", "academic help", "academic support", "guidance", "degree help",
        "how do i get academic help", "where do i get advising", "i need academic help",
        "how do i contact an advisor", "who do i talk to about my degree",
        "i need help with my courses", "can i talk to an advisor",
        "how do i get guidance", "where can i get academic support",
        "i need advice about my program", "who helps with course selection"]):
        return {"answer": """You can contact Academic Advising here:
https://carleton.ca/academicadvising/aac-request-form/

Scroll to the bottom of the page and fill out:
- Name
- Student Number
- Degree Program
- Carleton Email Address
- Phone Number

Then click Submit and an advisor will follow up with you."""}

    if any(word in q for word in [
        "certificate", "enrolment", "enrollment", "proof of enrollment", "proof of enrolment",
        "verification", "student status",
        "how do i get a certificate of enrollment", "how do i prove i am enrolled",
        "i need proof of enrollment", "how do i get an enrollment letter",
        "where do i get a certificate of enrolment", "i need a student status letter",
        "how do i verify my enrollment", "can i get proof that i am a student"]):
        return {"answer": """To request a certificate of enrolment:

1. Visit Carleton Central.
2. Go to 'Student Online Applications'.
3. Click 'Request a Transcript/Certificate of Enrolment/Verification of Student Status'.
4. Click 'Certificate of Enrolment Request'.
5. Choose the options and terms needed.
6. Choose your delivery option.
7. Click Continue."""}

    if any(word in q for word in [
        "intramural", "intramurals", "sport", "sports", "league", "leagues",
        "recreation", "recreational", "athletics", "gym", "fitness", "campus sport",
        "how do i join intramurals", "how do i play sports on campus",
        "where can i play sports", "how do i join a league",
        "i want to play sports", "how do i sign up for intramurals",
        "where can i work out", "what sports are available", "how do i join a team"]):
        return {"answer": """You can find intramural activities here:
https://athletics.carleton.ca/students/leagues-intramurals/

- Click 'Visit Page' to view all available sports and leagues.
- You can register as an individual or as part of a team depending on the activity."""}

    if any(word in q for word in [
        "drop", "withdraw", "withdrawal", "unenroll", "remove course", "remove class",
        "cancel course", "cancel class", "leave course", "leave class",
        "how do i drop a class", "how do i drop a course", "how do i withdraw",
        "i want to drop a course", "i want to remove a class", "can i drop a course",
        "how do i unenroll", "how do i cancel a course", "how do i leave a class",
        "what is the deadline to drop", "how do i get out of a course"]):
        return {"answer": """To drop a class:

1. Go to Carleton Central.
2. Go to the Registration section.
3. Click 'Add/Drop Classes'.
4. Choose 'Drop' under the Action dropdown.
5. Click Submit.

Important deadlines can be found here:
https://calendar.carleton.ca/academicyear/"""}

    if any(word in q for word in [
        "osap", "financial aid", "student loan", "loan", "bursary", "funding",
        "scholarship", "grant", "money for school", "financial help", "financial",
        "how do i apply for osap", "how do i get financial aid", "i need money for school",
        "how do i get a student loan", "how do i apply for a bursary",
        "how do i get a scholarship", "is there financial help available",
        "how do i fund my education", "how do i get help paying for school"]):
        return {"answer": """For information about OSAP and other financial aid options, visit:
https://carleton.ca/awards/government-financial-aid/osap/

This page covers:
- How to apply
- What you may be eligible for
- Important deadlines you should be aware of"""}

    if any(word in q for word in [
        "password", "mycarletonone", "mco", "login", "log in", "locked out",
        "forgot", "reset password", "change password", "account", "credentials",
        "cant log in", "can't log in",
        "i forgot my password", "how do i reset my password", "i can't log in",
        "how do i change my password", "i am locked out", "i can't access my account",
        "what are the password requirements", "how do i unlock my account",
        "how do i log into mycarletonone", "i forgot my mycarletonone password"]):
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

    # Default response if no topic matched
    return {"answer": """I'm sorry, I didn't quite understand that. For an answer please enter one of the key words in regards to the topic you are interested in:

- Course registration
- Tuition fees
- Residence
- Academic advising
- Certificates of enrolment
- Intramurals
- Dropping courses
- OSAP
- MyCarletonOne passwords

I'll do my best to help!"""}
