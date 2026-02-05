# Enterprise Authentication Database Schema

This repository contains the PostgreSQL database schema for a generic authentication system called `enterprise-auth`.

## Overview

The authentication schema includes all necessary tables and relationships for managing users, accounts, roles, permissions, and authentication flows.

## Database Setup

### Prerequisites

- PostgreSQL 12+
- Admin credentials (username: `admin`, password: `admin`)

### Creating the Database

1. Connect to PostgreSQL as admin:
   ```bash
   psql -h localhost -U admin
   ```

2. Create the database:
   ```sql
   CREATE DATABASE "enterprise-auth";
   \c enterprise-auth
   ```

3. Run the schema script:
   ```bash
   psql -h localhost -U admin -d "enterprise-auth" -f auth_schema.sql
   ```

## Schema Structure

### Tables

1. **accounts** - Core account information (username, email, password hash, etc.)
2. **users** - Extended user profile information linked to accounts
3. **roles** - Different roles that define sets of permissions
4. **permissions** - Individual permissions that can be assigned to roles
5. **role_permissions** - Junction table linking roles to permissions
6. **user_roles** - Junction table linking users to roles
7. **sessions** - Active user sessions
8. **refresh_tokens** - Refresh tokens for maintaining sessions
9. **password_reset_tokens** - Tokens for password reset functionality
10. **email_verification_tokens** - Tokens for email verification

### Key Features

- UUID primary keys for distributed systems
- Automatic timestamp updates
- Flexible role and permission system
- Support for OAuth providers
- Session management
- Password reset and email verification flows

## Default Data

The schema includes:

- Three default roles: Administrator, User, Moderator
- Common permissions for user management
- Proper indexes for performance
- Automatic timestamp updates via triggers

## Usage Examples

### Creating a new user account:

```sql
-- First, create an account
INSERT INTO accounts (username, email, password_hash) 
VALUES ('johndoe', 'john@example.com', '$2b$12$LQv3c1kZpVzXJt4uR2H4PuOf.j3aY5F2b1x3Y3L1vZ4pR5G6H7I8J');

-- Then create the user profile
INSERT INTO users (account_id, first_name, last_name, display_name) 
SELECT id, 'John', 'Doe', 'John Doe' FROM accounts WHERE username = 'johndoe';
```

### Assigning a role to a user:

```sql
-- Assign the 'user' role to John Doe
INSERT INTO user_roles (user_id, role_id) 
VALUES 
  ((SELECT u.id FROM users u JOIN accounts a ON u.account_id = a.id WHERE a.username = 'johndoe'),
   (SELECT id FROM roles WHERE slug = 'user'));
```

### Checking user permissions:

```sql
-- Find all permissions for a specific user
SELECT DISTINCT p.name, p.slug, p.resource, p.action
FROM users u
JOIN user_roles ur ON u.id = ur.user_id
JOIN role_permissions rp ON ur.role_id = rp.role_id
JOIN permissions p ON rp.permission_id = p.id
WHERE u.id = 'some-user-id' AND ur.expires_at > NOW();
```

## Security Considerations

- Passwords should always be stored as bcrypt or similar hashed values
- Session tokens and refresh tokens should be properly secured
- Regular cleanup of expired tokens is recommended
- Use connection pooling with secure credentials in production

## Notes

- The schema uses UUIDs as primary keys for better scalability
- All timestamps are stored in UTC with timezone information
- The `updated_at` fields are automatically managed by triggers
- Default roles and permissions can be customized for specific use cases
# Enterprise PostgreSQL Docker Image

This is a Docker image for deploying PostgreSQL with default admin credentials.

## Default Credentials
- Username: `admin`
- Password: `admin`
- Database: `enterprise_db`

## Quick Start with Docker Compose

1. Navigate to the `src/enterprise-postgres` directory
2. Run the following command:

```bash
docker-compose up -d
```

This will start the PostgreSQL server on port 5432.

## Building the Image Manually

To build the image manually:

```bash
docker build -t enterprise-postgres .
```

To run the container:

```bash
docker run -d \
  --name enterprise-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=enterprise_db \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  enterprise-postgres
```

## Data Persistence

The Docker Compose file includes a named volume (`postgres_data`) to persist your data between container restarts.

## Custom Initialization

The `init.sql` file in this directory will be executed when the container starts for the first time to initialize the database with any necessary tables or data.
