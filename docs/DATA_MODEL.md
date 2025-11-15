# Data Model & Schema Design

## Document Information
- **Version**: 0.1.0
- **Last Updated**: 2025-11-15
- **Status**: Schema Specification

---

## 1. Overview

This document defines the complete data model for FeelInk, including:
- Database schemas (PostgreSQL)
- Frontend TypeScript interfaces
- API request/response models
- IndexedDB local storage schemas

---

## 2. Core Entities

### 2.1 Entity Relationship Diagram

```
┌──────────────┐
│    User      │
└──────┬───────┘
       │
       │ 1:N
       │
   ┌───┴────────────────┐
   │                    │
   │                    │
┌──▼─────────┐    ┌────▼──────┐
│  Metric    │    │   Entry   │
└──┬─────────┘    └────┬──────┘
   │                   │
   │ 1:N               │ 1:N
   │                   │
   │              ┌────▼──────────┐
   └──────────────►  EntryValue   │
                  └───────────────┘
```

---

## 3. Database Schema (PostgreSQL)

### 3.1 Users Table

```sql
CREATE TABLE users (
    -- Primary Key
    id                  SERIAL PRIMARY KEY,

    -- Authentication
    email               VARCHAR(255) UNIQUE NOT NULL,
    password_hash       VARCHAR(255) NOT NULL,

    -- Preferences
    language            VARCHAR(2) DEFAULT 'en' CHECK (language IN ('en', 'pl')),
    timezone            VARCHAR(50) DEFAULT 'UTC',

    -- Metadata
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at          TIMESTAMP WITH TIME ZONE NULL,

    -- Indexes
    CONSTRAINT email_lowercase CHECK (email = LOWER(email))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | SERIAL | Auto-incrementing user ID |
| `email` | VARCHAR(255) | User's email (unique, lowercase) |
| `password_hash` | VARCHAR(255) | Bcrypt hashed password |
| `language` | VARCHAR(2) | Preferred language (en/pl) |
| `timezone` | VARCHAR(50) | User's timezone (e.g., "Europe/Warsaw") |
| `created_at` | TIMESTAMP | Account creation timestamp |
| `updated_at` | TIMESTAMP | Last profile update |
| `deleted_at` | TIMESTAMP | Soft delete timestamp (NULL if active) |

---

### 3.2 Metrics Table

```sql
CREATE TABLE metrics (
    -- Primary Key
    id                  SERIAL PRIMARY KEY,

    -- Foreign Key
    user_id             INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Metric Definition
    name_key            VARCHAR(100) NOT NULL,  -- i18n key (e.g., "custom.my_mood")
    category            VARCHAR(50) NOT NULL
                        CHECK (category IN (
                            'physical',
                            'psychological',
                            'triggers',
                            'medications',
                            'selfcare',
                            'wellness',
                            'notes'
                        )),

    -- Value Type & Constraints
    value_type          VARCHAR(20) NOT NULL
                        CHECK (value_type IN (
                            'range',
                            'number',
                            'boolean',
                            'count',
                            'text'
                        )),
    min_value           DECIMAL(10, 2) NULL,
    max_value           DECIMAL(10, 2) NULL,

    -- Display
    description         TEXT NULL,
    color               VARCHAR(7) NULL,        -- Hex color (e.g., "#3B82F6")
    icon                VARCHAR(50) NULL,       -- Icon name
    display_order       INTEGER DEFAULT 0,

    -- Status
    archived            BOOLEAN DEFAULT FALSE,

    -- Metadata
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT unique_user_metric_name UNIQUE(user_id, name_key),
    CONSTRAINT valid_range CHECK (
        (value_type != 'range') OR
        (min_value IS NOT NULL AND max_value IS NOT NULL AND min_value < max_value)
    )
);

CREATE INDEX idx_metrics_user_id ON metrics(user_id);
CREATE INDEX idx_metrics_category ON metrics(category);
CREATE INDEX idx_metrics_archived ON metrics(archived);
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | SERIAL | Auto-incrementing metric ID |
| `user_id` | INTEGER | Owner user ID |
| `name_key` | VARCHAR(100) | i18n translation key |
| `category` | VARCHAR(50) | Metric category (enum) |
| `value_type` | VARCHAR(20) | Data type (range/number/boolean/count/text) |
| `min_value` | DECIMAL | Minimum value (for range type) |
| `max_value` | DECIMAL | Maximum value (for range type) |
| `description` | TEXT | Optional user description |
| `color` | VARCHAR(7) | Hex color for charts |
| `icon` | VARCHAR(50) | Icon identifier |
| `display_order` | INTEGER | Sort order in UI |
| `archived` | BOOLEAN | Whether metric is archived |

