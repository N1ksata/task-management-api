# Task Management API

A professional, production-ready REST API built with FastAPI and PostgreSQL for task management.

## Features

✨ **Core Features**
- User authentication with JWT tokens
- Create, read, update, and delete tasks
- Task status management (pending, in_progress, completed)
- Priority levels for tasks
- User-specific task filtering
- Comprehensive error handling
- Input validation with Pydantic

🏗️ **Architecture**
- Async SQLAlchemy ORM integration
- Database migrations with Alembic
- Clean separation of concerns (models, schemas, routes, services)
- Environment-based configuration
- Comprehensive logging

🧪 **Quality Assurance**
- Unit and integration tests
- Code validation with Pydantic
- Database constraint enforcement

🐳 **Deployment**
- Docker and Docker Compose support
- CI/CD ready with GitHub Actions
- Production-grade configuration

## Project Structure

```
task-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py              # Configuration management
│   ├── database.py            # Database setup
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── routes/                # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── tasks.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── security.py
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── test_users.py
├── migrations/                # Alembic migrations
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Docker and Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/N1ksata/task-management-api.git
   cd task-management-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Using Docker

```bash
docker-compose up -d
```

This will start both the FastAPI server and PostgreSQL database.

## API Documentation

- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## Authentication

The API uses JWT (JSON Web Token) authentication. To use protected endpoints:

1. Register a user via `/api/v1/auth/register`
2. Login via `/api/v1/auth/login` to get an access token
3. Include the token in the Authorization header: `Authorization: Bearer <token>`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile
- `DELETE /api/v1/users/me` - Delete current user account

### Tasks
- `GET /api/v1/tasks` - List all tasks (paginated)
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task
- `PATCH /api/v1/tasks/{task_id}/status` - Update task status

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Environment Variables

See `.env.example` for all available configuration options:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing secret
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `APP_NAME` - Application name
- `DEBUG` - Enable debug mode

## Database Migrations

Using Alembic for schema management:

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## Development

### Code Style
The project follows PEP 8 standards. Format code using:
```bash
pip install black
black app/ tests/
```

### Type Checking
```bash
pip install mypy
mypy app/
```

## Deployment

See `docker-compose.yml` for production setup. The application is containerized and ready for deployment on platforms like:
- Heroku
- AWS (ECS, Elastic Beanstalk)
- Google Cloud Run
- DigitalOcean App Platform
- Kubernetes

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please open an issue on GitHub.
