# FeelInk Setup Guide

Complete setup instructions for FeelInk development environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start with Docker](#quick-start-with-docker)
3. [Database Setup](#database-setup)
4. [Manual Setup](#manual-setup)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** and **Docker Compose** (recommended)
  - Docker Desktop for Mac/Windows
  - Or Docker Engine + Docker Compose for Linux
- **Node.js** 18+ (for frontend development without Docker)
- **Python** 3.11+ (for backend development without Docker)
- **PostgreSQL** 14+ (if not using Docker)

---

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/BBest24-OU/feelink_app.git
cd feelink_app
```

### 2. Configure Environment Variables

The project includes default environment variables in:
- `/frontend/.env` - Frontend configuration
- `/.env` - Backend configuration (used by Docker Compose)

**Default values should work for local development.**

### 3. Start All Services

```bash
docker-compose up -d
```

This starts:
- **PostgreSQL** (port 5433) - Database
- **Redis** (port 6380) - Cache
- **Backend** (port 8000) - FastAPI server
- **Frontend** (port 5173) - Svelte dev server

### 4. **IMPORTANT: Run Database Migrations**

⚠️ **This step is required on first setup!** The database tables won't exist until you run migrations.

```bash
# Run migrations inside the backend container
docker exec feelink_backend alembic upgrade head
```

Or using Docker Compose:

```bash
docker-compose exec backend alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial_schema, Initial database schema
```

### 5. Verify Setup

**Frontend:** http://localhost:5173
**Backend API:** http://localhost:8000
**API Documentation:** http://localhost:8000/docs

**Test registration:**
1. Navigate to http://localhost:5173/#/register
2. Create an account with:
   - Email: your-email@example.com
   - Password: Must contain at least one uppercase letter (e.g., `Password123`)

---

## Database Setup

### Database Schema

The initial migration creates the following tables:
- **users** - User accounts and authentication
- **metrics** - Custom tracking metrics (physical, psychological, etc.)
- **entries** - Daily log entries
- **entry_values** - Values for each metric in daily entries

### Migration Commands

```bash
# Check current migration status
docker exec feelink_backend alembic current

# View migration history
docker exec feelink_backend alembic history

# Upgrade to latest migration
docker exec feelink_backend alembic upgrade head

# Rollback one migration
docker exec feelink_backend alembic downgrade -1

# Rollback all migrations
docker exec feelink_backend alembic downgrade base
```

### Creating New Migrations

```bash
# Auto-generate migration from model changes
docker exec feelink_backend alembic revision --autogenerate -m "Description of changes"

# Create empty migration
docker exec feelink_backend alembic revision -m "Description of changes"
```

### Database Access

**Connect to PostgreSQL:**
```bash
# Using docker exec
docker exec -it feelink_postgres psql -U feelink_user -d feelink_db

# Using local psql (if installed)
psql -h localhost -p 5433 -U feelink_user -d feelink_db
# Password: feelink_password
```

**Useful SQL queries:**
```sql
-- List all tables
\dt

-- View users table
SELECT * FROM users;

-- View metrics table
SELECT * FROM metrics;

-- Check database size
SELECT pg_size_pretty(pg_database_size('feelink_db'));
```

---

## Manual Setup

If you prefer not to use Docker:

### Backend Setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL:**
   ```bash
   # Create database
   createdb feelink_db

   # Create user (if needed)
   psql -c "CREATE USER feelink_user WITH PASSWORD 'feelink_password';"
   psql -c "GRANT ALL PRIVILEGES ON DATABASE feelink_db TO feelink_user;"
   ```

4. **Configure environment variables:**
   ```bash
   # Create .env file in backend directory
   cat > .env << EOF
   DATABASE_URL=postgresql://feelink_user:feelink_password@localhost:5432/feelink_db
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your-secret-key-change-in-production
   ENVIRONMENT=development
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   EOF
   ```

5. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   # Create .env file in frontend directory
   echo "VITE_API_URL=http://localhost:8000" > .env
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

---

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://feelink_user:feelink_password@postgres:5432/feelink_db

# Redis Cache
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Environment
ENVIRONMENT=development  # Options: development, staging, production

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)

```bash
# Backend API URL (without /api/v1 suffix)
VITE_API_URL=http://localhost:8000
```

⚠️ **Important:** `VITE_API_URL` should NOT include `/api/v1` - the client adds this automatically.

---

## Troubleshooting

### Issue: "relation 'users' does not exist"

**Problem:** Database migrations haven't been run.

**Solution:**
```bash
docker exec feelink_backend alembic upgrade head
```

### Issue: "404 Not Found" on API requests

**Problem:** Incorrect API URL with duplicate `/api/v1`.

**Solution:** Verify `VITE_API_URL` in `frontend/.env`:
```bash
# ✅ Correct
VITE_API_URL=http://localhost:8000

# ❌ Wrong
VITE_API_URL=http://localhost:8000/api/v1
```

After changing `.env`, restart the frontend dev server.

### Issue: "422 Validation Error" on registration

**Common causes:**
1. **Password requirements:** Must contain at least one uppercase letter
2. **Email format:** Must be valid email address
3. **Language format:** Should be `"en"` or `"pl"` (not `"en-US"` or `"pl-PL"`)

**Solution:** The frontend automatically handles language conversion, but ensure you're using a password with an uppercase letter (e.g., `Password123`).

### Issue: Docker containers not starting

**Check logs:**
```bash
docker-compose logs backend
docker-compose logs postgres
docker-compose logs frontend
```

**Restart services:**
```bash
docker-compose down
docker-compose up -d
```

### Issue: Port conflicts

If ports 5173, 8000, 5433, or 6380 are already in use:

**Option 1:** Stop conflicting services
**Option 2:** Change ports in `docker-compose.yml`:

```yaml
ports:
  - "5174:5173"  # Frontend: change from 5173 to 5174
  - "8001:8000"  # Backend: change from 8000 to 8001
  # etc.
```

Then update `VITE_API_URL` in `frontend/.env` accordingly.

### Issue: Database connection refused

**Check PostgreSQL is running:**
```bash
docker-compose ps postgres
```

**Verify connection from backend:**
```bash
docker exec feelink_backend python -c "from app.database import engine; print(engine.connect())"
```

### Issue: Frontend build errors

**Clear cache and reinstall:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Issue: Backend module not found

**Rebuild Docker image:**
```bash
docker-compose down
docker-compose build backend
docker-compose up -d
```

---

## Development Workflow

### Daily Development

1. **Start services:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f backend  # Backend logs
   docker-compose logs -f frontend # Frontend logs
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

### Running Tests

**Backend:**
```bash
docker exec feelink_backend pytest
docker exec feelink_backend pytest --cov=app tests/
```

**Frontend:**
```bash
cd frontend
npm run test
npm run test:e2e
```

### Database Reset

⚠️ **Warning:** This will delete all data!

```bash
# Rollback all migrations
docker exec feelink_backend alembic downgrade base

# Re-run migrations
docker exec feelink_backend alembic upgrade head

# Or reset entire database
docker-compose down -v  # Removes volumes
docker-compose up -d
docker exec feelink_backend alembic upgrade head
```

---

## Next Steps

After successful setup:

1. ✅ Create a test account via registration
2. ✅ Explore the API documentation at http://localhost:8000/docs
3. ✅ Read the [PROJECT_OVERVIEW.md](/docs/PROJECT_OVERVIEW.md)
4. ✅ Review the [ARCHITECTURE.md](/docs/ARCHITECTURE.md)
5. ✅ Check the [CLAUDE.md](/CLAUDE.md) for development agent collaboration

---

## Getting Help

- **Documentation:** [`/docs`](/docs) directory
- **Issues:** [GitHub Issues](https://github.com/BBest24-OU/feelink_app/issues)
- **Discussions:** [GitHub Discussions](https://github.com/BBest24-OU/feelink_app/discussions)

---

**Happy coding! 🚀**
