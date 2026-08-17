# Suwa Setha Triage

A rule-based medical triage prototype designed to prioritize patient cases based on symptom descriptions.  
Built as part of an Emerging Technologies assignment.

## Overview

Suwa Setha Triage is a lightweight web application that classifies patient urgency levels (**High**, **Medium**, **Low**) using keyword-based rules. It includes an admin dashboard for managing and viewing the patient queue.

This prototype demonstrates how simple rule-based logic can support decision-making in healthcare environments.

> **Disclaimer:** This is an educational prototype and is **not** intended to provide medical diagnosis or replace professional medical advice.

## Features

- Patient symptom submission form
- Rule-based triage engine
- High / Medium / Low priority classification
- Admin login and protected dashboard
- Real-time priority scoring
- Automatic patient queue sorting
- Clean and simple web interface
- Session-based authentication

## Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, Jinja2  
- **Authentication:** Flask sessions  
- **Storage:** In-memory data storage  
- **Deployment:** Vercel configuration included  

## How the Triage Logic Works

The system analyzes the symptoms entered by the patient and matches them against predefined keyword lists:

| Priority   | Example Keywords                                              |
|------------|---------------------------------------------------------------|
| **High**   | chest pain, difficulty breathing, unconscious, severe bleeding, stroke, seizure |
| **Medium** | high fever, vomiting, fracture, severe pain, allergic reaction |
| **Low**    | mild cough, cold, headache, sore throat, mild fever           |

If no keywords match, the case is classified as **Low (Unmatched)** and can be manually reviewed by an administrator.

## Project Structure

```text
suwa-setha-triage/
├── api/                # API-related files
├── static/             # CSS and static assets
├── templates/          # HTML/Jinja2 templates
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
└── vercel.json         # Vercel deployment configuration
Installation & Running Locally

Clone the repository

Bashgit clone https://github.com/akifffur/suwa-setha-triage.git
cd suwa-setha-triage

Install dependencies

Bashpip install -r requirements.txt

Run the application

Bashpython app.py

Open your browser and go to:

texthttp://127.0.0.1:5000
Default Admin Credentials
textUsername: admin
Password: suwasetha123
Security Notice: These credentials are hardcoded for demonstration purposes only and must not be used in a production environment.
Future Improvements

Replace in-memory storage with a proper database
Implement secure password hashing
Add patient authentication
Introduce role-based access control
Improve classification using NLP or machine learning
Add multilingual support
Implement persistent patient records
Add analytics and reporting
Strengthen input validation and security
Deploy with production-grade practices

Author
Akif ur Rahman
HND in Computing (Cyber Security)

LinkedIn: akif-ur-rahman
GitHub: akifffur

License
This project was created for educational purposes as part of an Emerging Technologies assignment.
