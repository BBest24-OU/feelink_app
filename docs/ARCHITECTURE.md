# FeelInk - Technical Architecture

## Document Information
- **Version**: 0.1.0
- **Last Updated**: 2025-11-15
- **Status**: Draft

---

## 1. Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT (PWA)                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │            UI Layer (Mobile-First)                    │  │
│  │  React/Vue/Svelte Components + i18n                   │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Application Logic Layer                       │  │
│  │  State Management + Business Logic                    │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Data Synchronization Layer                    │  │
│  │  Offline Queue + Sync Manager + Conflict Resolution   │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Local Storage Layer                           │  │
│  │  IndexedDB + Cache API + ServiceWorker                │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                    HTTPS/REST API
                           │
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Python)                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              API Layer (Flask/FastAPI)                │  │
│  │  REST Endpoints + Authentication + Validation         │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │            Business Logic Layer                       │  │
│  │  Correlation Engine + Analytics + Report Generator    │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Data Access Layer                        │  │
│  │  ORM + Query Builder + Data Validation                │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Database Layer                           │  │
│  │  PostgreSQL/MySQL + Redis Cache                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Principles

1. **Offline-First**: All core functionality works without internet
2. **Progressive Enhancement**: Basic features work everywhere, enhanced features where supported
3. **Security by Design**: Authentication, encryption, input validation at every layer
4. **Scalability**: Horizontal scaling capability from day one
5. **Maintainability**: Clear separation of concerns, testable code
6. **Privacy-Focused**: User data ownership, no unnecessary data collection

---

## 2. Frontend Architecture

### 2.1 Technology Stack

#### 2.1.1 Core Framework Options
**Recommendation**: React or Svelte for optimal PWA performance

| Framework | Pros | Cons | Recommendation |
|-----------|------|------|----------------|
| **React** | Large ecosystem, good PWA support, widely known | Bundle size, complexity | ✅ Recommended |
| **Vue 3** | Easy to learn, good performance, composition API | Smaller ecosystem | ✅ Alternative |
| **Svelte** | Smallest bundle, fastest performance, simple | Smaller ecosystem, newer | ✅ Best for PWA |

**Decision**: Start with **Svelte** for MVP due to:
- Smallest bundle size (critical for mobile)
- Native reactivity (no virtual DOM overhead)
- Excellent PWA performance
- Simple learning curve
- Can migrate to React later if needed

#### 2.1.2 Essential Libraries

```json
{
  "core": {
    "svelte": "Framework",
    "vite": "Build tool",
    "typescript": "Type safety"
  },
  "pwa": {
    "workbox": "Service Worker management",
    "vite-plugin-pwa": "PWA build integration"
  },
  "storage": {
    "idb": "IndexedDB wrapper",
    "localforage": "Fallback storage abstraction"
  },
  "state": {
    "svelte/store": "Built-in state management",
    "rxdb": "Offline-first reactive database (alternative)"
  },
  "i18n": {
    "svelte-i18n": "Internationalization",
    "date-fns": "Date formatting with locale support"
  },
  "charts": {
    "chart.js": "Simple, responsive charts",
    "d3.js": "Advanced custom visualizations",
    "plotly.js": "Scientific plotting (alternative)"
  },
  "ui": {
    "tailwindcss": "Utility-first CSS (centralized theme)",
    "daisyui": "Component library for Tailwind (optional)"
  },
  "forms": {
    "svelte-forms-lib": "Form handling",
    "yup": "Validation schema"
  },
  "utils": {
    "date-fns": "Date manipulation",
    "lodash-es": "Utility functions",
    "uuid": "UUID generation"
  }
}
```

### 2.2 PWA Architecture

#### 2.2.1 Service Worker Strategy

