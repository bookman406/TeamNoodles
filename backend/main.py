from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    message: str


@app.post("/chat")
def chat(question: Question):

    q = question.message.lower()

    if "register" in q and "course" in q:
        return {"answer": """Log in to Carleton Central.
Click on “Getting Started” under the “Registration” section.
Choose the term appropriate to you.

This is where you will see your personalized time-ticket.
You may begin to register at the specified date/time.

If your Student Status or Academic Standing prevents registration,
please contact the Registrar’s Office or Graduate Studies.

Holds may prevent registration. If you have holds,
click “View Holds” to see details and contact the originator.

Once everything is confirmed, you may move to the next step."""}


    if "tuition" in q or "computer science" in q:
        return {"answer": """Tuition fees for first year Computer Science students (Fall 2025 - Winter 2026):

Ontario: $10,549.48
Rest of Canada: $12,633.62
International: $56,273.62"""}


    if "residence" in q:
        return {"answer": """To accept your residence offer:

1. Login to the Carleton Housing Portal using your MyCarletonOne credentials.
2. Go to the housing application tab.
3. Complete the process in the portal.
4. Pay the $700 non-refundable Residence Advanced Payment (RAP).
5. Click “Save & Complete” when finished."""}


    if "academic advising" in q or "advisor" in q:
        return {"answer": """You can contact Academic Advising here:

https://carleton.ca/academicadvising/aac-request-form/

Scroll to the bottom of the page and fill out:
Name
Student Number
Degree Program
Carleton Email Address
Phone Number

Then click Submit."""}


    if "certificate of enrolment" in q or "enrolment" in q:
        return {"answer": """To request a certificate of enrolment:

1. Visit Carleton Central
2. Go to ‘Student Online Applications’
3. Click ‘Request a Transcript/Certificate of Enrolment/Verification of Student Status’
4. Click ‘Certificate of Enrolment Request’
5. Choose the options and terms needed
6. Choose delivery option
7. Click Continue."""}


    if "intramural" in q:
        return {"answer": """You can find intramural activities here:

https://athletics.carleton.ca/students/leagues-intramurals/

Click 'Visit Page' to view activities and register as an individual or team."""}


    if "drop a class" in q or "drop course" in q:
        return {"answer": """To drop a class:

1. Go to Carleton Central
2. Go to the Registration section
3. Click ‘Add/Drop Classes’
4. Choose ‘Drop’ under the Action dropdown
5. Click Submit

Important deadlines can be found here:
https://calendar.carleton.ca/academicyear/"""}


    if "osap" in q:
        return {"answer": "For information about OSAP visit: https://carleton.ca/awards/government-financial-aid/osap/"}


    if "password" in q or "mycarletonone" in q:
        return {"answer": """MyCarletonOne password requirements:

• 8-15 characters with no spaces
• At least 1 lowercase and 1 uppercase letter
• At least 1 number
• Allowed special characters: ! . _
• Cannot contain your username
• Cannot reuse previous 5 passwords
• Cannot be changed within 1 day of last change

More info:
https://carleton.ca/its/help-centre/accounts-and-passwords/"""}


    return {"answer": "Sorry, I can only answer questions about registration, tuition, residence, advising, certificates, intramurals, dropping courses, OSAP, and MyCarletonOne passwords."}
