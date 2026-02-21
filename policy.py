BRIGHTSPACE = "https://brightspace.carleton.ca/"
CARLETON_PHONE = "+1 613-520-2600"

GRADE_STEPS = [
    "Open Brightspace: https://brightspace.carleton.ca/",
    "Log in with your MyCarletonOne credentials.",
    "From the homepage, open your course (or use the waffle/grid menu → Courses).",
    "Click **Grades** in the course navigation bar.",
    "If you’re asked, select the correct **term/semester**.",
    "If you still can’t find it, check **Content** or **Course Tools**, or message your TA/instructor."
]

def brightspace_grades_reply() -> str:
    steps = "\n".join([f"{i+1}. {s}" for i, s in enumerate(GRADE_STEPS)])
    return (
        "That information is behind login (Brightspace), so I can’t pull it from public Carleton websites.\n\n"
        f"Link: {BRIGHTSPACE}\n"
        f"General phone (if you’re stuck): {CARLETON_PHONE}\n\n"
        f"Steps:\n{steps}"
    )