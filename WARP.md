# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Install dependencies (choose one)
pip install -r requirements.txt  # Traditional pip
uv sync                          # Using uv (faster)
```

### Running the Application
```bash
# Start development server with hot reload
uvicorn main:app --reload

# Start server on specific host/port
uvicorn main:app --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --workers 4
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Run a single test function
python -m pytest tests/test_routes.py::test_register -v

# Run tests with coverage
python -m pytest tests/ --cov=api --cov-report=html
```

### Database Management
```bash
# Database is automatically created on first run
# SQLite database file: polls.db
# Test database: test_polls.db (automatically managed by tests)

# To reset database, simply delete the file:
rm polls.db
```

### API Documentation
```bash
# Access interactive Swagger UI
# http://127.0.0.1:8000/docs

# Access ReDoc documentation  
# http://127.0.0.1:8000/redoc

# Get OpenAPI schema
curl http://127.0.0.1:8000/openapi.json
```

## Architecture Overview

### Project Structure
The codebase follows a modular FastAPI architecture with clear separation of concerns:

```
api/                    # Core application package
├── __init__.py        
├── auth.py            # JWT authentication & password hashing
├── database.py        # SQLAlchemy database configuration
├── models.py          # SQLAlchemy ORM models
├── routes.py          # FastAPI route handlers
└── schemas.py         # Pydantic models for request/response
main.py                # Application entry point
tests/                 # Test suite
openapi.yaml          # OpenAPI 3.1 specification
```

### Data Models & Relationships
Four core entities with the following relationships:
- **User**: Has many polls, has many votes
- **Poll**: Belongs to user, has many options
- **Option**: Belongs to poll, has many votes  
- **Vote**: Links user to option (with poll relationship through option)

Key business rules:
- Users can only vote once per poll (existing votes are updated, not duplicated)
- Only poll owners can delete their polls
- Polls require minimum 2 options
- Cascading deletes: Poll deletion removes options and votes

### Authentication Flow
Uses JWT bearer tokens with the following pattern:
1. User registers via `/register` endpoint
2. User logs in via `/login` with form data (OAuth2PasswordRequestForm)
3. Server returns JWT token valid for 30 minutes
4. Protected endpoints require `Authorization: Bearer <token>` header
5. Token contains username in `sub` claim, validated against database

### Key Technical Details
- **Database**: SQLite with SQLAlchemy ORM (easy to switch to PostgreSQL/MySQL)
- **Password Security**: bcrypt hashing via passlib
- **Token Security**: JWT with configurable secret key via environment variables
- **API Standards**: Follows OpenAPI 3.1 specification
- **Testing**: Uses FastAPI TestClient with separate test database
- **Environment**: Python 3.13+, managed with uv or pip

### Protected vs Public Endpoints
**Authentication Required:**
- POST /polls (create poll)
- POST /polls/{id}/vote (vote on poll)  
- DELETE /polls/{id} (delete own poll)

**Public Access:**
- POST /register, POST /login (auth endpoints)
- GET /polls, GET /polls/{id} (view polls)
- GET /polls/{id}/results (view results)

### Environment Configuration
Optional environment variables in `.env` file:
- `SECRET_KEY`: JWT signing secret (defaults to "supersecretkey")

### Development Notes
- Database tables are auto-created on application startup
- Tests use dependency injection to override database with test instance
- Vote updates (not inserts) when user votes again on same poll
- UTC timestamps for created_at fields
- SQLAlchemy relationships use appropriate cascade settings for data integrity