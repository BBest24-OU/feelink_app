# FeelInk - Action Plan & Implementation Roadmap

## Document Information
- **Version**: 1.0.0
- **Created**: 2025-11-15
- **Status**: Active Development Plan
- **Target**: MVP (Phase 1) Completion

---

## 🎯 Overview

This document outlines the complete implementation strategy for FeelInk MVP (Phase 1), breaking down the development process into manageable stages with clear deliverables, timelines, and responsible agents.

**Total Estimated Time**: 6-8 weeks
**Team**: 18 Specialized AI Agents (see [CLAUDE.md](./CLAUDE.md))

---

## 📊 Development Stages

### **STAGE 0: Project Infrastructure** 🏗️
**Priority**: CRITICAL | **Duration**: 1-2 days
**Agents**: @devops, @backend-dev, @frontend-dev

#### Tasks:

**0.1 Directory Structure**
- Create `frontend/` and `backend/` directories
- Setup `.gitignore` for both environments
- Create `docker-compose.yml` for development environment
- Initialize Git repository structure

**0.2 Backend Setup (Python + FastAPI)**
- Initialize Python project (venv, requirements.txt)
- Setup FastAPI with basic folder structure:
  ```
  backend/
  ├── app/
  │   ├── api/           # API endpoints
  │   ├── models/        # SQLAlchemy models
  │   ├── schemas/       # Pydantic schemas
  │   ├── services/      # Business logic
  │   ├── analytics/     # Correlation engine
  │   ├── security/      # Auth & security
  │   └── utils/         # Utilities
  ├── migrations/        # Alembic migrations
  ├── requirements.txt
  └── main.py
  ```
- Configure Alembic for database migrations
- Setup PostgreSQL in Docker
- Setup Redis for cache/sessions

**0.3 Frontend Setup (Svelte + Vite)**
- Initialize Svelte + TypeScript project
- Configure Vite build tool
- Setup Tailwind CSS
- Basic folder structure:
  ```
  frontend/
  ├── src/
  │   ├── components/    # Reusable UI components
  │   ├── pages/         # Route pages
  │   ├── stores/        # Svelte stores (state)
  │   ├── lib/           # Utilities, API client
  │   ├── i18n/          # Translation files
  │   └── assets/        # Static assets
  ├── public/            # Public static files
  └── vite.config.ts
  ```

**0.4 Development Environment**
- Complete Docker Compose configuration:
  - Frontend service (Vite dev server)
  - Backend service (FastAPI)
  - PostgreSQL database
  - Redis cache
- Easy startup scripts (`npm run dev`, `make start`)
- Environment variables setup (.env files)

#### Deliverables:
- ✅ Working development environment (Docker Compose up)
- ✅ Backend responds on http://localhost:8000
- ✅ Frontend responds on http://localhost:5173
- ✅ Database is accessible and migrations run
- ✅ "Hello World" endpoint works

#### ✅ STAGE 0 - COMPLETED (2025-11-15)

**Completed Tasks:**
- ✅ **0.1 Directory Structure**: Created frontend/, backend/, and all subdirectories
- ✅ **0.2 Backend Setup**:
  - FastAPI project initialized with proper structure
  - requirements.txt with all dependencies (FastAPI, SQLAlchemy, Alembic, etc.)
  - Alembic migrations configured
  - Main app with health check and hello world endpoints
  - Dockerfile for containerization
- ✅ **0.3 Frontend Setup**:
  - Svelte + TypeScript + Vite project initialized
  - Tailwind CSS configured
  - PWA support with vite-plugin-pwa
  - App.svelte with STAGE 0 status display
  - Dockerfile for containerization
- ✅ **0.4 Development Environment**:
  - docker-compose.yml with all 4 services (frontend, backend, postgres, redis)
  - .env.example files for configuration
  - Makefile with convenient development commands
  - DEVELOPMENT.md guide created

**Additional Files Created:**
- `.gitignore` for both frontend and backend
- `Makefile` for easy development commands
- `DEVELOPMENT.md` comprehensive development guide
- Environment example files (`.env.example`)

**Ready for STAGE 1**: Backend Foundation 🐍

---

### **STAGE 1: Backend Foundation** 🐍
**Priority**: HIGH | **Duration**: 3-4 days
**Agents**: @backend-dev, @security-engineer, @data-scientist

#### ✅ STAGE 1 - COMPLETED (2025-11-15)

**Completed Tasks:**
- ✅ **1.1 Database Schema**:
  - Created SQLAlchemy models (User, Metric, Entry, EntryValue)
  - Alembic migration 001_initial_schema.py with all tables
  - All indexes, constraints, and relationships defined
  - Soft delete support for users and metrics

- ✅ **1.2 Authentication System**:
  - Password hashing with bcrypt
  - JWT token generation (access + refresh tokens)
  - Protected route middleware with Bearer authentication
  - User registration and login endpoints
  - Token refresh endpoint

- ✅ **1.3 API Skeleton**:
  - Auth routes: `/api/v1/auth/register`, `/login`, `/refresh`
  - User routes: `/api/v1/users/me` (GET, PATCH, DELETE)
  - Metrics routes: `/api/v1/metrics` (CRUD + archive/unarchive)
  - Entries routes: `/api/v1/entries` (CRUD + date filtering)

- ✅ **1.4 Pydantic Models**:
  - Request schemas: UserRegister, UserLogin, MetricCreate, EntryCreate
  - Response schemas: UserResponse, MetricResponse, EntryResponse
  - Validation: password strength, email format, date validation
  - Type-safe value handling for metrics

- ✅ **1.5 Core Services**:
  - UserService: registration, authentication, profile management
  - MetricService: CRUD operations, archiving, ordering
  - EntryService: daily log management, value type validation
  - Database session management with dependency injection

