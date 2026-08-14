# SearchCraft Commands & Workflows

This document outlines the most common commands and workflows you'll need when developing, testing, and running SearchCraft.

## 🐳 Docker Workflow (Recommended)

The easiest way to run the entire stack (PostgreSQL, Meilisearch, API, Worker) is using Docker Compose. We have provided a `Makefile` for convenience.

```bash
# 1. Start all services in the background
make up

# 2. Run initial database migrations and create the outbox triggers
make migrate

# 3. Seed the database with 1000 random test products
make seed

# 4. Follow the logs for all services (API, worker, db, search engine)
make logs

# 5. Run the test suite inside the docker container
make test

# 6. Stop all services
make down
```

## 🐍 Local Python Virtual Environment Setup

While Docker handles the complete stack, you might want a local Python virtual environment (`venv`) to get IDE autocompletion, linting, or to run the Python apps directly on your host machine for faster debugging.

### 1. Create and Activate the Virtual Environment

Since you are on Windows, use the following commands (PowerShell/CMD):

```bash
# Create the virtual environment in the project root
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

*Note: For macOS/Linux, the activation command is `source venv/bin/activate`.*

### 2. Install Dependencies

Ensure your virtual environment is activated, then run:
```bash
pip install -r requirements.txt
```

### 3. Running Services Locally

If you run the Python services locally, you still need PostgreSQL and Meilisearch running via Docker. 

First, ensure the infrastructure is running:
```bash
# In one terminal, just start the DB and Meilisearch
docker-compose up -d postgres meilisearch
```

Then, run the API server locally:
```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

And in another terminal (with the venv activated), run the background worker:
```bash
python -m src.worker
```

### 4. Running Tests Locally

To run the pytest suite from your local machine:
```bash
pytest tests/
```

### 5. Environment Variables

If running locally, the services will default to the values in `src/config.py`. Make sure you have copied `.env.example` to `.env` so both local and Docker services use the correct credentials.

```bash
copy .env.example .env
```
