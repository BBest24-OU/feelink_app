# FeelInk - Development Guide

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Make (optional, for convenience commands)

### First Time Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd feelink_app
   ```

2. **Create environment files**
   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. **Start the development environment**
   ```bash
   make start
   # OR
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

### Development Workflow

#### Start services
```bash
make start
```

#### View logs
```bash
make logs              # All services
make logs-backend      # Backend only
make logs-frontend     # Frontend only
```

#### Stop services
```bash
make stop
```

#### Clean up (remove containers and volumes)
```bash
make clean
```

#### Run database migrations
```bash
make migrate                        # Apply migrations
make migrate-create                 # Create new migration
```

#### Access shells
```bash
make shell-backend     # Backend container bash
make shell-frontend    # Frontend container sh
make db-shell          # PostgreSQL shell
```

## 📁 Project Structure

```
feelink_app/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── analytics/    # Correlation engine
│   │   ├── security/     # Auth & security
│   │   └── utils/        # Utilities
│   ├── migrations/       # Alembic migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Svelte frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Route pages
│   │   ├── stores/      # Svelte stores
│   │   ├── lib/         # Utilities
│   │   └── i18n/        # Translations
│   ├── package.json
│   └── Dockerfile
├── docs/                # Documentation
├── docker-compose.yml
└── Makefile
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Auth**: JWT (python-jose)
- **Validation**: Pydantic
- **Analytics**: NumPy, Pandas, SciPy

### Frontend
- **Framework**: Svelte 4 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **PWA**: vite-plugin-pwa
- **Router**: svelte-spa-router
- **i18n**: svelte-i18n
- **HTTP Client**: Axios
- **Charts**: Chart.js
- **Local Storage**: Dexie.js (IndexedDB)

## 🧪 Testing

### Backend Tests
```bash
docker-compose exec backend pytest
docker-compose exec backend pytest --cov=app  # With coverage
```

### Frontend Tests
```bash
docker-compose exec frontend npm run test
```

## 📝 Development Notes

### Hot Reload
- Both frontend and backend support hot reload
- Changes to source code automatically rebuild and restart

### Database Migrations
- Alembic tracks database schema changes
- Create migrations after modifying models
- Always review generated migrations before applying

### Environment Variables
- Never commit `.env` files
- Update `.env.example` when adding new variables
- Use different values for dev/staging/production

## 🐛 Troubleshooting

### Port already in use
```bash
# Check what's using the port
lsof -i :5173  # Frontend
lsof -i :8000  # Backend

# Stop conflicting services or change ports in docker-compose.yml
```

### Database connection issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs postgres

# Reset database
make clean && make start
```

### Frontend build errors
```bash
# Clear node_modules and rebuild
docker-compose down
rm -rf frontend/node_modules
docker-compose build frontend
docker-compose up -d
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Svelte Documentation](https://svelte.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## 🤝 Contributing

See [ACTION_PLAN.md](./ACTION_PLAN.md) for development stages and priorities.

---

**Status**: STAGE 0 Complete ✅
**Next**: STAGE 1 - Backend Foundation