---

### 3.3 Entries Table

```sql
CREATE TABLE entries (
    -- Primary Key
    id                  SERIAL PRIMARY KEY,

    -- Foreign Key
    user_id             INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Entry Data
    entry_date          DATE NOT NULL,
    notes               TEXT NULL,

    -- Metadata
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT unique_user_date UNIQUE(user_id, entry_date),
    CONSTRAINT entry_date_not_future CHECK (entry_date <= CURRENT_DATE)
);

CREATE INDEX idx_entries_user_id ON entries(user_id);
CREATE INDEX idx_entries_date ON entries(entry_date);
CREATE INDEX idx_entries_user_date ON entries(user_id, entry_date);
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | SERIAL | Auto-incrementing entry ID |
| `user_id` | INTEGER | Owner user ID |
| `entry_date` | DATE | Date of entry (one per day) |
| `notes` | TEXT | Optional free-form notes |
| `created_at` | TIMESTAMP | When entry was created |
| `updated_at` | TIMESTAMP | Last modification time |

---

### 3.4 Entry Values Table

```sql
CREATE TABLE entry_values (
    -- Primary Key
    id                  SERIAL PRIMARY KEY,

    -- Foreign Keys
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    metric_id           INTEGER NOT NULL REFERENCES metrics(id) ON DELETE CASCADE,

    -- Polymorphic Value Storage
    value_numeric       DECIMAL(10, 2) NULL,
    value_boolean       BOOLEAN NULL,
    value_text          TEXT NULL,

    -- Metadata
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT unique_entry_metric UNIQUE(entry_id, metric_id),
    CONSTRAINT value_not_null CHECK (
        (value_numeric IS NOT NULL) OR
        (value_boolean IS NOT NULL) OR
        (value_text IS NOT NULL)
    )
);

CREATE INDEX idx_entry_values_entry_id ON entry_values(entry_id);
CREATE INDEX idx_entry_values_metric_id ON entry_values(metric_id);
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | SERIAL | Auto-incrementing value ID |
| `entry_id` | INTEGER | Reference to entry |
| `metric_id` | INTEGER | Reference to metric |
| `value_numeric` | DECIMAL | Numeric value (for range/number/count) |
| `value_boolean` | BOOLEAN | Boolean value (for boolean type) |
| `value_text` | TEXT | Text value (for text type) |

**Storage Strategy:**
- `range` type → `value_numeric`
- `number` type → `value_numeric`
- `count` type → `value_numeric`
- `boolean` type → `value_boolean`
- `text` type → `value_text`

---

### 3.5 Sync Metadata Table (for conflict resolution)

```sql
CREATE TABLE sync_metadata (
    -- Primary Key
    id                  SERIAL PRIMARY KEY,

    -- Foreign Key
    user_id             INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Entity Reference
    entity_type         VARCHAR(50) NOT NULL
                        CHECK (entity_type IN ('metric', 'entry', 'entry_value')),
    entity_id           INTEGER NOT NULL,

    -- Sync Tracking
    version             INTEGER DEFAULT 1,
    last_synced         TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    device_id           VARCHAR(255) NULL,

    -- Constraints
    CONSTRAINT unique_entity_sync UNIQUE(entity_type, entity_id)
);

CREATE INDEX idx_sync_user_id ON sync_metadata(user_id);
CREATE INDEX idx_sync_entity ON sync_metadata(entity_type, entity_id);
```

---

## 4. TypeScript Interfaces (Frontend)

### 4.1 User

```typescript
// src/types/user.ts

export interface User {
  id: number;
  email: string;
  language: 'en' | 'pl';
  timezone: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserSettings {
  language: 'en' | 'pl';
  timezone: string;
  notificationsEnabled: boolean;
  dailyReminderTime: string | null; // e.g., "20:00"
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresAt: Date;
}
```

