# FEMCA Analysis Management Platform

A facilities/equipment FEMCA analysis management platform built with **Vue 3** and **Django REST Framework**.

The application was developed with AI-assisted coding using Trae and is also used as a practical software-testing portfolio project, focusing on **API Testing, API Automation and Test Reporting**.

> This repository is a learning and portfolio project. The API automation suite currently covers selected authentication and equipment-management scenarios and is being expanded progressively.

## Tech Stack

- **Frontend:** Vue 3, Vue Router, Pinia, Element Plus, Axios, ECharts, Vite
- **Backend:** Django, Django REST Framework, Simple JWT
- **Database:** MySQL / local development database configuration
- **API Testing:** Python, Pytest, Requests
- **Test Framework:** Fixtures, Parameterization, Assertions, API Request Encapsulation
- **Test Reporting:** Python Logging, Pytest Hooks, Allure Report

## API Automation Testing

The project includes an implemented API automation suite using **Python + Pytest + Requests**.

### Implemented Test Coverage

The current suite contains **13 automated test cases**.

| Module | Test Scenarios |
|---|---|
| Authentication | Successful login, incorrect username, incorrect password |
| JWT Authentication | Missing token, invalid token |
| Boundary Value Analysis | Equipment name lengths: 199, 200, 201 characters |
| Input Validation | Missing name, null name, invalid equipment-type foreign key |
| Business Rules | Duplicate equipment validation using `equipment_type` and `serial_number` |

The tests validate HTTP status codes, selected response fields and relevant business rules.

### Test Framework Features

- **Request Encapsulation:** Reusable API request functions.
- **Pytest Fixtures:** Shared authentication and equipment-type test data.
- **Parameterization:** Multiple scenarios executed using `pytest.mark.parametrize`.
- **Dynamic Test Data:** UUID-based serial numbers reduce duplicate-data conflicts.
- **Test Data Cleanup:** Created equipment records are deleted after testing.
- **Configuration Management:** Environment variables for credentials and API base URL.
- **Logging:** INFO and ERROR messages for test execution and unexpected responses.
- **Pytest Hooks:** Automatic logging of test-function failures and assertion details.
- **Allure Reporting:** Visual test results, execution steps and selected API response attachments.

## Test Project Structure

The implemented automation code is located in `backend/tests/`.

```text
backend/
├── tests/
│   ├── conftest.py
│   ├── config.py
│   ├── api_client.py
│   ├── login_test_data.py
│   ├── test_login_api.py
│   └── test_equipment_api.py
└── requirements.txt
```

## Local Setup

### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```bat
venv\Scripts\activate
```

Install dependencies and start the backend:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Configure the required database settings and environment variables for your local development environment.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Running Automated API Tests

Ensure the backend service is running and the test account is available.

Configure the following environment variables:

- `FEMCA_USERNAME`: Test account username
- `FEMCA_PASSWORD`: Test account password
- `FEMCA_BASE_URL`: Optional API base URL (default: `http://127.0.0.1:8000`)

From the project root directory, with the backend virtual environment activated:

```bash
pytest backend/tests/ -v
```

## Allure Test Reporting

Generate test results:

```bash
pytest backend/tests/ -v --alluredir=allure-results --clean-alluredir
```

Open the interactive report:

```bash
allure serve allure-results
```

The `allure-pytest` dependency is included in `backend/requirements.txt`.

**Note:** Allure CLI must be installed separately.

The report supports:

- Test execution overview and pass/fail statistics
- Test Suites and individual Test Case details
- Execution Steps
- Selected API Response Body attachments
- Failure details and traceback information

## Latest Regression Test Result

**13 Passed / 13 Executed**

The latest local regression test completed successfully.

This result represents the currently implemented authentication and equipment API tests, not complete coverage of the entire FEMCA platform.

## Security Notes

- Credentials are read from environment variables rather than hardcoded into test scripts.
- JWT tokens and passwords should not be included in logs or report attachments.
- Generated Allure results and reports are excluded from Git version control.
- Local environments, databases and sensitive configuration files should not be committed to GitHub.

## Future Improvements

- Expand automated coverage to additional FEMCA analysis APIs.
- Add more permission and exception-handling scenarios.
- Improve reporting and failure diagnostics.
- Integrate automated test execution into a CI/CD pipeline.