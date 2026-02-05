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