### 4.2 Metric

```typescript
// src/types/metric.ts

export type MetricCategory =
  | 'physical'
  | 'psychological'
  | 'triggers'
  | 'medications'
  | 'selfcare'
  | 'wellness'
  | 'notes';

export type MetricValueType =
  | 'range'
  | 'number'
  | 'boolean'
  | 'count'
  | 'text';

export interface Metric {
  id: number;
  userId: number;
  nameKey: string;           // i18n key
  category: MetricCategory;
  valueType: MetricValueType;
  minValue: number | null;
  maxValue: number | null;
  description: string | null;
  color: string | null;      // Hex color
  icon: string | null;
  displayOrder: number;
  archived: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface MetricCreate {
  nameKey: string;
  category: MetricCategory;
  valueType: MetricValueType;
  minValue?: number;
  maxValue?: number;
  description?: string;
  color?: string;
  icon?: string;
}

export interface MetricUpdate {
  nameKey?: string;
  category?: MetricCategory;
  description?: string;
  color?: string;
  icon?: string;
  displayOrder?: number;
  archived?: boolean;
}
```

### 4.3 Entry & Entry Value

```typescript
// src/types/entry.ts

export type MetricValue = number | boolean | string;

export interface EntryValue {
  metricId: number;
  value: MetricValue;
}

export interface Entry {
  id: number;
  userId: number;
  entryDate: string;         // ISO date string "YYYY-MM-DD"
  notes: string | null;
  values: EntryValue[];
  createdAt: Date;
  updatedAt: Date;
}

export interface EntryCreate {
  entryDate: string;         // "YYYY-MM-DD"
  notes?: string;
  values: EntryValue[];
}

export interface EntryUpdate {
  notes?: string;
  values?: EntryValue[];
}

// For daily log form
export interface DailyLogFormData {
  date: string;
  notes: string;
  metricValues: Record<number, MetricValue>; // metricId → value
}
```

### 4.4 Analytics & Correlations

```typescript
// src/types/analytics.ts

export interface CorrelationResult {
  metric1Id: number;
  metric2Id: number;
  metric1Name: string;
  metric2Name: string;
  coefficient: number;       // -1 to 1
  pValue: number;           // 0 to 1
  lag: number;              // Days (0 = no lag)
  strength: 'weak' | 'moderate' | 'strong';
  significance: 'not_significant' | 'marginally_significant' | 'significant' | 'highly_significant';
  direction: 'positive' | 'negative';
  sampleSize: number;
}

export interface CorrelationRequest {
  metricIds?: number[];     // If empty, analyze all
  dateFrom?: string;
  dateTo?: string;
  algorithm: 'pearson' | 'spearman' | 'kendall';
  maxLag: number;           // Default 7
  minSignificance: number;  // Default 0.05
}

export interface StatisticsSummary {
  metricId: number;
  metricName: string;
  count: number;
  mean: number;
  median: number;
  min: number;
  max: number;
  stdDev: number;
  trend: 'increasing' | 'decreasing' | 'stable';
}

export interface AnalyticsResponse {
  correlations: CorrelationResult[];
  statistics: StatisticsSummary[];
  dateRange: {
    from: string;
    to: string;
  };
  algorithmUsed: string;
}
```

### 4.5 Report

```typescript
// src/types/report.ts

export interface ReportRequest {
  dateFrom: string;
  dateTo: string;
  includeMetrics: number[];
  includeCorrelations: boolean;
  maxCorrelations: number;  // Top N correlations
  includeCharts: boolean;
  notes?: string;
}

export interface ReportMetadata {
  id: string;
  userId: number;
  generatedAt: Date;
  dateRange: {
    from: string;
    to: string;
  };
  fileUrl: string;         // URL to download PDF
  expiresAt: Date;
}
```

---

## 5. IndexedDB Schema (Offline Storage)

### 5.1 Database Structure