**Files Created (40+ files):**
```
backend/app/
├── models/
│   ├── base.py (Base + TimestampMixin)
│   ├── user.py
│   ├── metric.py
│   ├── entry.py (Entry + EntryValue)
│   └── __init__.py
├── schemas/
│   ├── user.py
│   ├── metric.py
│   ├── entry.py
│   └── __init__.py
├── security/
│   ├── password.py (bcrypt)
│   ├── jwt.py (token generation)
│   ├── dependencies.py (get_current_user)
│   └── __init__.py
├── services/
│   ├── user_service.py
│   ├── metric_service.py
│   ├── entry_service.py
│   └── __init__.py
├── api/
│   ├── auth.py (register, login, refresh)
│   ├── users.py (profile management)
│   ├── metrics.py (metric CRUD)
│   ├── entries.py (entry CRUD)
│   └── __init__.py
├── utils/
│   └── database.py (session management)
└── main.py (updated with all routers)

migrations/
└── versions/
    └── 001_initial_schema.py
```

**API Endpoints Functional:**
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh
- `GET /api/v1/users/me` - Get current user profile
- `PATCH /api/v1/users/me` - Update profile
- `DELETE /api/v1/users/me` - Delete account
- `GET /api/v1/metrics` - List all metrics
- `POST /api/v1/metrics` - Create metric
- `GET /api/v1/metrics/{id}` - Get metric
- `PATCH /api/v1/metrics/{id}` - Update metric
- `DELETE /api/v1/metrics/{id}` - Archive metric
- `POST /api/v1/metrics/{id}/unarchive` - Unarchive metric
- `GET /api/v1/entries` - List entries (with date filters)
- `POST /api/v1/entries` - Create entry
- `GET /api/v1/entries/{id}` - Get entry
- `GET /api/v1/entries/date/{date}` - Get entry by date
- `PATCH /api/v1/entries/{id}` - Update entry
- `DELETE /api/v1/entries/{id}` - Delete entry

**Ready for STAGE 2**: Frontend Foundation ⚡

---

#### Tasks:

**1.1 Database Schema**
- Create Alembic migrations for core tables:
  - `users` - User accounts
  - `metrics` - Custom user metrics
  - `entries` - Daily log entries
  - `entry_values` - Metric values per entry
- Add indexes for performance optimization
- Define constraints and relationships
- Implement soft delete for metrics (archived flag)

**1.2 Authentication System**
- User registration endpoint (`POST /api/v1/auth/register`)
- Login/logout with JWT tokens (`POST /api/v1/auth/login`)
- Password hashing using bcrypt
- Token refresh mechanism (`POST /api/v1/auth/refresh`)
- Protected route middleware (authentication dependency)
- Password strength validation

**1.3 API Skeleton**
- Authentication routes (`/api/v1/auth/*`)
  - Register, login, logout, refresh token
  - Password reset request/confirm
- User routes (`/api/v1/users/*`)
  - Get/update profile (`/me`)
  - Get/update settings (`/me/settings`)
  - Delete account (`/me`)
- Metrics routes (`/api/v1/metrics/*`)
  - List all metrics (`GET /`)
  - Create metric (`POST /`)
  - Get/update/archive metric (`GET/PATCH/DELETE /{id}`)
- Entries routes (`/api/v1/entries/*`)
  - List entries with filters (`GET /`)
  - Create entry (`POST /`)
  - Get/update/delete entry (`GET/PATCH/DELETE /{id}`)
  - Get entry by date (`GET /date/{date}`)

**1.4 Pydantic Models**
- Request models (validation schemas):
  - `UserRegister`, `UserLogin`, `UserUpdate`
  - `MetricCreate`, `MetricUpdate`
  - `EntryCreate`, `EntryUpdate`
- Response models:
  - `UserResponse`, `TokenResponse`
  - `MetricResponse`, `MetricListResponse`
  - `EntryResponse`, `EntryListResponse`
- Error response models

**1.5 Core Services**
- `UserService` - User CRUD operations
- `MetricService` - Metric management logic
- `EntryService` - Daily log entry management
- Database session management (dependency injection)
- Transaction handling
- Error handling patterns

#### Deliverables:
- ✅ All API endpoints functional (tested in Swagger/Postman)
- ✅ User can register and authenticate
- ✅ CRUD operations for metrics work correctly
- ✅ CRUD operations for entries work correctly
- ✅ OpenAPI documentation available at `/docs`
- ✅ All endpoints have proper validation
- ✅ Authentication protects private routes

---

### **STAGE 2: Frontend Foundation** ⚡
**Priority**: HIGH | **Duration**: 4-5 days
**Agents**: @frontend-dev, @ux-designer, @i18n-specialist, @accessibility-specialist

#### ✅ STAGE 2 - COMPLETED (2025-11-15)

**Completed Tasks:**
- ✅ **2.1 PWA Setup**: vite-plugin-pwa configured, manifest.webmanifest, service worker caching
- ✅ **2.2 i18n**: svelte-i18n with complete PL/EN translations, browser locale detection
- ✅ **2.3 State Management**: Svelte stores (auth, metrics, entries) with derived stores
- ✅ **2.4 Design System**: Button, Input, Card, Loading components with variants
- ✅ **2.5 Routing**: svelte-spa-router with protected routes, auth guard

**Additional Files Created (25+ files):**
- API client with axios (auto token refresh)
- Login/Register/Dashboard pages
- Complete translation files (PL/EN)
- Svelte stores with actions

**Ready for STAGE 3**: Core Features - Metrics & Daily Log 🎯

---

#### Tasks:

**2.1 PWA Setup**
- Configure Vite PWA plugin
- Service Worker caching strategies:
  - Cache First: App shell, static assets
  - Network First: API calls (with cache fallback)
  - Background Sync: POST requests when offline
- Web App Manifest configuration:
  - App name, description
  - Icons (192x192, 512x512)
  - Theme colors
  - Display mode (standalone)
- Offline detection and user notifications
- Add to Home Screen functionality

**2.2 Internationalization (i18n)**
- Install and configure `svelte-i18n`
- Create translation file structure:
  - `/src/i18n/pl.json` - Polish translations
  - `/src/i18n/en.json` - English translations
- Translation keys organization by feature
- Language switcher component
- Browser locale detection (set default language)
- Date/time formatting with `date-fns` (locale-aware)
- Number formatting (locale-aware)

**2.3 State Management**
- Setup Svelte stores:
  ```typescript
  // stores/user.ts
  - userStore: User | null
  - isAuthenticated: derived store

  // stores/metrics.ts
  - metricsStore: Metric[]
  - metricsByCategory: derived store

  // stores/entries.ts
  - entriesStore: Entry[]
  - todayEntry: derived store

  // stores/sync.ts
  - syncStatusStore: NetworkStatus

  // stores/i18n.ts
  - localeStore: 'pl' | 'en'
  ```
- API client setup (Axios or Fetch wrapper)
- Request/response interceptors
- Error handling patterns
- Loading state management

**2.4 Design System Foundation**
- Tailwind CSS configuration:
  - Custom color palette (from UI_UX_GUIDELINES.md)
  - Typography scale
  - Spacing system
  - Breakpoints
- Base UI components:
  - **Button** (primary, secondary, danger, ghost variants)
  - **Input** (text, number, email, password)
  - **TextArea** (with auto-resize)
  - **Select** (dropdown)
  - **Checkbox** and **Toggle** switch
  - **Radio** buttons
  - **Card** component
  - **Modal** dialog
  - **Loading Spinner**
  - **Toast** notifications
- Component documentation (Storybook optional)

**2.5 Routing & Layout**
- Install router (svelte-spa-router or similar)
- Define routes:
  ```
  /              → Landing page
  /login         → Login page
  /register      → Registration page
  /dashboard     → Main dashboard (protected)
  /metrics       → Metric management (protected)
  /log           → Daily log form (protected)
  /insights      → Data insights (protected)
  /correlations  → Correlation analysis (protected)
  /settings      → User settings (protected)
  /export        → Data export (protected)
  ```
- Main layout component:
  - Header with navigation
  - Sidebar (mobile: bottom nav)
  - Content area
  - Footer
- Protected route guard (redirect to login if not authenticated)
- 404 Not Found page

#### Deliverables:
- ✅ PWA is installable (Add to Home Screen works)
- ✅ App works offline (cached assets + SW)
- ✅ Language switching PL/EN works
- ✅ Design system components ready to use
- ✅ Routing works, protected routes enforce auth
- ✅ API client successfully communicates with backend
- ✅ Layout is responsive (mobile-first)

---

### **STAGE 3: Core Features - Metrics & Daily Log** 🎯
**Priority**: CRITICAL | **Duration**: 5-6 days
**Agents**: @frontend-dev, @backend-dev, @ux-designer, @clinical-psychologist

#### ✅ STAGE 3 - COMPLETED (2025-11-15)

**Completed Tasks:**
- ✅ **3.1 Metric Management UI**: Complete CRUD with filtering, search, category grouping, archive/unarchive
- ✅ **3.2 Daily Log Form**: All 5 metric types (range, number, boolean, count, text), progress bar, date selection
- ✅ **3.3 Entry History**: List view with filtering, search, date range selection
- ✅ **3.4 Navigation**: Top navbar with links to all pages, logout functionality
- ✅ **3.5 Integration**: Dashboard shows real stats from stores

**Additional Files Created (8 files):**
- Modal, Select components
- Metrics, DailyLog, Entries pages
- Updated Dashboard with navigation and real data

**Ready for STAGE 4**: Local Storage & Visualizations 📊

---

#### Tasks:

**3.1 Metric Management UI**
- **Metrics List Page**:
  - Display all metrics grouped by category
  - Show metric type, range, color/icon
  - Filter by category
  - Search metrics by name
  - Archive/unarchive toggle

- **Create Metric Modal/Page**:
  - Category selection (7 categories)
  - Value type selection (Range, Number, Boolean, Count, Text)
  - For Range: min/max value inputs
  - Name input (translatable key or custom)
  - Optional description
  - Color picker (for visual identification)
  - Icon selector
  - Preview of metric

- **Edit Metric**:
  - Edit all metric properties
  - Warning if metric has existing data

- **Archive Metric**:
  - Soft delete (archived flag)
  - Confirmation dialog
  - Option to restore

- **Drag & Drop Reordering**:
  - Change display order
  - Save order preference

**3.2 Daily Log Form**
- **Form Design** (Mobile-First, <60s completion target):
  - Display all active metrics
  - Group by category (collapsible sections)
  - Progress bar (% of metrics filled)
  - Previous day's values visible (for reference)

- **Input Components by Type**:
  - **Range**: Horizontal slider with current value display
  - **Number**: Number input with +/- stepper buttons
  - **Boolean**: Toggle switch (yes/no)
  - **Count**: Number stepper (0+)
  - **Text**: Expandable textarea

- **Form Features**:
  - Auto-save draft (every 30s or on blur)
  - Manual save button
  - Submit button (validates all required fields)
  - Skip/mark as optional
  - Quick navigation between categories
  - Keyboard shortcuts (Tab navigation)

