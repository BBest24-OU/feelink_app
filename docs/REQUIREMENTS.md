# FeelInk - Requirements Specification

## Document Information
- **Version**: 0.1.0
- **Last Updated**: 2025-11-15
- **Status**: Draft

---

## 1. Functional Requirements

### 1.1 Metric Management

#### 1.1.1 Metric Categories
**Priority**: MUST HAVE

**Requirements**:
- FR-1.1.1: System SHALL provide predefined metric categories:
  - Physical Symptoms
  - Psychological Symptoms
  - Triggers
  - Medications
  - Self-Care
  - Wellness
  - Notes
- FR-1.1.2: Users SHALL be able to create custom metrics within each category
- FR-1.1.3: Users SHALL be able to edit metric definitions
- FR-1.1.4: Users SHALL be able to archive (not delete) unused metrics
- FR-1.1.5: Users SHALL be able to reorder metrics for display priority

#### 1.1.2 Metric Value Types
**Priority**: MUST HAVE

**Requirements**:
- FR-1.2.1: System SHALL support the following value types:
  - Range (min-max with configurable bounds)
  - Integer/Decimal number
  - Boolean (yes/no, true/false)
  - Count (non-negative integer)
  - Free text (optional note)
- FR-1.2.2: Each metric SHALL have exactly one primary value type
- FR-1.2.3: All metrics SHALL support optional text notes
- FR-1.2.4: Range metrics SHALL allow custom min/max values (e.g., 1-5, 0-100)
- FR-1.2.5: Metrics SHALL have user-defined names (externalized, translatable)

#### 1.1.3 Metric Configuration
**Priority**: MUST HAVE

**Requirements**:
- FR-1.3.1: Users SHALL define metric name (translatable string key)
- FR-1.3.2: Users SHALL select metric category
- FR-1.3.3: Users SHALL select value type
- FR-1.3.4: Users SHALL configure value constraints (min/max for ranges)
- FR-1.3.5: Users SHALL optionally add metric description
- FR-1.3.6: Users SHALL be able to set metric color/icon for quick recognition

### 1.2 Daily Logging

#### 1.2.1 Quick Entry Interface
**Priority**: MUST HAVE

**Requirements**:
- FR-2.1.1: Daily log form SHALL display all active metrics
- FR-2.1.2: Form completion time SHALL target <60 seconds
- FR-2.1.3: Form SHALL be mobile-optimized (large touch targets)
- FR-2.1.4: Form SHALL support partial completion (save draft)
- FR-2.1.5: Form SHALL show completion progress indicator
- FR-2.1.6: Previously entered values SHALL be visible (for reference)

#### 1.2.2 Data Entry Controls
**Priority**: MUST HAVE

**Requirements**:
- FR-2.2.1: Range metrics SHALL use sliders or number inputs
- FR-2.2.2: Boolean metrics SHALL use toggle switches or checkboxes
- FR-2.2.3: Count metrics SHALL use number steppers
- FR-2.2.4: Note fields SHALL use expandable text areas
- FR-2.2.5: All controls SHALL be keyboard and screen-reader accessible

#### 1.2.3 Entry Validation
**Priority**: MUST HAVE

**Requirements**:
- FR-2.3.1: System SHALL validate values against metric constraints
- FR-2.3.2: System SHALL prevent submission of invalid data
- FR-2.3.3: System SHALL show clear validation error messages
- FR-2.3.4: System SHALL allow skipping optional metrics
- FR-2.3.5: System SHALL timestamp each entry automatically

#### 1.2.4 Historical Entries
**Priority**: SHOULD HAVE

**Requirements**:
- FR-2.4.1: Users SHALL be able to view past entries
- FR-2.4.2: Users SHALL be able to edit entries within 24 hours
- FR-2.4.3: Users SHALL be able to add missed entries for past dates
- FR-2.4.4: System SHALL mark edited/backdated entries clearly
- FR-2.4.5: Users SHALL be able to delete entries with confirmation

### 1.3 Data Visualization

#### 1.3.1 Chart Types
**Priority**: MUST HAVE

**Requirements**:
- FR-3.1.1: System SHALL provide line charts for metric trends over time
- FR-3.1.2: System SHALL provide scatter plots for correlation visualization
- FR-3.1.3: System SHALL provide heatmaps for pattern recognition
- FR-3.1.4: System SHALL provide calendar view for daily overview
- FR-3.1.5: Charts SHALL be interactive (zoom, pan, tooltip details)