```typescript
// src/db/schema.ts

import Dexie, { Table } from 'dexie';
import type { Metric, Entry, User } from '@/types';

export class FeelinkDatabase extends Dexie {
  // Tables
  users!: Table<User, number>;
  metrics!: Table<Metric, number>;
  entries!: Table<Entry, number>;
  syncQueue!: Table<SyncOperation, number>;
  settings!: Table<LocalSettings, string>;

  constructor() {
    super('feelink');

    this.version(1).stores({
      users: 'id, email',
      metrics: 'id, userId, category, archived, [userId+archived]',
      entries: 'id, userId, entryDate, [userId+entryDate]',
      syncQueue: '++id, operation, timestamp, status',
      settings: 'key'
    });
  }
}

export const db = new FeelinkDatabase();
```

### 5.2 Sync Queue

```typescript
// Sync operation tracking

export interface SyncOperation {
  id?: number;              // Auto-increment
  operation: 'CREATE' | 'UPDATE' | 'DELETE';
  entityType: 'metric' | 'entry';
  entityId: number | null;  // NULL for CREATE before server assigns ID
  payload: any;
  timestamp: Date;
  status: 'pending' | 'syncing' | 'completed' | 'failed';
  retryCount: number;
  lastError: string | null;
}
```

### 5.3 Local Settings

```typescript
export interface LocalSettings {
  key: string;
  value: any;
}

// Examples:
// { key: 'lastSyncTime', value: '2025-11-15T10:30:00Z' }
// { key: 'preferredTheme', value: 'light' }
// { key: 'onboardingCompleted', value: true }
```

---

## 6. API Request/Response Models

### 6.1 Authentication

```typescript
// POST /api/v1/auth/register
export interface RegisterRequest {
  email: string;
  password: string;
  language?: 'en' | 'pl';
  timezone?: string;
}

export interface RegisterResponse {
  user: User;
  tokens: AuthTokens;
}

// POST /api/v1/auth/login
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  tokens: AuthTokens;
}
```

### 6.2 Metrics

```typescript
// GET /api/v1/metrics
export interface MetricsListResponse {
  metrics: Metric[];
  total: number;
}

// POST /api/v1/metrics
export interface MetricCreateRequest {
  nameKey: string;
  category: MetricCategory;
  valueType: MetricValueType;
  minValue?: number;
  maxValue?: number;
  description?: string;
  color?: string;
  icon?: string;
}

export interface MetricCreateResponse {
  metric: Metric;
}

// PATCH /api/v1/metrics/:id
export interface MetricUpdateRequest {
  nameKey?: string;
  category?: MetricCategory;
  description?: string;
  color?: string;
  icon?: string;
  displayOrder?: number;
  archived?: boolean;
}

export interface MetricUpdateResponse {
  metric: Metric;
}
```

### 6.3 Entries

```typescript
// GET /api/v1/entries?from=2025-11-01&to=2025-11-30
export interface EntriesListQuery {
  from?: string;            // ISO date
  to?: string;
  limit?: number;
  offset?: number;
}

export interface EntriesListResponse {
  entries: Entry[];
  total: number;
  hasMore: boolean;
}

// POST /api/v1/entries
export interface EntryCreateRequest {
  entryDate: string;
  notes?: string;
  values: Array<{
    metricId: number;
    value: MetricValue;
  }>;
}

export interface EntryCreateResponse {
  entry: Entry;
}

// PATCH /api/v1/entries/:id
export interface EntryUpdateRequest {
  notes?: string;
  values?: Array<{
    metricId: number;
    value: MetricValue;
  }>;
}

export interface EntryUpdateResponse {
  entry: Entry;
}
```

### 6.4 Batch Sync

```typescript
// POST /api/v1/sync/batch
export interface BatchSyncRequest {
  operations: Array<{
    operation: 'CREATE' | 'UPDATE' | 'DELETE';
    entityType: 'metric' | 'entry';
    entityId?: number;
    payload: any;
    clientTimestamp: string;
  }>;
  lastSyncTime: string | null;
}

export interface BatchSyncResponse {
  results: Array<{
    operation: string;
    success: boolean;
    entityId?: number;
    serverId?: number;      // For CREATE operations
    error?: string;
  }>;
  serverTime: string;
  changes: {                // Changes from other devices
    metrics: Metric[];
    entries: Entry[];
    deletedMetrics: number[];
    deletedEntries: number[];
  };
}
```

### 6.5 Analytics

