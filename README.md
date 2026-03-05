# Campus Assist — Team Noodles

Repository for the IRM3004/OSS3009 Group Project.

## Overview

Campus Assist is a student focused chatbot designed to help answer common questions about services at Carleton University. The purpose of the project is to simplify how students find information by providing quick responses and directing them to the appropriate university resources.

Instead of searching through multiple pages, students can ask a question and receive guidance along with the relevant steps or links.

This project demonstrates a simple chatbot system using a static frontend interface and a lightweight backend API that returns responses to common student questions.

## Features

- Chatbot Interface
  A simple web chat interface where students can type questions and receive responses.

- FAQ Response System
  The chatbot responds to common Carleton University questions such as registration, tuition, residence, advising, and more.

- Backend API
  A FastAPI backend processes questions and returns the appropriate responses.

- Guided Instructions
  Responses provide step-by-step guidance and links to official university pages.

- Demo Knowledge Base
  The chatbot contains a set of predefined prompts and responses used to simulate an AI-powered FAQ assistant.


## How It Works

1. A user types a question in the chatbot interface.
2. The frontend sends the message to the backend API.
3. The backend checks the message against known FAQ prompts.
4. The backend returns the appropriate response.
5. The chatbot displays the answer to the user.


## Running the Project

### Run the Backend
TERMINAL: 
cd backend
python3 -m uvicorn main:app --reload --port 8001


### Run the Frontend
TERMINAL:
python3 -m http.server 5500


Then open the website in a browser:

http://127.0.0.1:5500

## Disclaimer

This project was created by **Team Noodles** as part of the IRM3004/OSS3009 course project.

Campus Assist is a student project demonstration** and is not an official Carleton University service.

* The chatbot does not access real university systems
* No personal information is collected or stored
* Responses are based on publicly available information from Carleton University websites
* The system is intended only as a prototype for demonstrating chatbot functionality

Students should always refer to official Carleton University resources or contact the appropriate department for authoritative information.


## Team

Team Noodles
IRM3004/OSS3009 Group Project
Carleton University