#### 1.3.2 Visualization Features
**Priority**: MUST HAVE

**Requirements**:
- FR-3.2.1: Users SHALL select time range for visualization (7d, 30d, 90d, all)
- FR-3.2.2: Users SHALL select which metrics to display
- FR-3.2.3: Charts SHALL be responsive and mobile-friendly
- FR-3.2.4: Charts SHALL use consistent color scheme from theme
- FR-3.2.5: Charts SHALL include clear legends and axis labels

#### 1.3.3 Data Insights
**Priority**: SHOULD HAVE

**Requirements**:
- FR-3.3.1: System SHALL highlight significant trends
- FR-3.3.2: System SHALL show basic statistics (mean, median, range)
- FR-3.3.3: System SHALL indicate data sufficiency for correlations
- FR-3.3.4: System SHALL suggest interesting metric pairs to compare

### 1.4 Correlation Analysis

#### 1.4.1 Correlation Engine
**Priority**: MUST HAVE

**Requirements**:
- FR-4.1.1: System SHALL calculate correlations between numeric metrics
- FR-4.1.2: System SHALL support lag correlation analysis (time-delayed effects)
- FR-4.1.3: System SHALL calculate cross-correlations between metric pairs
- FR-4.1.4: System SHALL provide statistical significance indicators (p-values)
- FR-4.1.5: System SHALL require minimum data points (e.g., 7 days) before showing correlations

#### 1.4.2 Correlation Display
**Priority**: MUST HAVE

**Requirements**:
- FR-4.2.1: System SHALL show correlation coefficient (-1 to +1)
- FR-4.2.2: System SHALL show correlation strength interpretation (weak/moderate/strong)
- FR-4.2.3: System SHALL show lag time for delayed correlations
- FR-4.2.4: System SHALL sort correlations by strength
- FR-4.2.5: System SHALL filter correlations by significance threshold

#### 1.4.3 Algorithm Selection
**Priority**: SHOULD HAVE

**Requirements**:
- FR-4.3.1: System SHALL support multiple correlation algorithms
- FR-4.3.2: Users SHALL be able to select preferred algorithm
- FR-4.3.3: System SHALL provide algorithm descriptions
- FR-4.3.4: Results SHALL indicate which algorithm was used

### 1.5 Report Generation

#### 1.5.1 PDF Reports
**Priority**: MUST HAVE

**Requirements**:
- FR-5.1.1: System SHALL generate one-page PDF summary report
- FR-5.1.2: Report SHALL include user-selected date range
- FR-5.1.3: Report SHALL include top correlations (user-selected count)
- FR-5.1.4: Report SHALL include key metrics visualization
- FR-5.1.5: Report SHALL include statistical summary
- FR-5.1.6: Report SHALL be professionally formatted for clinical use
- FR-5.1.7: Report SHALL include generation date and data range

#### 1.5.2 Data Export
**Priority**: MUST HAVE

**Requirements**:
- FR-5.2.1: System SHALL export all user data to CSV format
- FR-5.2.2: System SHALL export all user data to JSON format
- FR-5.2.3: Export SHALL include all metrics and their definitions
- FR-5.2.4: Export SHALL include all logged entries with timestamps
- FR-5.2.5: Export SHALL include user preferences and configuration
- FR-5.2.6: Export format SHALL be well-documented and human-readable

#### 1.5.3 Report Customization
**Priority**: SHOULD HAVE

**Requirements**:
- FR-5.3.1: Users SHALL select which correlations to include
- FR-5.3.2: Users SHALL select which visualizations to include
- FR-5.3.3: Users SHALL add custom notes to report
- FR-5.3.4: Users SHALL preview report before generation

### 1.6 Offline Functionality

#### 1.6.1 Offline-First Architecture
**Priority**: MUST HAVE

**Requirements**:
- FR-6.1.1: Application SHALL work fully offline after initial load
- FR-6.1.2: All core features SHALL be available offline
- FR-6.1.3: Data SHALL be stored locally using browser storage
- FR-6.1.4: Application SHALL detect online/offline status
- FR-6.1.5: Application SHALL queue operations when offline

#### 1.6.2 Data Synchronization
**Priority**: MUST HAVE

