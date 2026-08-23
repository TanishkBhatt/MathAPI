# MathAPI - API Services

> A RESTful API service designed for students and developers pursuing mathematics and related fields. Provides structured access to topic explanations, step-by-step worked examples, practice questions, and concise formula sheets across various branches of mathematics.

[![Documentations](https://img.shields.io/badge/Documentation-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://mathapi.vercel.app/docs)

---

## Table of Contents

- [Key Features](#features)
- [Routes](#routes)
- [Project Structure](#project-structure)
- [Tech Stack Used](#tech-stack)
- [Quick Start](#quick-start)
- [Run Project Locally](#running-locally)
- [Contribution](#contribution)
- [Author And Credits](#author-and-credits)

---

## Features

### Topic Catalog
Browse all available mathematics topics with metadata including difficulty level, branch classification, prerequisites, and related topics.

### Detailed Explanations
Get in-depth topic explanations covering definitions, origins, real-world applications, and step-by-step breakdowns.

### Worked Examples
Access fully solved examples with key observations, concept mappings, formula references, and solution interpretations.

### Practice Questions
Retrieve multiple-choice questions with difficulty and type filters to test your understanding.

### Formula Sheets
Fetches concise formula collections for any topic in both plain text and LaTeX format.

### Learning Sources
Fetches selected learning sources (a website or a youtube video) for that particular topic.

### LaTeX Support
All mathematical expressions are **LaTeX** coded for better rendering and user experience.

### API Key Authentication
Register with a username and email to receive a unique API key for authenticated access. Keys are valid for **6 months** from registration; expired keys return **UNAUTHORIZED_401** and must be re-created.

### API Key Limiting
A user can hit only **100 GET requests** on Get API routes with an API Key per hour.

### Daily Challenge
Get **3 daily challenge problems** — one Beginner, one Intermediate, and one Advanced — randomly assigned and shared globally for the day.

### Random Question
Fetch a single random question from any topic, any difficulty, any type in one call.

### Interactive Docs
Full Swagger UI at **/docs** and ReDoc at **/redoc**.

---

## Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `GET` | `/` | API health check with service info and quick-start guide | ❌ |
| `POST` | `/auth` | Register with username + email, receive an API key | ❌ |
| `GET` | `/api/v1/topics` | List all topics with metadata and resource counts | ✅ |
| `GET` | `/api/v1/explanation` | Get topic explanation with optional formulae, examples, questions, learning sources | ✅ |
| `GET` | `/api/v1/examples` | Get worked examples for a topic | ✅ |
| `GET` | `/api/v1/questions` | Get practice questions with optional difficulty & type filters | ✅ |
| `GET` | `/api/v1/formulae` | Get all formulae for a topic | ✅ |
| `GET` | `/api/v1/sources` | Get all learning sources for a topic | ✅ |
| `GET` | `/api/v1/daily-challenge` | Get 3 daily challenge problems — one per difficulty level | ✅ |
| `GET` | `/api/v1/random-question` | Get a single random question from any topic | ✅ |

---

## Project Structure

```
MathAPI/
  ├── main.py                     # FastAPI app entry point
  ├── .env                        # Environment variables (not tracked) 
  ├── config.py                   # Environment variables settings
  │
  ├── controllers/
  │   └── auth/                   # User registration logic
  │       └── auth.py
  │   └── api/v1/                 # Main Backend Logic
  │
  ├── models/
  │   ├── home.py                 # Home response schema
  │   ├── errors.py               # API Errors response schema
  │   └── auth/                   # Auth request/response schemas
  │       └── auth.py
  │   ├── api/v1/                 # API response Pydantic models
  │   └── components/
  │       ├── helpers.py          # Shared Enums and BaseModels
  │       └── main.py             # Composite models - Topic, Explain, Example, Question
  │
  ├── routes/
  │   ├── home.py                 # GET /
  │   └── auth/
  │       └── auth.py             # POST /auth
  │   └── api/v1/
  │           ├── topics.py              # GET /topics
  │           ├── explanation.py         # GET /explain
  │           ├── examples.py            # GET /examples
  │           ├── questions.py           # GET /questions
  │           ├── formulae.py            # GET /formulae
  │           ├── sources.py             # GET /sources
  │           ├── daily_challenge.py     # GET /daily-challenge
  │           └── random_question.py     # GET /random-question
  │
  ├── utils/                      # Database, API auth and limiter functions
  ├── tests/                      # Pytest integration tests
  │
  ├── pyproject.toml                  # UV based dependency management
  ├── requirements.txt                # PIP based dependency management
  ├── vercel.json                     # Deployment config
  ├── .gitignore                      # Untracked files config
  └── README.md                       # Documentation
```

---

## Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) — Python web framework |
| **Server** | [Uvicorn](https://www.uvicorn.org/) — ASGI server |
| **Database** | [MongoDB](https://www.mongodb.com/) via [PyMongo](https://pymongo.readthedocs.io/) |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) — data validation & settings |
| **Auth** | API key-based ([Hashlib](https://docs.python.org/3/library/hashlib.html), [Secrets](https://docs.python.org/3/library/secrets.html)) |
| **Rate Limiting** | [SlowAPI](https://slowapi.readthedocs.io/) — 100 requests/hour per key |
| **Deployment** | [Vercel](https://vercel.com/) — serverless Python functions |
| **Environment** | [Python](https://python.org) 3.12+, managed with [UV](https://docs.astral.sh/uv/) |

--- 

## Quick Start

### Get your API key
```bash
  curl -X POST "https://mathapi.vercel.app/auth" \
    -H "Content-Type: application/json" \
    -d '{"username": "your_username", "email": "your@email.com"}'
```

### Use the API key to access topics
```bash
  curl "https://mathapi.vercel.app/api/v1/topics?api_key=YOUR_API_KEY"
```

### Explore a specific topic
```bash
  curl "https://mathapi.vercel.app/api/v1/explanation?api_key=YOUR_API_KEY&topic_id=quadratic-equations&include_examples=true&include_questions=true"
```

---

## Running Locally

### Clone the reporitory
```bash
git clone https://github.com/TanishkBhatt/MathAPI.git
```

### Create environment variables
- MathAPI/.env

```python
# Database Connetion URL
DB_CONNECTION_URL=YOUR_MONGODB_URL

# Admin Token
ADMIN_TOKEN=YOUR_ADMIN_TOKEN
```

### Install dependencies
```bash
uv sync
```

### Start development server
```bash
uv run uvs dev
```

### Start production server
```bash
uv run uvs start
```

### Run automated tests
```bash
uv run uvs test
```

---

## Contribution

Found a bug or have a feature request? Open an issue on the [GitHub repository](https://github.com/TanishkBhatt/MathAPI).

---

## Author And Credits
**Tanishk Bhatt** — A Student and A Programmer

[![Portfolio](https://img.shields.io/badge/Portfolio-005571?style=for-the-badge&logo=streamlit&logoColor=white)](https://tanishkbhatt.vercel.app)

---