```typescript
// GET /api/v1/analytics/correlations
export interface CorrelationsQuery {
  metricIds?: string;       // Comma-separated IDs
  dateFrom?: string;
  dateTo?: string;
  algorithm?: 'pearson' | 'spearman' | 'kendall';
  maxLag?: number;
  minSignificance?: number;
}

export interface CorrelationsResponse {
  correlations: CorrelationResult[];
  metadata: {
    dateRange: { from: string; to: string };
    algorithm: string;
    totalPairsTested: number;
    significantPairs: number;
  };
}

// GET /api/v1/analytics/statistics
export interface StatisticsResponse {
  statistics: StatisticsSummary[];
  dateRange: { from: string; to: string };
}
```

### 6.6 Export

```typescript
// GET /api/v1/export/csv
export interface ExportCsvQuery {
  dateFrom?: string;
  dateTo?: string;
  includeMetrics: boolean;
  includeEntries: boolean;
}

// Response: CSV file download

// GET /api/v1/export/json
export interface ExportJsonQuery {
  dateFrom?: string;
  dateTo?: string;
}

export interface ExportJsonResponse {
  version: string;
  exportDate: string;
  user: {
    email: string;
    timezone: string;
    language: string;
  };
  metrics: Metric[];
  entries: Entry[];
}
```

---

## 7. Validation Rules

### 7.1 User

```typescript
const userValidation = {
  email: {
    required: true,
    format: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    maxLength: 255
  },
  password: {
    required: true,
    minLength: 8,
    maxLength: 128,
    pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, // At least 1 lowercase, 1 uppercase, 1 digit
  },
  language: {
    enum: ['en', 'pl']
  },
  timezone: {
    valid: Intl.supportedValuesOf('timeZone') // IANA timezone
  }
};
```

### 7.2 Metric

```typescript
const metricValidation = {
  nameKey: {
    required: true,
    minLength: 1,
    maxLength: 100,
    pattern: /^[a-z0-9_.]+$/  // Lowercase, numbers, dots, underscores
  },
  category: {
    required: true,
    enum: ['physical', 'psychological', 'triggers', 'medications', 'selfcare', 'wellness', 'notes']
  },
  valueType: {
    required: true,
    enum: ['range', 'number', 'boolean', 'count', 'text']
  },
  minValue: {
    requiredIf: (metric) => metric.valueType === 'range',
    type: 'number'
  },
  maxValue: {
    requiredIf: (metric) => metric.valueType === 'range',
    type: 'number',
    greaterThan: 'minValue'
  },
  color: {
    pattern: /^#[0-9A-Fa-f]{6}$/
  }
};
```

### 7.3 Entry

```typescript
const entryValidation = {
  entryDate: {
    required: true,
    format: 'YYYY-MM-DD',
    notFuture: true
  },
  values: {
    required: true,
    minLength: 1,
    validate: (values, metrics) => {
      return values.every(v => {
        const metric = metrics.find(m => m.id === v.metricId);
        if (!metric) return false;

        switch (metric.valueType) {
          case 'range':
          case 'number':
          case 'count':
            return typeof v.value === 'number' &&
                   (!metric.minValue || v.value >= metric.minValue) &&
                   (!metric.maxValue || v.value <= metric.maxValue);
          case 'boolean':
            return typeof v.value === 'boolean';
          case 'text':
            return typeof v.value === 'string';
          default:
            return false;
        }
      });
    }
  }
};
```

---

## 8. Sample Data

### 8.1 Sample User

```json
{
  "id": 1,
  "email": "user@example.com",
  "language": "en",
  "timezone": "Europe/Warsaw",
  "createdAt": "2025-11-01T10:00:00Z",
  "updatedAt": "2025-11-15T12:30:00Z"
}
```

### 8.2 Sample Metrics

