# FeelInk

<div align="center">

**Mental Health & Mood Tracking Made Simple, Insightful, and Yours**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Svelte](https://img.shields.io/badge/Svelte-4+-FF3E00?logo=svelte&logoColor=white)](https://svelte.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PWA](https://img.shields.io/badge/PWA-Enabled-5A0FC8?logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Features](#-features) • [Documentation](#-documentation) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 🎯 What is FeelInk?

**FeelInk** is a Progressive Web Application (PWA) that empowers individuals to track and understand their mental health, mood, and overall well-being through simple daily tracking and advanced statistical analysis.

### The Problem We Solve

**For Patients:**
- ⏱️ Wasting 10-15 minutes of therapy describing "how things are" instead of solving problems
- 🧠 Difficulty remembering mood patterns from weeks ago
- 🔍 Missing hidden correlations between external triggers and mental states
- 💰 Expensive therapy sessions where time = money

**For Healthcare Providers:**
- 📊 Relying on patient memory and subjective recall
- ⏰ Spending valuable session time on data gathering instead of treatment
- 🔎 Difficulty spotting patterns across multiple sessions

### Our Solution

FeelInk transforms mental health tracking from a chore into a powerful diagnostic tool:

- **1-Minute Daily Tracking**: Quick, effortless data entry optimized for mobile
- **Flexible Metrics**: Track what matters to you - symptoms, medications, triggers, self-care, wellness
- **Smart Correlation Engine**: Automatically discover relationships (e.g., "Sleep < 6 hours → irritability next day")
- **Clinical Reports**: One-page PDF summaries with correlations and lag effects for healthcare professionals
- **Data Ownership**: Full export capabilities (CSV, JSON) - your data belongs to you

---

## ✨ Features

### 📊 Personalized Tracking
- **Custom Metrics**: Define what to track across 7 categories (Physical, Psychological, Triggers, Medications, Self-Care, Wellness, Notes)
- **Multiple Value Types**: Range sliders, numbers, yes/no toggles, counts, free text
- **Mobile-First**: Optimized for quick daily logging (<60 seconds)

### 📈 Advanced Analytics
- **Correlation Analysis**: Pearson, Spearman, and Kendall algorithms
- **Lag Correlations**: Discover delayed effects (e.g., "Alcohol → mood decrease 3 days later")
- **Statistical Significance**: P-values and confidence indicators
- **Interactive Visualizations**: Line charts, scatter plots, heatmaps, calendar views

### 🔒 Privacy & Ownership
- **Offline-First**: Works without internet, syncs when available
- **Local Storage**: Data stored on your device (IndexedDB)
- **Full Export**: CSV, JSON, and PDF formats
- **GDPR Compliant**: Your data, your control
- **No Vendor Lock-in**: Export everything, anytime

### 🌍 Internationalization
- **Multi-Language**: Polish and English from day one
- **Locale-Aware**: Date, time, and number formatting
- **Scalable**: Ready for additional languages

### 📱 Progressive Web App
- **Installable**: Add to home screen (iOS, Android, Desktop)
- **Offline Capable**: Full functionality without internet
- **Fast**: Optimized bundle size and load times
- **Responsive**: Works on all screen sizes (320px - 2560px)

---

## 📚 Documentation

Comprehensive documentation is available in the [`/docs`](/docs) directory:

| Document | Description |
|----------|-------------|
| [PROJECT_OVERVIEW.md](/docs/PROJECT_OVERVIEW.md) | Project vision, philosophy, and goals |
| [REQUIREMENTS.md](/docs/REQUIREMENTS.md) | Detailed functional and non-functional requirements |
| [ARCHITECTURE.md](/docs/ARCHITECTURE.md) | Technical architecture and design decisions |
| [DATA_MODEL.md](/docs/DATA_MODEL.md) | Database schema and data structures |
| [CORRELATION_ALGORITHMS.md](/docs/CORRELATION_ALGORITHMS.md) | Statistical methods and algorithms |
| [UI_UX_GUIDELINES.md](/docs/UI_UX_GUIDELINES.md) | Design system and UX principles |
| [PRIVACY_AND_SECURITY.md](/docs/PRIVACY_AND_SECURITY.md) | Privacy and security approach |
| [I18N_STRATEGY.md](/docs/I18N_STRATEGY.md) | Internationalization strategy |

---

## 🤖 Development Agents

FeelInk is developed with the help of **18 specialized AI agents**, each with specific expertise:

- **Technical**: Frontend Dev, Backend Dev, Data Scientist, DevOps, Security Engineer, QA Engineer
- **Design**: UI/UX Designer, Visual Designer, Accessibility Specialist
- **Domain**: Clinical Psychologist, Medical Advisor, Privacy Advisor
- **Product**: Product Manager, Project Coordinator
- **Content**: Technical Writer, UX Writer, i18n Specialist
- **Specialized**: DataViz Specialist, Performance Engineer

👉 **Learn more**: [CLAUDE.md](/CLAUDE.md) - Full agent descriptions and collaboration matrix

---

## 🚀 Quick Start

> **Note**: FeelInk is currently in active development (MVP Phase). The following instructions will be updated as the project progresses.

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.11+ (for backend)
- **PostgreSQL** 14+ (for database)
- **Docker** (optional, for containerized development)

### Development Setup

#### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/BBest24-OU/feelink_app.git
cd feelink_app

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Option 2: Manual Setup

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# Access at http://localhost:5173
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
# Access at http://localhost:8000
```

**Database:**
```bash
# Create PostgreSQL database
createdb feelink

# Run migrations
cd backend
alembic upgrade head
```

### Running Tests

**Frontend:**
```bash
cd frontend
npm run test
npm run test:e2e
```

**Backend:**
```bash
cd backend
pytest
pytest --cov=app tests/
```

---

## 🏗️ Project Structure

```
feelink_app/
├── frontend/              # Svelte PWA application
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Route pages
│   │   ├── stores/        # State management (Svelte stores)
│   │   ├── lib/           # Utilities, API clients
│   │   ├── i18n/          # Translation files
│   │   └── assets/        # Static assets
│   ├── public/            # Public static files
│   └── vite.config.ts     # Vite configuration
│
├── backend/               # FastAPI Python application
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── analytics/     # Correlation engine
│   │   ├── security/      # Authentication & authorization
│   │   └── utils/         # Utilities
│   ├── migrations/        # Alembic database migrations
│   └── requirements.txt   # Python dependencies
│
├── docs/                  # Comprehensive documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   ├── CORRELATION_ALGORITHMS.md
│   ├── UI_UX_GUIDELINES.md
│   ├── PRIVACY_AND_SECURITY.md
│   └── I18N_STRATEGY.md
│
├── agents/                # Specialized development agent definitions
│   └── [18 agent directories with expertise areas]
│
├── CLAUDE.md              # Agent collaboration guide
├── README.md              # This file
├── docker-compose.yml     # Development environment
└── LICENSE                # MIT License
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: [Svelte 4+](https://svelte.dev/) - Reactive, lightweight, fast
- **Build Tool**: [Vite](https://vitejs.dev/) - Lightning-fast development
- **Language**: [TypeScript](https://www.typescriptlang.org/) - Type safety
- **PWA**: [Workbox](https://developers.google.com/web/tools/workbox) - Service Worker management
- **Storage**: [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API) - Offline data
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- **Charts**: [Chart.js](https://www.chartjs.org/) + [D3.js](https://d3js.org/) - Data visualization
- **i18n**: [svelte-i18n](https://github.com/kaisermann/svelte-i18n) - Internationalization

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast Python web framework
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI server
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Relational database
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- **Analytics**: [NumPy](https://numpy.org/), [Pandas](https://pandas.pydata.org/), [SciPy](https://scipy.org/) - Statistical analysis
- **Auth**: [JWT](https://jwt.io/) + [bcrypt](https://github.com/pyca/bcrypt/) - Authentication
- **Cache**: [Redis](https://redis.io/) - Session and data caching

### Infrastructure
- **Containerization**: [Docker](https://www.docker.com/) - Consistent environments
- **CI/CD**: [GitHub Actions](https://github.com/features/actions) - Automated testing and deployment
- **Monitoring**: [Sentry](https://sentry.io/) - Error tracking

---

## 🎨 Design Principles

1. **Clarity over Complexity**: Clean, uncluttered interface
2. **Speed**: Fast load times, instant interactions (<60s daily log)
3. **Accessibility**: WCAG 2.1 Level AA compliance
4. **Mobile-First**: Optimized for touch screens and small devices
5. **Professional Aesthetics**: Trust-building visual design for clinical use

---

## 🗺️ Roadmap

### Phase 1: Foundation (MVP) - Q1 2025
- ✅ Project setup and architecture
- ✅ Comprehensive documentation
- 🚧 Metric management system
- 🚧 Daily logging interface (mobile-optimized)
- 🚧 Local data storage (IndexedDB)
- 🚧 Basic visualizations (charts)
- 🚧 PWA functionality (offline-first)

### Phase 2: Analytics - Q2 2025
- ⏳ Correlation engine (Pearson, Spearman, Kendall)
- ⏳ Lag correlation analysis
- ⏳ Advanced visualizations (interactive charts)
- ⏳ PDF report generation

### Phase 3: Cloud & Sync - Q3 2025
- ⏳ User authentication system
- ⏳ Cloud data synchronization
- ⏳ Multi-device support
- ⏳ Data export (CSV, JSON)

### Phase 4: Enhancement - Q4 2025
- ⏳ Advanced lag/cross-correlations
- ⏳ AI-powered insights
- ⏳ Wearable device integration
- ⏳ Dark mode

**Legend**: ✅ Complete | 🚧 In Progress | ⏳ Planned

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or suggesting enhancements, your help is appreciated.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow the code style and conventions used in the project
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📊 Success Metrics

We measure success by:
- **User Engagement**: >70% daily completion rate
- **Speed**: <1 minute average log completion time
- **Usability**: SUS score >75
- **Insights**: Users discovering ≥3 meaningful correlations within 30 days
- **Data Ownership**: High CSV/JSON export rates

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with ❤️ for mental health awareness
- Inspired by quantified self movement and evidence-based therapy
- Special thanks to all contributors and the open-source community

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/BBest24-OU/feelink_app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BBest24-OU/feelink_app/discussions)
- **Email**: support@feelink.com (coming soon)

---

<div align="center">

**Made with 🧠 by the FeelInk Team**

⭐ Star this repo if you find it helpful!

</div>