- **Date Selection**:
  - Default: today
  - Allow backdated entries
  - Calendar picker

**3.3 Calendar View**
- Month calendar grid
- Visual indicators:
  - Days with complete entries (green)
  - Days with partial entries (yellow)
  - Days without entries (gray)
  - Today highlighted
- Click on day → view/edit that day's entry
- Legend explaining colors
- Month/year navigation

**3.4 Entry History**
- List of past entries (newest first)
- Filter by date range
- Search by notes
- Quick edit/delete actions
- Pagination or infinite scroll

**3.5 Backend Validation**
- Validate value ranges (min/max constraints)
- Enforce unique constraint (user + date)
- Validate metric exists and belongs to user
- Handle timezone conversions correctly
- Audit trail (created_at, updated_at timestamps)

#### Deliverables:
- ✅ User can create custom metrics (all 7 categories)
- ✅ User can configure metric types and constraints
- ✅ Daily log form works and is fast (<60s target)
- ✅ Entries save successfully to database
- ✅ Calendar view shows entry history
- ✅ User can edit past entries
- ✅ Mobile UX is smooth and responsive
- ✅ Form validation works (client + server side)

---

### **STAGE 4: Local Storage & Visualizations** 📊
**Priority**: HIGH | **Duration**: 4-5 days
**Agents**: @frontend-dev, @dataviz-specialist, @performance-engineer

#### ✅ STAGE 4 - COMPLETED (2025-11-15)

**Completed Tasks:**
- ✅ **4.1 IndexedDB Integration**: Dexie.js database schema with metrics, entries, sync queue, user settings
- ✅ **4.2 Sync Manager**: Offline queue, online sync with retry logic, conflict resolution (LWW), sync status UI
- ✅ **4.3 Data Visualization Components**: LineChart (Chart.js), StatisticsPanel, CalendarHeatmap
- ✅ **4.4 Dashboard Updates**: Current streak calculation, sync status indicator, calendar heatmap, improved stats
- ✅ **4.5 Insights Page**: Multi-metric trend charts, date range filtering (7d/30d/90d/all), statistical summaries

**Additional Files Created (10+ files):**
- `frontend/src/lib/db.ts`: IndexedDB schema and helpers with Dexie.js
- `frontend/src/lib/sync.ts`: Sync manager with offline queue and auto-sync (every 30s)
- `frontend/src/components/LineChart.svelte`: Interactive line chart with Chart.js
- `frontend/src/components/StatisticsPanel.svelte`: Metric statistics (mean, median, std dev, trend)
- `frontend/src/components/CalendarHeatmap.svelte`: Monthly calendar with entry status visualization
- `frontend/src/pages/Insights.svelte`: Analytics page with multi-metric visualizations
- Updated `frontend/src/stores/metrics.ts` with offline-first data access
- Updated `frontend/src/stores/entries.ts` with offline-first data access
- Updated `frontend/src/pages/Dashboard.svelte` with streak, sync status, calendar
- Updated `frontend/src/App.svelte` with Insights route
- Updated `frontend/package.json` with Chart.js and Dexie.js dependencies

**Key Features Implemented:**
- **Offline-First Architecture**: All data cached in IndexedDB for instant access
- **Auto-Sync Queue**: Operations queued when offline, auto-processed every 30s when online
- **Streak Calculation**: Shows consecutive days with entries (checks today and yesterday)
- **Calendar Heatmap**: Visual calendar showing complete/partial/no entries per day
- **Line Charts**: Interactive trend visualization with Chart.js, time-based x-axis
- **Statistics Panel**: Displays mean, median, min/max, std dev, 7-day trend indicator
- **Multi-Metric Insights**: Select multiple metrics to compare trends
- **Sync Status Indicator**: Shows online/offline status and pending sync count
- **Date Range Filtering**: 7d, 30d, 90d, or all-time data views

**Technical Implementation:**
- Used Dexie.js for IndexedDB wrapper with clean API
- Chart.js with chartjs-adapter-date-fns for time-series charts
- Offline queue with retry logic (max 5 retries)
- Last Write Wins (LWW) conflict resolution strategy
- Auto-sync runs every 30 seconds when online
- Temporary negative IDs for offline-created entries

**Ready for STAGE 5**: Analytics Engine - Correlations 🔬

---

#### Tasks:

**4.1 IndexedDB Integration**
- Install Dexie.js (IndexedDB wrapper)
- Define database schema:
  ```typescript
  class FeelinkDB extends Dexie {
    metrics: Table<Metric>
    entries: Table<Entry>
    syncQueue: Table<SyncOperation>
    userSettings: Table<UserSettings>
  }
  ```
- Implement CRUD operations via IndexedDB
- Local-first data access pattern:
  - Read from IndexedDB first
  - Fetch from API if not cached
  - Update both IndexedDB and API

**4.2 Sync Manager**
- **Offline Queue**:
  - Queue all mutations when offline
  - Store operations (CREATE, UPDATE, DELETE)
  - Retry count and timestamp

- **Online Sync**:
  - Detect online status
  - Process sync queue (FIFO)
  - Send operations to server
  - Handle success/failure
  - Update local cache on success

- **Conflict Resolution**:
  - Strategy: Last Write Wins (LWW)
  - Compare timestamps (updated_at)
  - Alternative: Manual resolution for critical conflicts

- **Sync Status UI**:
  - Show sync pending count
  - Last successful sync timestamp
  - Manual sync trigger button
  - Sync error notifications

**4.3 Data Visualization Components**

- **Line Chart Component** (Chart.js):
  - Display metric trends over time
  - Multi-metric overlay (up to 5 metrics)
  - Interactive features:
    - Zoom (pinch/scroll)
    - Pan (drag)
    - Tooltips (show exact values)
  - Date range selector (7d, 30d, 90d, all)
  - Legend with color coding