```json
[
  {
    "id": 1,
    "userId": 1,
    "nameKey": "mood",
    "category": "psychological",
    "valueType": "range",
    "minValue": 1,
    "maxValue": 10,
    "description": "Overall mood level",
    "color": "#8B5CF6",
    "icon": "smile",
    "displayOrder": 1,
    "archived": false,
    "createdAt": "2025-11-01T10:05:00Z",
    "updatedAt": "2025-11-01T10:05:00Z"
  },
  {
    "id": 2,
    "userId": 1,
    "nameKey": "sleep_hours",
    "category": "wellness",
    "valueType": "number",
    "minValue": null,
    "maxValue": null,
    "description": "Hours of sleep",
    "color": "#3B82F6",
    "icon": "moon",
    "displayOrder": 2,
    "archived": false,
    "createdAt": "2025-11-01T10:06:00Z",
    "updatedAt": "2025-11-01T10:06:00Z"
  },
  {
    "id": 3,
    "userId": 1,
    "nameKey": "exercised",
    "category": "wellness",
    "valueType": "boolean",
    "minValue": null,
    "maxValue": null,
    "description": "Did I exercise today?",
    "color": "#10B981",
    "icon": "activity",
    "displayOrder": 3,
    "archived": false,
    "createdAt": "2025-11-01T10:07:00Z",
    "updatedAt": "2025-11-01T10:07:00Z"
  }
]
```

### 8.3 Sample Entry

```json
{
  "id": 1,
  "userId": 1,
  "entryDate": "2025-11-15",
  "notes": "Felt great today after morning run",
  "values": [
    {
      "metricId": 1,
      "value": 8
    },
    {
      "metricId": 2,
      "value": 7.5
    },
    {
      "metricId": 3,
      "value": true
    }
  ],
  "createdAt": "2025-11-15T20:00:00Z",
  "updatedAt": "2025-11-15T20:00:00Z"
}
```

### 8.4 Sample Correlation Result

```json
{
  "metric1Id": 2,
  "metric2Id": 1,
  "metric1Name": "Sleep Hours",
  "metric2Name": "Mood",
  "coefficient": 0.82,
  "pValue": 0.001,
  "lag": 0,
  "strength": "strong",
  "significance": "highly_significant",
  "direction": "positive",
  "sampleSize": 30
}
```

---

## 9. Data Migration Strategy

### 9.1 Version 1 → Version 2 (Future Example)

```sql
-- Add new field to metrics table
ALTER TABLE metrics
ADD COLUMN unit VARCHAR(50) NULL;

-- Update version
UPDATE schema_version SET version = 2;
```

### 9.2 Migration Script Template

```typescript
// src/db/migrations/002_add_metric_units.ts

export async function up(db: Dexie) {
  // Add new field to metrics
  await db.version(2).stores({
    metrics: 'id, userId, category, archived, unit, [userId+archived]'
  });

  // Migrate existing data
  await db.metrics.toCollection().modify((metric: any) => {
    metric.unit = null; // Default value
  });
}

export async function down(db: Dexie) {
  // Rollback
  await db.version(1).stores({
    metrics: 'id, userId, category, archived, [userId+archived]'
  });
}
```

---

## 10. Performance Considerations

### 10.1 Database Indexes

Already defined in schema, but key indexes:
- `idx_entries_user_date` - Fast lookup for daily log
- `idx_entry_values_metric_id` - Fast metric-based queries
- `idx_metrics_user_id` - Fast user metrics list

### 10.2 Query Optimization

```sql
-- Efficient query for correlation analysis
-- Fetch all entries for a user in date range with values
SELECT
    e.entry_date,
    ev.metric_id,
    ev.value_numeric,
    ev.value_boolean,
    m.value_type
FROM entries e
JOIN entry_values ev ON ev.entry_id = e.id
JOIN metrics m ON m.id = ev.metric_id
WHERE
    e.user_id = $1
    AND e.entry_date BETWEEN $2 AND $3
    AND m.archived = FALSE
ORDER BY e.entry_date, ev.metric_id;
```

### 10.3 Data Archival

For users with years of data:
```sql
-- Archive old entries (keep last 2 years hot)
CREATE TABLE entries_archive (LIKE entries INCLUDING ALL);

INSERT INTO entries_archive
SELECT * FROM entries
WHERE entry_date < (CURRENT_DATE - INTERVAL '2 years');

DELETE FROM entries
WHERE entry_date < (CURRENT_DATE - INTERVAL '2 years');
```

---

## 11. Related Documents

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical architecture
- [REQUIREMENTS.md](./REQUIREMENTS.md) - Functional requirements
- [PRIVACY_AND_SECURITY.md](./PRIVACY_AND_SECURITY.md) - Security approach

---

**Status**: Schema ready for implementation
**Next Steps**: Generate database migrations and TypeScript types
