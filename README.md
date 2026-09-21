# FEMCA Analysis Management Platform

A facilities/equipment FEMCA analysis management platform built with **Vue 3** and **Django REST Framework**. The application was developed with AI-assisted coding using Trae and is also used as a practical software-testing project, with emphasis on **API testing and API automation**.

> This repository is a learning and portfolio project. The automated API testing suite is being expanded progressively as the testing work continues.

## Tech Stack

- Frontend: Vue 3, Vue Router, Pinia, Element Plus, Axios, ECharts, Vite
- Backend: Django, Django REST Framework, Simple JWT
- Database: MySQL / local development database configuration
- Testing focus: HTTP API testing, Pytest, Requests, parameterization, assertions, fixtures, token authentication, interface chaining and Allure reporting

## Testing Scope

The testing work focuses on core business APIs such as authentication, equipment information and FEMCA-related analysis data. Test scenarios include normal flows, required fields, invalid parameters, boundary conditions, authentication and business-rule validation.

Planned/ongoing automation structure:

```text
api_tests/
├── conftest.py
├── test_login.py
├── test_equipment.py
├── test_femca.py
├── config/
├── data/
└── utils/
```

The automation suite will be completed incrementally rather than presenting unfinished work as completed functionality.

## Project Structure

```text
.
├── backend/        # Django REST Framework backend
├── frontend/       # Vue 3 frontend
├── api_tests/      # API automation tests (under development)
├── .env.example
├── .gitignore
└── README.md
```

## Local Setup

### Backend

```bash
cd backend
python -m venv venv
# Windows: venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Before running, configure environment variables based on `.env.example`. Do not commit real secrets to GitHub.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Automation

The API automation portion is intended to demonstrate a maintainable test workflow using Python + Pytest + Requests. As the project progresses, this section will include reusable request handling, fixtures, test-data/config separation, parameterized cases, assertions, authentication/token handling, API chaining and Allure reports.

## Security Note

Local virtual environments, `node_modules`, local databases, IDE files, test reports and environment secrets are excluded from version control through `.gitignore`.