**Requirements**:
- FR-6.2.1: System SHALL sync data when connection is restored
- FR-6.2.2: System SHALL handle sync conflicts intelligently
- FR-6.2.3: System SHALL show sync status to user
- FR-6.2.4: System SHALL allow manual sync trigger
- FR-6.2.5: System SHALL maintain data consistency across devices

### 1.7 Internationalization (i18n)

#### 1.7.1 Language Support
**Priority**: MUST HAVE

**Requirements**:
- FR-7.1.1: Application SHALL support Polish language
- FR-7.1.2: Application SHALL support English language
- FR-7.1.3: Users SHALL be able to switch language at runtime
- FR-7.1.4: Language preference SHALL persist across sessions
- FR-7.1.5: Browser language SHALL be detected and set as default

#### 1.7.2 Translation Architecture
**Priority**: MUST HAVE

**Requirements**:
- FR-7.2.1: ALL user-facing strings SHALL be externalized
- FR-7.2.2: NO hardcoded strings SHALL exist in source code
- FR-7.2.3: Translation files SHALL use standard format (e.g., JSON, YAML)
- FR-7.2.4: Missing translations SHALL fallback to English
- FR-7.2.5: Date, time, and number formats SHALL respect locale

### 1.8 User Management

#### 1.8.1 Authentication
**Priority**: MUST HAVE

**Requirements**:
- FR-8.1.1: Users SHALL create account with email and password
- FR-8.1.2: Users SHALL be able to reset forgotten password
- FR-8.1.3: System SHALL enforce password strength requirements
- FR-8.1.4: Users SHALL be able to change password
- FR-8.1.5: Sessions SHALL expire after configurable timeout

#### 1.8.2 Profile Management
**Priority**: SHOULD HAVE

**Requirements**:
- FR-8.2.1: Users SHALL set profile timezone
- FR-8.2.2: Users SHALL configure notification preferences
- FR-8.2.3: Users SHALL set preferred language
- FR-8.2.4: Users SHALL be able to delete account and all data

---

## 2. Non-Functional Requirements

### 2.1 Performance

**NFR-1.1**: Application SHALL load initial page in <3 seconds on 4G connection
**NFR-1.2**: Daily log form SHALL respond to input in <100ms
**NFR-1.3**: Chart rendering SHALL complete in <2 seconds for 90 days of data
**NFR-1.4**: Correlation calculation SHALL complete in <5 seconds for 365 days of data
**NFR-1.5**: Application SHALL support at least 1000 daily entries without performance degradation

### 2.2 Usability

**NFR-2.1**: Daily log completion SHALL take <60 seconds on average
**NFR-2.2**: Application SHALL achieve SUS (System Usability Scale) score >75
**NFR-2.3**: New users SHALL complete first entry within 5 minutes of onboarding
**NFR-2.4**: Application SHALL work on touch screens with target size ≥44×44 pixels
**NFR-2.5**: Font size SHALL be ≥16px for body text on mobile

### 2.3 Accessibility

**NFR-3.1**: Application SHALL meet WCAG 2.1 Level AA compliance
**NFR-3.2**: All interactive elements SHALL be keyboard accessible
**NFR-3.3**: All images and charts SHALL have meaningful alt text
**NFR-3.4**: Color contrast SHALL meet WCAG AA standards (4.5:1 for normal text)
**NFR-3.5**: Application SHALL be screen-reader friendly

### 2.4 Compatibility

**NFR-4.1**: Application SHALL work on iOS Safari (latest 2 versions)
**NFR-4.2**: Application SHALL work on Android Chrome (latest 2 versions)
**NFR-4.3**: Application SHALL work on desktop Chrome, Firefox, Safari, Edge (latest versions)
**NFR-4.4**: PWA SHALL be installable on iOS and Android
**NFR-4.5**: Application SHALL work on viewport sizes from 320px to 2560px width

### 2.5 Security

**NFR-5.1**: All data transmission SHALL use HTTPS/TLS 1.3+
**NFR-5.2**: Sensitive data SHALL be encrypted at rest
**NFR-5.3**: Authentication tokens SHALL expire after 24 hours
**NFR-5.4**: Application SHALL protect against OWASP Top 10 vulnerabilities
**NFR-5.5**: User passwords SHALL be hashed using bcrypt or stronger

### 2.6 Privacy