- **Scatter Plot Component**:
  - Display relationship between two metrics
  - Regression line (optional)
  - Interactive tooltips
  - Click point → jump to entry date

- **Calendar Heatmap**:
  - Visual density of entries
  - Color intensity based on metric value
  - Month/year navigation

- **Statistics Panel**:
  - Display for each metric:
    - Mean (average)
    - Median
    - Min / Max
    - Std deviation
    - Trend indicator (↑↓→)
  - Date range filter

**4.4 Dashboard Page**
- **Overview Section**:
  - Welcome message
  - Current streak (consecutive days logged)
  - Total entries count
  - Quick stats (last 7/30 days)

- **Quick Actions**:
  - "Log Today" button (jump to daily log)
  - "View Insights" button

- **Recent Activity**:
  - Last 3 entries preview
  - Top metrics chart

- **Insights Teaser**:
  - Preview top 2-3 correlations
  - "See all insights" link

**4.5 Insights Page**
- Metric trend charts (top 5 most tracked)
- Statistical summaries
- Date range selector
- Export chart as image (optional)

#### Deliverables:
- ✅ Data is cached locally in IndexedDB
- ✅ App works fully offline (read + write)
- ✅ Offline entries sync when back online
- ✅ Line charts display metric trends
- ✅ Scatter plots work for metric comparisons
- ✅ Dashboard provides useful overview
- ✅ Statistics are accurate and helpful
- ✅ Charts are responsive and mobile-friendly

---

### **STAGE 5: Analytics Engine - Correlations** 🔬
**Priority**: MEDIUM | **Duration**: 5-6 days
**Agents**: @data-scientist, @backend-dev, @dataviz-specialist, @clinical-psychologist

#### ✅ STAGE 5 - COMPLETED (2025-11-15)

**Completed Tasks:**
- ✅ **5.1 Correlation Engine**: Pearson, Spearman, Kendall algorithms with scipy
- ✅ **5.2 Lag Correlation Analysis**: Time-delayed effects up to 30 days
- ✅ **5.3 API Endpoints**: POST /correlations, GET /statistics
- ✅ **5.4 Correlation Service**: Data preparation, analytics service layer
- ✅ **5.5 Correlation Matrix**: Heatmap visualization with color-coded strengths
- ✅ **5.6 Scatter Plots**: Interactive Chart.js scatter plots for metric pairs
- ✅ **5.7 Correlations Page**: Complete UI with filtering, interpretation, analysis
- ✅ **5.8 Plain-Language Interpretations**: User-friendly correlation explanations

**Additional Files Created (9 files):**
- `backend/app/analytics/correlation.py`: Correlation engine with Pearson, Spearman, Kendall
- `backend/app/schemas/analytics.py`: Request/response schemas for analytics API
- `backend/app/services/analytics_service.py`: Analytics service layer with data preparation
- `backend/app/api/analytics.py`: Analytics endpoints (correlations, statistics)
- Updated `backend/app/api/__init__.py`: Register analytics router
- Updated `backend/app/main.py`: Include analytics router in app
- `frontend/src/lib/api.ts`: Add analyticsApi methods
- `frontend/src/components/CorrelationMatrix.svelte`: Heatmap visualization
- `frontend/src/components/ScatterPlot.svelte`: Scatter plot with Chart.js
- `frontend/src/pages/Correlations.svelte`: Complete correlations analysis page
- Updated `frontend/src/App.svelte`: Add /correlations route
- Updated `frontend/src/pages/Dashboard.svelte`: Add Correlations link in nav

**Key Features Implemented:**
- **Correlation Algorithms**: Pearson (linear), Spearman (rank), Kendall (rank)
- **Lag Analysis**: Detect delayed effects (e.g., sleep today → mood tomorrow)
- **Statistical Significance**: P-value testing, significance threshold (default p<0.05)
- **Strength Classification**: Weak (|r|<0.3), Moderate (0.3≤|r|<0.7), Strong (|r|≥0.7)
- **Direction Detection**: Positive, negative, or none
- **Correlation Matrix**: Visual heatmap with blue (positive) and red (negative) shades
- **Scatter Plots**: Interactive visualization of metric pairs with regression info
- **Plain-Language Interpretations**: User-friendly explanations of correlations
- **Filtering**: Date range, algorithm selection, significance filter, strength filter
- **Data Requirements**: Minimum 7 data points enforced

**Technical Implementation:**
- Scipy for correlation calculations (pearsonr, spearmanr, kendalltau)
- Pandas for data preparation and handling missing values
- Chart.js ScatterController for scatter plots
- Color-coded heatmap with significance indicators
- Automatic lag detection (tests 0-7 days by default)
- Last Write Wins (LWW) for best lag correlation

**Clinical Considerations:**
- Clear "correlation ≠ causation" disclaimer
- Statistical significance clearly marked
- Sample size displayed for transparency
- Plain-language interpretations for non-technical users

**Ready for STAGE 6**: Polish, Testing & Deployment ✨

---

#### Tasks:

**5.1 Correlation Engine (Backend)**
- **Algorithm Implementation** (Python):
  - Pearson correlation coefficient
  - Spearman rank correlation
  - Kendall tau correlation (optional)
  - Statistical significance (p-value calculation)

- **Lag Correlation Analysis**:
  - Calculate correlations with time delays (0-30 days)
  - Example: Metric A today → Metric B in 3 days
  - Find optimal lag (highest correlation)

- **Data Preparation**:
  - Convert entry data to Pandas DataFrame
  - Handle missing values (interpolation or skip)
  - Normalize data if needed
  - Filter by date range