```javascript
// Multi-layered caching strategy

// 1. App Shell - Cache First
workbox.routing.registerRoute(
  ({request}) => request.destination === 'document',
  new workbox.strategies.CacheFirst({
    cacheName: 'app-shell',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days
      }),
    ],
  })
);

// 2. Static Assets - Cache First
workbox.routing.registerRoute(
  ({request}) => ['style', 'script', 'worker'].includes(request.destination),
  new workbox.strategies.CacheFirst({
    cacheName: 'static-assets',
    plugins: [
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      }),
    ],
  })
);

// 3. API - Network First with Cache Fallback
workbox.routing.registerRoute(
  ({url}) => url.pathname.startsWith('/api/'),
  new workbox.strategies.NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 10,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 5 * 60, // 5 minutes
      }),
    ],
  })
);

// 4. Background Sync for POST requests
workbox.routing.registerRoute(
  ({url, request}) => url.pathname.startsWith('/api/') && request.method === 'POST',
  new workbox.strategies.NetworkOnly({
    plugins: [
      new workbox.backgroundSync.BackgroundSyncPlugin('api-queue', {
        maxRetentionTime: 24 * 60, // Retry for up to 24 hours
      }),
    ],
  })
);
```

#### 2.2.2 Offline Capabilities

```typescript
// Offline Detection
interface NetworkStatus {
  online: boolean;
  syncPending: boolean;
  lastSyncAttempt: Date | null;
  lastSuccessfulSync: Date | null;
}

class OfflineManager {
  private status: NetworkStatus;

  constructor() {
    window.addEventListener('online', () => this.handleOnline());
    window.addEventListener('offline', () => this.handleOffline());
  }

  async handleOffline() {
    this.status.online = false;
    // Notify user
    // Switch to offline mode
  }

  async handleOnline() {
    this.status.online = true;
    // Attempt sync
    await this.syncManager.syncAll();
  }
}
```

### 2.3 Local Storage Architecture

#### 2.3.1 IndexedDB Schema

```typescript
// Database Schema using Dexie.js (IndexedDB wrapper)

import Dexie, { Table } from 'dexie';

class FeelinkDatabase extends Dexie {
  metrics!: Table<Metric>;
  entries!: Table<Entry>;
  syncQueue!: Table<SyncOperation>;
  userSettings!: Table<UserSettings>;

  constructor() {
    super('feelink');

    this.version(1).stores({
      metrics: '++id, userId, category, &name, createdAt, updatedAt',
      entries: '++id, userId, date, syncStatus, createdAt, updatedAt',
      syncQueue: '++id, operation, timestamp, retryCount',
      userSettings: 'userId, language, theme, lastSync'
    });
  }
}

const db = new FeelinkDatabase();
```

#### 2.3.2 Data Synchronization

```typescript
// Sync Manager - handles offline/online data sync

interface SyncOperation {
  id: string;
  operation: 'CREATE' | 'UPDATE' | 'DELETE';
  entity: 'metric' | 'entry' | 'settings';
  data: any;
  timestamp: number;
  retryCount: number;
  maxRetries: number;
}

class SyncManager {
  private queue: SyncOperation[] = [];

  async queueOperation(op: SyncOperation) {
    await db.syncQueue.add(op);
    if (navigator.onLine) {
      await this.processSyncQueue();
    }
  }

  async processSyncQueue() {
    const operations = await db.syncQueue.toArray();

    for (const op of operations) {
      try {
        await this.syncOperation(op);
        await db.syncQueue.delete(op.id);
      } catch (error) {
        if (op.retryCount < op.maxRetries) {
          await db.syncQueue.update(op.id, {
            retryCount: op.retryCount + 1
          });
        } else {
          // Handle failed sync
          this.handleSyncFailure(op, error);
        }
      }
    }
  }

  async syncOperation(op: SyncOperation) {
    switch (op.operation) {
      case 'CREATE':
        return await api.create(op.entity, op.data);
      case 'UPDATE':
        return await api.update(op.entity, op.data);
      case 'DELETE':
        return await api.delete(op.entity, op.data.id);
    }
  }
}
```