**NFR-6.1**: Application SHALL comply with GDPR requirements
**NFR-6.2**: Users SHALL have right to export all personal data
**NFR-6.3**: Users SHALL have right to delete all personal data
**NFR-6.4**: Privacy policy SHALL be clear and accessible
**NFR-6.5**: No personal data SHALL be shared with third parties without consent

### 2.7 Scalability

**NFR-7.1**: System SHALL support 10,000 active users initially
**NFR-7.2**: Database SHALL scale to millions of entries
**NFR-7.3**: API SHALL handle 100 requests/second per server
**NFR-7.4**: System architecture SHALL allow horizontal scaling

### 2.8 Maintainability

**NFR-8.1**: Code SHALL have >80% test coverage
**NFR-8.2**: All functions SHALL have clear documentation
**NFR-8.3**: Code SHALL follow consistent style guide
**NFR-8.4**: Dependencies SHALL be kept up-to-date
**NFR-8.5**: System SHALL use centralized theme/style management

### 2.9 Reliability

**NFR-9.1**: Application SHALL have 99.5% uptime
**NFR-9.2**: Data loss SHALL be prevented through automated backups
**NFR-9.3**: System SHALL recover gracefully from errors
**NFR-9.4**: Failed sync operations SHALL retry automatically
**NFR-9.5**: Application SHALL handle network interruptions gracefully

### 2.10 Portability

**NFR-10.1**: Backend SHALL be containerized (Docker)
**NFR-10.2**: Application SHALL be deployable on major cloud platforms (AWS, Azure, GCP)
**NFR-10.3**: Database SHALL use standard SQL or document format
**NFR-10.4**: API SHALL follow RESTful conventions

---

## 3. Constraints

### 3.1 Technical Constraints
- **TC-1**: Must be PWA installable
- **TC-2**: Must work offline-first
- **TC-3**: Must use Python backend (Flask/FastAPI)
- **TC-4**: Must support PL/EN languages from start
- **TC-5**: Must externalize all strings and styles

### 3.2 Business Constraints
- **BC-1**: Initial budget is limited (lightweight stack)
- **BC-2**: Must launch MVP within 3-6 months
- **BC-3**: Must comply with healthcare data regulations

### 3.3 Design Constraints
- **DC-1**: Mobile-first design mandatory
- **DC-2**: Light theme initially (dark theme future)
- **DC-3**: Professional, clinical aesthetic required
- **DC-4**: No vendor lock-in philosophy

---

## 4. Assumptions

- **A-1**: Users have smartphone or computer with modern browser
- **A-2**: Users can commit to 1 minute daily logging
- **A-3**: Users have basic digital literacy
- **A-4**: 7+ days of data needed for meaningful correlations
- **A-5**: Users track for therapy/medical purposes primarily

---

## 5. Dependencies

### 5.1 External Dependencies
- Cloud hosting provider (AWS/Azure/GCP/Vercel)
- SSL certificate provider
- Email service for authentication
- Analytics service (privacy-focused)

### 5.2 Technical Dependencies
- Modern browser with ServiceWorker support
- IndexedDB for local storage
- Chart visualization library
- PDF generation library
- Statistical computation library

---

## 6. Future Enhancements (Out of Scope for MVP)

- **FE-1**: Dark mode support
- **FE-2**: Wearable device integration
- **FE-3**: AI-powered insight suggestions
- **FE-4**: Social/community features
- **FE-5**: Therapist collaboration portal
- **FE-6**: Voice input for quick logging
- **FE-7**: Photo/image attachments to entries
- **FE-8**: Reminder/notification system
- **FE-9**: Advanced machine learning predictions
- **FE-10**: Additional languages beyond PL/EN

---

## 7. Acceptance Criteria

### 7.1 MVP Acceptance
The MVP is considered complete when:
1. User can create custom metrics across all categories
2. User can complete daily log in <60 seconds on mobile
3. Application works fully offline
4. Data syncs when online
5. User can view basic charts (line, scatter)
6. User can see correlation analysis with ≥7 days data
7. User can export data to CSV/JSON
8. Application works in PL and EN languages
9. Application is installable as PWA
10. All MUST HAVE requirements are implemented

---

## Document Control

**Reviewed By**: [Pending]
**Approved By**: [Pending]
**Next Review Date**: [After initial implementation]

## Related Documents
- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [DATA_MODEL.md](./DATA_MODEL.md)