- **Requirements**:
  - Minimum 7 data points for correlation
  - Configurable significance threshold (default p<0.05)
  - Return correlation strength classification:
    - |r| < 0.3: weak
    - 0.3 ≤ |r| < 0.7: moderate
    - |r| ≥ 0.7: strong

**5.2 API Endpoints**
- `POST /api/v1/analytics/correlations`:
  - Request body:
    ```json
    {
      "metric_ids": [1, 2, 3],  // optional, default: all
      "date_from": "2024-01-01",  // optional
      "date_to": "2024-12-31",    // optional
      "algorithm": "pearson",     // pearson|spearman|kendall
      "max_lag": 7,               // max days to check
      "min_significance": 0.05    // p-value threshold
    }
    ```
  - Response:
    ```json
    {
      "correlations": [
        {
          "metric_1_id": 1,
          "metric_1_name": "Sleep Hours",
          "metric_2_id": 3,
          "metric_2_name": "Mood",
          "coefficient": 0.73,
          "p_value": 0.002,
          "lag": 0,
          "strength": "strong",
          "significant": true,
          "direction": "positive",
          "sample_size": 45
        }
      ],
      "algorithm_used": "pearson",
      "date_range": {"from": "...", "to": "..."}
    }
    ```

- `GET /api/v1/analytics/statistics`:
  - Basic stats for all metrics
  - Date range filter

**5.3 Correlation UI (Frontend)**
- **Correlations Page**:
  - List of all significant correlations
  - Sort by:
    - Strength (|r|)
    - Significance (p-value)
    - Lag (days)
  - Filter by:
    - Metric category
    - Date range
    - Strength threshold
    - Include/exclude lag correlations

- **Correlation Card**:
  - Display:
    - Metric 1 ↔ Metric 2 names
    - Correlation coefficient (r = 0.73)
    - Strength indicator (Strong Positive)
    - P-value and significance badge
    - Lag information (if applicable)
    - Sample size
  - Click to expand:
    - Scatter plot visualization
    - Plain-language interpretation
    - Link to both metrics' trend charts

- **Plain-Language Interpretation**:
  - Example: "Strong positive correlation (r=0.73, p<0.01) between Sleep Hours and Mood. When you sleep more, your mood tends to improve. This relationship is statistically significant."
  - For lag: "Alcohol consumption shows a moderate negative correlation (r=-0.52, p=0.03) with mood 3 days later."

**5.4 Visualization**
- **Correlation Matrix Heatmap**:
  - Grid showing all metric pairs
  - Color intensity = correlation strength
  - Tooltip with details
  - Click cell → view details

- **Scatter Plot for Correlation**:
  - X-axis: Metric 1 values
  - Y-axis: Metric 2 values
  - Regression line overlay
  - R² value display
  - Interactive points (click → see entry date)

**5.5 Insights Generation**
- **Top Insights Panel**:
  - Top 5 strongest correlations
  - Most significant lag effects
  - Unusual patterns detected

- **Clinical Context** (with @clinical-psychologist):
  - Appropriate interpretation language
  - Disclaimers ("correlation ≠ causation")
  - Suggestions for discussing with healthcare provider

#### Deliverables:
- ✅ Correlation engine calculates Pearson/Spearman/Kendall
- ✅ Lag correlation analysis works (delayed effects)
- ✅ User sees top correlations with r, p-value, lag
- ✅ Visualizations (scatter plots, heatmap) display relationships
- ✅ Plain-language interpretations are helpful
- ✅ Statistical significance is clearly indicated
- ✅ Minimum data requirements are enforced

---

### **STAGE 6: Polish, Testing & Deployment** ✨
**Priority**: MEDIUM | **Duration**: 4-5 days
**Agents**: @qa-engineer, @accessibility-specialist, @performance-engineer, @devops, @technical-writer

#### Progress:
✅ **6.1 Testing - Backend**:
  - Pytest infrastructure configured (pytest, pytest-asyncio, httpx)
  - Created comprehensive test suite (conftest.py with fixtures)
  - 140+ tests across 5 test files:
    - test_correlation.py: 30+ tests for correlation algorithms
    - test_auth.py: 40+ tests for password hashing and JWT
    - test_metrics.py: 20+ tests for metrics CRUD API
    - test_entries.py: 25+ tests for entries CRUD API
    - test_analytics.py: 25+ tests for analytics/correlations API

✅ **6.1 Testing - Frontend**:
  - Vitest + @testing-library/svelte configured
  - Test setup with mocks (localStorage, matchMedia)
  - Example tests created:
    - Button.test.ts: Component testing
    - db.test.ts: Database helpers unit tests
    - user.test.ts: Store testing

✅ **6.2 Accessibility**:
  - Loading component: Added role="status", aria-live, aria-busy, sr-only text
  - Card component: Keyboard navigation (Enter/Space), focus indicators
  - Login/Register: Error messages with role="alert" and aria-live
  - Created comprehensive ACCESSIBILITY.md documentation
  - WCAG 2.1 Level AA guidelines documented

🚧 **In Progress**:
  - Performance optimization (bundle size, database indexes)
  - User documentation
  - CI/CD pipeline
  - Docker production configuration

#### Tasks:

**6.1 Testing**

- **Backend Testing (pytest)**:
  - Unit tests:
    - Authentication logic
    - CRUD operations (metrics, entries)
    - Correlation algorithms
    - Data validation
  - Integration tests:
    - API endpoint flows
    - Database transactions
    - Authentication flow
  - Test fixtures and factories
  - Mock external dependencies
  - Target: >80% code coverage

