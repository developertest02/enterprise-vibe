# Enterprise Auth API

This is the authentication API service for the Enterprise Vibe platform. It handles user registration, authentication, and account management.

## Features
- User registration via REST API
- Secure password hashing with bcrypt
- PostgreSQL integration with SQLAlchemy ORM
- Input validation with Pydantic models
- Comprehensive error handling

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables by copying `.env.example` to `.env` and filling in values
3. Make sure PostgreSQL database is running with the appropriate schema (found in `../enterprise-postgres/auth_schema.sql`)
4. Run the application: `python app.py`

## API Endpoints
- `GET /` - Health check endpoint
- `POST /register` - Register a new user account

## Registration Request Format
```json
{
  "email": "user@example.com",
  "username": "unique_username",
  "password": "SecurePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "display_name": "John Doe"
}
```

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

### Username Requirements
- Length between 3-50 characters
- Only alphanumeric characters, underscores, and hyphens allowed