#### 2.3.3 Conflict Resolution

```typescript
// Conflict Resolution Strategy: Last Write Wins (LWW)

interface ConflictResolution {
  strategy: 'last-write-wins' | 'manual' | 'server-wins' | 'client-wins';
}

class ConflictResolver {
  async resolve(local: any, remote: any, strategy: ConflictResolution) {
    switch (strategy.strategy) {
      case 'last-write-wins':
        return local.updatedAt > remote.updatedAt ? local : remote;

      case 'server-wins':
        return remote;

      case 'client-wins':
        return local;

      case 'manual':
        // Present both versions to user
        return await this.presentConflictToUser(local, remote);
    }
  }
}
```

### 2.4 State Management

```typescript
// Svelte Stores Architecture

// stores/user.ts
export const user = writable<User | null>(null);
export const isAuthenticated = derived(user, $user => !!$user);

// stores/metrics.ts
export const metrics = writable<Metric[]>([]);
export const metricsByCategory = derived(
  metrics,
  $metrics => groupBy($metrics, 'category')
);

// stores/entries.ts
export const entries = writable<Entry[]>([]);
export const todayEntry = derived(
  entries,
  $entries => $entries.find(e => isToday(e.date))
);

// stores/sync.ts
export const syncStatus = writable<NetworkStatus>({
  online: navigator.onLine,
  syncPending: false,
  lastSyncAttempt: null,
  lastSuccessfulSync: null
});

// stores/i18n.ts
export const locale = writable<'pl' | 'en'>('en');
export const t = derived(locale, $locale => (key: string) => translate(key, $locale));
```

### 2.5 Routing

```typescript
// Client-side routing with code splitting

// routes.ts
export const routes = {
  '/': () => import('./pages/Home.svelte'),
  '/login': () => import('./pages/Login.svelte'),
  '/dashboard': () => import('./pages/Dashboard.svelte'),
  '/metrics': () => import('./pages/Metrics.svelte'),
  '/log': () => import('./pages/DailyLog.svelte'),
  '/insights': () => import('./pages/Insights.svelte'),
  '/correlations': () => import('./pages/Correlations.svelte'),
  '/reports': () => import('./pages/Reports.svelte'),
  '/settings': () => import('./pages/Settings.svelte'),
  '/export': () => import('./pages/Export.svelte')
};
```

---

## 3. Backend Architecture

### 3.1 Technology Stack

#### 3.1.1 Core Framework

**Recommendation**: FastAPI for modern, high-performance Python backend

```python
# Why FastAPI?
# 1. Built-in async support (high performance)
# 2. Automatic OpenAPI documentation
# 3. Type hints and validation with Pydantic
# 4. Modern, well-maintained
# 5. Excellent for RESTful APIs

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FeelInk API",
    description="Mental health tracking API",
    version="0.1.0"
)

# CORS configuration for PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.feelink.com"],  # Production domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3.1.2 Essential Python Libraries

```python
# requirements.txt

# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0  # ASGI server
pydantic==2.5.0            # Data validation
pydantic-settings==2.1.0   # Settings management

# Database
sqlalchemy==2.0.23         # ORM
alembic==1.13.0            # Migrations
psycopg2-binary==2.9.9     # PostgreSQL driver
redis==5.0.1               # Caching

# Authentication
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4            # Password hashing
python-multipart==0.0.6           # Form data

# Statistics & Analytics
numpy==1.26.2
pandas==2.1.3
scipy==1.11.4              # Statistical functions
statsmodels==0.14.0        # Advanced statistics

# Visualization & Export
matplotlib==3.8.2
reportlab==4.0.7           # PDF generation

# Utilities
python-dotenv==1.0.0       # Environment variables
httpx==0.25.2              # Async HTTP client
celery==5.3.4              # Background tasks (optional)
```

### 3.2 API Architecture

#### 3.2.1 RESTful API Design

```
API Endpoint Structure:

/api/v1
  /auth
    POST   /register          - Create new user account
    POST   /login             - Authenticate and get token
    POST   /logout            - Invalidate token
    POST   /refresh           - Refresh access token
    POST   /reset-password    - Request password reset
    POST   /confirm-reset     - Confirm password reset

  /users
    GET    /me                - Get current user profile
    PATCH  /me                - Update user profile
    DELETE /me                - Delete user account
    GET    /me/settings       - Get user settings
    PATCH  /me/settings       - Update user settings

  /metrics
    GET    /                  - List all user metrics
    POST   /                  - Create new metric
    GET    /{id}              - Get specific metric
    PATCH  /{id}              - Update metric
    DELETE /{id}              - Archive metric
    POST   /{id}/restore      - Restore archived metric

  /entries
    GET    /                  - List entries (with filters)
    POST   /                  - Create new entry
    GET    /{id}              - Get specific entry
    PATCH  /{id}              - Update entry
    DELETE /{id}              - Delete entry
    GET    /date/{date}       - Get entry for specific date

  /sync
    POST   /batch             - Batch sync multiple operations
    GET    /status            - Get sync status
    GET    /changes           - Get changes since timestamp

  /analytics
    GET    /correlations      - Get correlation analysis
    GET    /statistics        - Get statistical summary
    GET    /trends            - Get trend analysis

  /reports
    POST   /generate          - Generate PDF report
    GET    /{id}              - Download generated report

  /export
    GET    /csv               - Export data as CSV
    GET    /json              - Export data as JSON
```

#### 3.2.2 Request/Response Models

```python
# models/requests.py

from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List, Dict, Any

class MetricCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., pattern="^(physical|psychological|triggers|medications|selfcare|wellness|notes)$")
    value_type: str = Field(..., pattern="^(range|number|boolean|count|text)$")
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = None

class EntryCreate(BaseModel):
    date: date
    metric_values: Dict[str, Any]  # {metric_id: value}
    notes: Optional[str] = None

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    language: str = Field(default="en", pattern="^(pl|en)$")
    timezone: str = Field(default="UTC")

class CorrelationRequest(BaseModel):
    metric_ids: List[int]
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    algorithm: str = Field(default="pearson", pattern="^(pearson|spearman|kendall)$")
    max_lag: int = Field(default=7, ge=0, le=30)
    min_significance: float = Field(default=0.05, ge=0, le=1)
```

```python
# models/responses.py

class MetricResponse(BaseModel):
    id: int
    user_id: int
    name: str
    category: str
    value_type: str
    min_value: Optional[float]
    max_value: Optional[float]
    description: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    created_at: datetime
    updated_at: datetime
    archived: bool

class CorrelationResult(BaseModel):
    metric_1_id: int
    metric_2_id: int
    metric_1_name: str
    metric_2_name: str
    coefficient: float
    p_value: float
    lag: int  # Days of lag (0 = no lag)
    strength: str  # "weak", "moderate", "strong"
    significant: bool
    direction: str  # "positive", "negative"
    sample_size: int

class AnalyticsResponse(BaseModel):
    correlations: List[CorrelationResult]
    statistics: Dict[str, Any]
    date_range: Dict[str, date]
    algorithm_used: str
```

### 3.3 Database Architecture

#### 3.3.1 Database Schema

```sql
-- PostgreSQL Schema

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    language VARCHAR(2) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Metrics table
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    value_type VARCHAR(20) NOT NULL,
    min_value DECIMAL(10, 2),
    max_value DECIMAL(10, 2),
    description TEXT,
    color VARCHAR(7),
    icon VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_metric_name UNIQUE(user_id, name)
);

-- Entries table
CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    entry_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_date UNIQUE(user_id, entry_date)
);