- **Frontend Testing (Vitest + Testing Library)**:
  - Component tests:
    - UI components render correctly
    - User interactions work
    - Props and events
  - Store tests:
    - State mutations
    - Derived stores
    - API integration
  - Integration tests:
    - Page flows
    - Form submissions
    - Navigation
  - Target: >80% code coverage

- **E2E Testing (Playwright)**:
  - Critical user flows:
    - User registration → login
    - Create metric → log daily entry
    - View dashboard → insights
    - Run correlation analysis
  - Cross-browser testing (Chrome, Firefox, Safari)
  - Mobile viewport testing
  - Offline functionality testing

**6.2 Accessibility (a11y)**
- **WCAG 2.1 Level AA Audit**:
  - Run automated tools (axe, Lighthouse)
  - Manual keyboard navigation testing
  - Screen reader testing (NVDA, VoiceOver, JAWS)

- **Fixes**:
  - Color contrast ratios (≥4.5:1 for normal text)
  - ARIA labels for all interactive elements
  - Focus management (visible focus indicators)
  - Keyboard navigation (Tab, Enter, Esc)
  - Form labels and error associations
  - Skip links for navigation
  - Alt text for all images/icons
  - Proper heading hierarchy (h1→h2→h3)

- **Testing Checklist**:
  - ✅ All forms keyboard-navigable
  - ✅ Screen reader announces changes
  - ✅ Color is not only indicator (use icons too)
  - ✅ Focus visible on all interactive elements
  - ✅ Error messages associated with inputs

**6.3 Performance Optimization**

- **Frontend**:
  - Bundle size analysis (use vite-bundle-visualizer)
  - Code splitting (lazy load routes)
  - Tree shaking (remove unused code)
  - Image optimization (WebP, lazy loading)
  - Font optimization (subset, preload)
  - Lighthouse audit (target score >90):
    - Performance
    - Accessibility
    - Best Practices
    - SEO
  - Core Web Vitals:
    - LCP < 2.5s
    - FID < 100ms
    - CLS < 0.1

- **Backend**:
  - Database query optimization:
    - Use EXPLAIN ANALYZE
    - Add missing indexes
    - Optimize N+1 queries
  - API response time:
    - Cache frequent queries (Redis)
    - Pagination for large datasets
    - Gzip compression
  - Connection pooling

- **PWA**:
  - Optimize Service Worker caching
  - Reduce cache size
  - Prefetch critical resources

**6.4 Documentation**

- **User Documentation**:
  - Onboarding tutorial (first-time user guide)
  - How to create metrics
  - How to log daily entries
  - Understanding correlations
  - Exporting data
  - FAQ section

- **API Documentation**:
  - Complete OpenAPI/Swagger docs
  - Example requests/responses
  - Authentication guide
  - Error codes reference

- **Developer Documentation**:
  - Updated README.md with setup instructions
  - Architecture overview
  - Contributing guidelines
  - Code style guide
  - Testing guide
  - Deployment guide

**6.5 CI/CD Pipeline**

- **GitHub Actions Workflow**:
  ```yaml
  # .github/workflows/ci-cd.yml

  on: [push, pull_request]

  jobs:
    test-backend:
      - Run pytest
      - Check coverage (fail if <80%)

    test-frontend:
      - Run Vitest
      - Check coverage (fail if <80%)

    build:
      - Build Docker images
      - Run security scan

    deploy-staging:
      - Deploy to staging (on develop branch)

    deploy-production:
      - Deploy to production (on main branch)
      - Run database migrations
  ```

- **Automated Database Migrations**:
  - Run Alembic migrations on deploy
  - Rollback strategy

- **Environment Management**:
  - Separate configs for dev/staging/prod
  - Secrets management

**6.6 Production Deployment**

