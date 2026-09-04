# AI-Assisted Task Review Application

A small full-stack task review application built with Django REST Framework and React. Users can view and filter tasks, update their status, and request an AI-assisted analysis with a structured result.

## Tech Stack

* **Backend:** Python, Django, Django REST Framework
* **Frontend:** React, Vite, JavaScript, CSS
* **Database:** SQLite
* **AI:** Deterministic mock AI provider with a provider abstraction
* **HTTP:** Browser Fetch API

## Features

* View tasks with title, description, priority, status, and creation date
* Filter tasks by status
* Update task status with validation
* Analyse tasks using AI
* Display structured AI results:

  * Category
  * Priority
  * Summary
  * Recommended action
* Handle AI/API failures gracefully
* Automated backend tests

## Architecture

```text
React UI
   |
Django REST API
   |
Task Analysis Service
   |
AI Provider
   |
Structured Analysis Result
   |
React UI
```

The AI provider is abstracted so the mock implementation can be replaced with a real LLM provider later.

## API

| Method | Endpoint                   | Purpose                |

| GET    | `/api/tasks/`              | List tasks             |
| GET    | `/api/tasks/?status=NEW`   | Filter tasks           |
| PATCH  | `/api/tasks/{id}/status/`  | Update task status     |
| POST   | `/api/tasks/{id}/analyse/` | Analyse a task with AI |

Supported statuses:

```text
NEW
IN_PROGRESS
COMPLETED
```

AI analysis returns:

```json
{
  "category": "DOCUMENT_REQUEST",
  "priority": "HIGH",
  "summary": "Customer needs to provide the missing document required for their application.",
  "recommendedAction": "Request the missing document from the customer."
}
```

## AI Approach

The project currently uses a deterministic *mock AI provider* so it can run locally without API keys or external costs.

The provider is separated from the analysis service, making it possible to integrate a real LLM later without changing the overall API flow.

Expected AI failures are handled with appropriate API responses rather than crashing the application.

## Running Locally

## Backend

```bash
cd backend

python -m venv .venv
source .venv/bin/activate

pip install django djangorestframework django-cors-headers

python manage.py migrate
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000/
```

## Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173/
```

## Testing

Backend tests:

```bash
cd backend
python manage.py test
```

Current result:

```text
Ran 3 tests
OK
```

The tests cover:

* Valid status update
* Invalid status rejection
* AI provider failure

Frontend production build:

```bash
cd frontend
npm run build
```

The production build was also verified successfully.

## Future Improvements

* Integrate a real LLM provider
* Add environment-based AI configuration
* Add authentication and authorization
* Add frontend automated tests
* Add pagination and API documentation
* Add logging, monitoring, and rate limiting
* Persist AI analysis results if required

## AI Coding Tools Used

ChatGPT,Claude,codex was used as a coding assistant for architecture planning, implementation, debugging, testing, and documentation.

AI-generated code was not accepted blindly. The implementation was manually reviewed and verified by:

Running Django system checks
Running the Django automated test suite
Running the React/Vite production build
Manually testing task listing and filtering
Manually testing task status updates
Manually testing AI analysis
Checking AI provider failure handling
Reviewing the final project structure