-- Entry values table (stores actual metric values)
CREATE TABLE entry_values (
    id SERIAL PRIMARY KEY,
    entry_id INTEGER REFERENCES entries(id) ON DELETE CASCADE,
    metric_id INTEGER REFERENCES metrics(id) ON DELETE CASCADE,
    value_numeric DECIMAL(10, 2),
    value_boolean BOOLEAN,
    value_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_entry_metric UNIQUE(entry_id, metric_id)
);

-- Sync tokens (for optimistic locking)
CREATE TABLE sync_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1
);

-- Indexes for performance
CREATE INDEX idx_metrics_user_id ON metrics(user_id);
CREATE INDEX idx_metrics_category ON metrics(category);
CREATE INDEX idx_entries_user_id ON entries(user_id);
CREATE INDEX idx_entries_date ON entries(entry_date);
CREATE INDEX idx_entry_values_entry_id ON entry_values(entry_id);
CREATE INDEX idx_entry_values_metric_id ON entry_values(metric_id);
```

#### 3.3.2 Database Models (SQLAlchemy)

```python
# database/models.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    language = Column(String(2), default="en")
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    metrics = relationship("Metric", back_populates="user", cascade="all, delete-orphan")
    entries = relationship("Entry", back_populates="user", cascade="all, delete-orphan")

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    value_type = Column(String(20), nullable=False)
    min_value = Column(Numeric(10, 2), nullable=True)
    max_value = Column(Numeric(10, 2), nullable=True)
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)
    icon = Column(String(50), nullable=True)
    display_order = Column(Integer, default=0)
    archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="metrics")
    entry_values = relationship("EntryValue", back_populates="metric", cascade="all, delete-orphan")

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    entry_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="entries")
    values = relationship("EntryValue", back_populates="entry", cascade="all, delete-orphan")

class EntryValue(Base):
    __tablename__ = "entry_values"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("entries.id"), nullable=False)
    metric_id = Column(Integer, ForeignKey("metrics.id"), nullable=False)
    value_numeric = Column(Numeric(10, 2), nullable=True)
    value_boolean = Column(Boolean, nullable=True)
    value_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    entry = relationship("Entry", back_populates="values")
    metric = relationship("Metric", back_populates="entry_values")
```

### 3.4 Authentication & Security

```python
# security/auth.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your-secret-key-here"  # From environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
```

### 3.5 Correlation Engine

```python
# analytics/correlation.py

import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Optional
from models.responses import CorrelationResult

class CorrelationEngine:

    def __init__(self, algorithm: str = "pearson"):
        self.algorithm = algorithm
        self.methods = {
            "pearson": stats.pearsonr,
            "spearman": stats.spearmanr,
            "kendall": stats.kendalltau
        }

    def calculate_correlations(
        self,
        data: pd.DataFrame,
        max_lag: int = 7,
        min_significance: float = 0.05
    ) -> List[CorrelationResult]:
        """
        Calculate correlations between all metric pairs.
        Includes lag correlation analysis.
        """
        results = []
        metrics = data.columns.tolist()

        for i, metric1 in enumerate(metrics):
            for metric2 in metrics[i+1:]:
                # Standard correlation (lag=0)
                corr_result = self._correlate_pair(
                    data[metric1],
                    data[metric2],
                    lag=0
                )
                if corr_result and corr_result.p_value < min_significance:
                    results.append(corr_result)

                # Lag correlations
                for lag in range(1, max_lag + 1):
                    lag_result = self._correlate_with_lag(
                        data[metric1],
                        data[metric2],
                        lag=lag
                    )
                    if lag_result and lag_result.p_value < min_significance:
                        results.append(lag_result)

        # Sort by absolute correlation strength
        results.sort(key=lambda x: abs(x.coefficient), reverse=True)
        return results

    def _correlate_pair(
        self,
        series1: pd.Series,
        series2: pd.Series,
        lag: int = 0
    ) -> Optional[CorrelationResult]:
        """Calculate correlation between two series."""
        # Remove NaN values
        mask = ~(series1.isna() | series2.isna())
        s1 = series1[mask]
        s2 = series2[mask]

        if len(s1) < 3:  # Need at least 3 data points
            return None

        # Calculate correlation
        method = self.methods[self.algorithm]
        coefficient, p_value = method(s1, s2)

        return CorrelationResult(
            metric_1_id=series1.name,
            metric_2_id=series2.name,
            coefficient=float(coefficient),
            p_value=float(p_value),
            lag=lag,
            strength=self._get_strength(coefficient),
            significant=p_value < 0.05,
            direction="positive" if coefficient > 0 else "negative",
            sample_size=len(s1)
        )

    def _correlate_with_lag(
        self,
        series1: pd.Series,
        series2: pd.Series,
        lag: int
    ) -> Optional[CorrelationResult]:
        """Calculate correlation with time lag."""
        if lag == 0:
            return self._correlate_pair(series1, series2, lag=0)

        # Shift series2 by lag days
        series2_shifted = series2.shift(-lag)

        return self._correlate_pair(series1, series2_shifted, lag=lag)

    def _get_strength(self, coefficient: float) -> str:
        """Classify correlation strength."""
        abs_coef = abs(coefficient)
        if abs_coef < 0.3:
            return "weak"
        elif abs_coef < 0.7:
            return "moderate"
        else:
            return "strong"
