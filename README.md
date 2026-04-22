# Team Request Tracker

## Overview

Team Request Tracker is a lightweight one-page web app for workplace teams to submit, track, and fulfill requests for files, responses, or follow-up items in one organized place.

The goal of the app is to reduce the messiness of handling requests through chat tools like Slack, where requests can get buried in threads, forgotten, or completed without clear visibility.

This project was intentionally scoped as a small but polished MVP for an entry-level software developer pre-work assignment.

## Features

- Create a new request with a title, type, description, requester, assignee, priority, and due date
- View all requests in one place
- Filter requests by person, status, priority, type, and search text
- View requests by sent or received
- Update an existing request
- Add a response note
- Record what file or response was delivered
- Mark a request as completed
- Delete requests
- Persist request data locally

## Tech Stack

- Python
- Streamlit
- JSON for lightweight local persistence

## Setup Instructions

### 1. Create and activate a virtual environment (recommended)

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Open the local URL

Streamlit will provide a local URL in the terminal, usually:

```text
http://localhost:8501
```

## How It Works

Users can submit a new request by entering the request details, including who is requesting the item and who it is assigned to. Once created, requests appear on the main page, where users can filter them by person, status, priority, request type, or search text.

The app also allows users to view requests in terms of what they have sent and what they have received. Each request can be expanded and updated with a new status, reassigned if needed, and supplemented with a response note or delivered item. Completed requests remain visible for tracking purposes, and all request data is stored locally so it persists between sessions.

## Key Design Decisions

- **One-page layout:** I kept the app on one page so the full workflow of submitting, viewing, filtering, and updating requests could happen in one place without extra navigation.
- **Focused use case:** Instead of building a broad project management tool, I focused on one specific workflow: managing file, response, and follow-up requests more clearly than chat threads.
- **Streamlit for speed and simplicity:** I chose Streamlit because Python is one of the languages I currently know best, and it allowed me to build a working web app quickly within the assignment timeline.
- **Local persistence:** I used JSON-based local storage instead of a full database to keep the MVP lightweight and easy to run locally.
- **Intentional scope limits:** I left out authentication, external integrations, and production-level infrastructure so I could focus on delivering a working MVP with clear core functionality.

## Limitations and Future Improvements

This app is an MVP prototype and not a production-ready internal platform. It uses local JSON storage, does not include user authentication, and records delivered files as text rather than true file uploads.

Future improvements could include:

- authentication and user accounts
- file upload support
- Slack or email notifications
- activity history
- a shared database for multi-user support
- tagging or categorization