- **Infrastructure Setup**:
  - Choose hosting platform:
    - Option A: AWS (EC2, RDS, S3)
    - Option B: Azure (App Service, PostgreSQL)
    - Option C: GCP (Cloud Run, Cloud SQL)
    - Option D: Vercel (Frontend) + Railway (Backend)
  - SSL/TLS certificate setup (Let's Encrypt)
  - Domain configuration (DNS)

- **Database**:
  - Production PostgreSQL instance
  - Automated backups (daily)
  - Point-in-time recovery enabled
  - Connection pooling (PgBouncer)

- **Monitoring & Logging**:
  - Error tracking (Sentry)
  - Application monitoring (Prometheus + Grafana)
  - Log aggregation (CloudWatch, Datadog, or ELK)
  - Uptime monitoring (UptimeRobot)

- **Health Checks**:
  - Backend health endpoint (`/health`)
  - Database connectivity check
  - Redis connectivity check
  - Frontend uptime

- **Security**:
  - Environment variables (never commit secrets)
  - HTTPS only (HSTS enabled)
  - CORS configuration
  - Rate limiting (prevent abuse)
  - SQL injection prevention (parameterized queries)
  - XSS prevention (sanitize inputs)

#### Deliverables:
- ✅ All tests pass (>80% coverage backend + frontend)
- ✅ E2E tests cover critical user flows
- ✅ WCAG 2.1 Level AA compliance achieved
- ✅ Lighthouse score >90 (all categories)
- ✅ Bundle size optimized (<500KB initial load)
- ✅ API response times <500ms (p95)
- ✅ CI/CD pipeline functional
- ✅ Documentation complete and published
- ✅ Application deployed to production
- ✅ Monitoring and alerting configured
- ✅ Backup strategy implemented

---

## 📋 MVP Acceptance Criteria

The MVP is considered **COMPLETE** when all of the following are true:

### Functional Requirements:
- [ ] User can register and authenticate
- [ ] User can create custom metrics (all 7 categories)
- [ ] User can configure metric types (Range, Number, Boolean, Count, Text)
- [ ] User can complete daily log in <60 seconds on mobile
- [ ] Application works fully offline
- [ ] Data syncs automatically when online
- [ ] User can view metric trends (line charts)
- [ ] User can view correlation analysis (≥7 days data required)
- [ ] Correlations show coefficient, p-value, lag, strength
- [ ] Application supports PL and EN languages
- [ ] Language switching works at runtime
- [ ] Application is installable as PWA (iOS, Android, Desktop)

### Non-Functional Requirements:
- [ ] Initial page load <3s (4G connection)
- [ ] Daily log form response <100ms
- [ ] WCAG 2.1 Level AA compliant
- [ ] Works on iOS Safari, Android Chrome, Desktop browsers
- [ ] Responsive design (320px - 2560px width)
- [ ] Test coverage >80% (backend + frontend)
- [ ] Lighthouse score >90
- [ ] HTTPS/TLS 1.3+ for all communication
- [ ] Password hashed with bcrypt
- [ ] GDPR compliant (data export capability)

### Documentation:
- [ ] User onboarding guide published
- [ ] API documentation complete
- [ ] Developer setup guide updated
- [ ] Deployment documentation available

### Deployment:
- [ ] Application deployed to production
- [ ] CI/CD pipeline operational
- [ ] Monitoring and error tracking active
- [ ] Database backups automated

---

## 🚀 Recommended First Steps

If you agree with this plan, I recommend starting with:

### **Immediate Actions** (Day 1):

1. **STAGE 0.1**: Create directory structure and Docker Compose
   - `frontend/`, `backend/`, `docs/` directories
   - `docker-compose.yml` with all services
   - `.gitignore` files

2. **STAGE 0.2**: Setup Backend
   - Initialize FastAPI project
   - Configure Alembic
   - Connect to PostgreSQL

3. **STAGE 0.3**: Setup Frontend
   - Initialize Svelte + TypeScript + Vite
   - Configure Tailwind CSS
   - Basic project structure

4. **STAGE 0.4**: Integration
   - Connect all services
   - "Hello World" endpoint
   - Verify everything runs

### **Incremental Development Approach**:
- Complete each stage with working deliverables
- Commit frequently with descriptive messages
- Push to branch `claude/create-action-plan-*`
- Review and adjust plan after every 2-3 stages
- Demo working features at each milestone

---

## 🎯 Post-MVP Enhancements

Features to implement **after** MVP is complete:

### Phase 2: Advanced Features (2-3 weeks)
- [ ] PDF report generation (clinical summaries)
- [ ] Data export (CSV, JSON, full backup)
- [ ] Advanced lag/cross-correlations
- [ ] Email notifications (daily reminders)
- [ ] Password reset via email
- [ ] User preferences (theme, notification settings)

### Phase 3: Enhancement (3-4 weeks)
- [ ] Dark mode support
- [ ] Advanced data visualizations (D3.js custom charts)
- [ ] AI-powered insight suggestions
- [ ] Pattern detection (anomaly alerts)
- [ ] Multi-device sync optimization
- [ ] Bulk data import

### Phase 4: Future (Long-term)
- [ ] Wearable device integration (Fitbit, Apple Watch)
- [ ] Voice input for quick logging
- [ ] Photo/image attachments to entries
- [ ] Therapist collaboration portal
- [ ] Social/community features (optional, privacy-focused)
- [ ] Mobile native apps (React Native, Flutter)
- [ ] Advanced machine learning predictions

---

## 📊 Success Metrics

Track these KPIs during and after MVP launch:

### User Engagement:
- Daily log completion rate: **Target >70%**
- Average time to complete log: **Target <60 seconds**
- User retention (Day 7, Day 30)
- Active users (DAU, WAU, MAU)

### Feature Adoption:
- % users creating custom metrics
- Average metrics per user
- % users viewing correlations
- % users exporting data

### Technical Performance:
- Page load time (p95): **Target <3s**
- API response time (p95): **Target <500ms**
- Uptime: **Target >99.5%**
- Error rate: **Target <0.1%**

### User Satisfaction:
- System Usability Scale (SUS): **Target >75**
- User discovers ≥3 meaningful correlations within 30 days
- Net Promoter Score (NPS)

---

## 📞 Questions & Next Steps

### Questions for You:
1. ✅ Does this plan look comprehensive?
2. ❓ Any changes to priorities or timeline?
3. ❓ Should we start with backend-first, frontend-first, or parallel development?
4. ❓ Preferences for specific technologies (alternatives to Svelte/FastAPI)?
5. ❓ Should I begin implementation of **STAGE 0** now?

### My Recommendations:
- ✅ Start with **STAGE 0** (infrastructure foundation)
- ✅ Use **incremental approach** - each stage produces working software
- ✅ Commit frequently to `claude/create-action-plan-*` branch
- ✅ Review and adapt plan every 2-3 stages
- ✅ Prioritize core user value (daily logging + insights)

---

## 📝 Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-11-15 | Initial action plan created | Claude (Agent Team) |

---

## 🔗 Related Documents

- [PROJECT_OVERVIEW.md](./docs/PROJECT_OVERVIEW.md) - Project vision
- [REQUIREMENTS.md](./docs/REQUIREMENTS.md) - Detailed requirements
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) - Technical architecture
- [CLAUDE.md](./CLAUDE.md) - Agent team structure
- [README.md](./README.md) - Project overview

---

**Status**: ✅ Plan Ready - Awaiting Approval to Start Implementation
**Next Action**: Begin STAGE 0 - Project Infrastructure Setup

---

**Ready to build something amazing! 🚀**