```

---

## 4. Deployment Architecture

### 4.1 Development Environment

```yaml
# docker-compose.yml

version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"  # Vite dev server
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://feelink:password@db:5432/feelink
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=dev-secret-key
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=feelink
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=feelink
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 4.2 Production Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CDN (CloudFlare)                     │
│              Static Assets + SSL/TLS                    │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│              Load Balancer (NGINX/Traefik)              │
└─────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
┌──────────────────────┐      ┌──────────────────────┐
│   Frontend Server    │      │   Frontend Server    │
│   (Static PWA)       │      │   (Static PWA)       │
│   Docker Container   │      │   Docker Container   │
└──────────────────────┘      └──────────────────────┘
                           │
                  ┌────────┴────────┐
                  │                 │
     ┌────────────────────┐  ┌────────────────────┐
     │  Backend Server 1  │  │  Backend Server 2  │
     │  FastAPI + Python  │  │  FastAPI + Python  │
     │  Docker Container  │  │  Docker Container  │
     └────────────────────┘  └────────────────────┘
                  │                 │
                  └────────┬────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
┌───────────────────────┐    ┌──────────────────────┐
│  PostgreSQL Primary   │───▶│  PostgreSQL Replica  │
│  (Master)             │    │  (Read-only)         │
└───────────────────────┘    └──────────────────────┘
            │
┌───────────────────────┐
│   Redis Cache         │
│   (Session & Cache)   │
└───────────────────────┘
            │
┌───────────────────────┐
│   Backup Storage      │
│   (S3/Object Storage) │
└───────────────────────┘
```

### 4.3 CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml

name: Deploy FeelInk

on:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Backend Tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

      - name: Run Frontend Tests
        run: |
          cd frontend
          npm install
          npm run test

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker Images
        run: |
          docker build -t feelink-frontend:${{ github.sha }} ./frontend
          docker build -t feelink-backend:${{ github.sha }} ./backend

      - name: Push to Registry
        run: |
          docker push feelink-frontend:${{ github.sha }}
          docker push feelink-backend:${{ github.sha }}

      - name: Deploy to Production
        run: |
          # Deploy using your preferred method
          # (Kubernetes, Docker Swarm, etc.)
```

---

## 5. Related Documents

- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
- [REQUIREMENTS.md](./REQUIREMENTS.md)
- [DATA_MODEL.md](./DATA_MODEL.md)
- [CORRELATION_ALGORITHMS.md](./CORRELATION_ALGORITHMS.md)
- [I18N_STRATEGY.md](./I18N_STRATEGY.md)

---

**Next Steps**: Finalize framework selection and begin MVP development.
