# Privacy & Security

## Document Information
- **Version**: 0.1.0
- **Last Updated**: 2025-11-15
- **Status**: Security & Privacy Specification
- **Compliance**: GDPR, healthcare data best practices

---

## 1. Core Principles

### 1.1 Privacy-First Philosophy

**"Your Data. Your Control. Your Freedom."**

1. **Data Ownership**: User owns 100% of their data
2. **No Vendor Lock-in**: Full export capabilities (CSV/JSON/PDF)
3. **Minimal Collection**: Collect only what's necessary
4. **Transparent Processing**: Clear about what we do with data
5. **User Control**: Users decide what to track, share, and delete
6. **No Third-Party Sharing**: Never sell or share data with third parties
7. **No Advertisements**: Business model does not rely on data monetization

### 1.2 Regulatory Compliance

✅ **GDPR (General Data Protection Regulation)**
- Right to access
- Right to rectification
- Right to erasure ("right to be forgotten")
- Right to data portability
- Right to object
- Data minimization
- Privacy by design

✅ **Healthcare Data Best Practices**
- While not strictly medical records, treat mental health data as sensitive
- Encryption at rest and in transit
- Access controls
- Audit logging

---

## 2. Data Classification

### 2.1 Data Categories

| Category | Examples | Sensitivity | Retention |
|----------|----------|-------------|-----------|
| **Identity** | Email | High | Until account deletion |
| **Authentication** | Password hash | Critical | Until account deletion |
| **Health Data** | Mood, symptoms, metrics | Critical | User-controlled |
| **Usage Data** | Login times, feature usage | Low | 90 days |
| **Settings** | Language, timezone | Low | Until account deletion |
| **Analytics** | Correlations calculated | Medium | User-controlled |

### 2.2 Sensitive Personal Data

**Mental health tracking data is considered sensitive personal information.**

Protection measures:
- ✅ Encryption at rest (database level)
- ✅ Encryption in transit (TLS 1.3+)
- ✅ Access controls (user can only access their own data)
- ✅ Audit logging (who accessed what, when)
- ✅ Secure deletion (data is unrecoverable)

---

## 3. Security Architecture

### 3.1 Authentication

#### Password Security

```python
# Backend password hashing
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Cost factor (higher = more secure, slower)
)

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)
```

**Password Requirements:**
- Minimum length: 8 characters
- Must contain: 1 lowercase, 1 uppercase, 1 digit
- Maximum length: 128 characters
- No common passwords (check against breached password database)
- Password strength meter in UI

#### JWT Tokens

```python
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY")  # From secure environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 30

def create_access_token(user_id: int) -> str:
    """Create JWT access token."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access"
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    """Create JWT refresh token."""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**Token Storage:**
- Frontend: Stored in memory (not localStorage or cookies)
- Backend: Refresh tokens in httpOnly cookies
- Automatic refresh before expiration

#### Session Management

```typescript
// Frontend session manager

class SessionManager {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private tokenRefreshTimer: number | null = null;

  setTokens(access: string, refresh: string) {
    this.accessToken = access;
    this.refreshToken = refresh;

    // Schedule refresh 5 minutes before expiration
    const expiresIn = this.getTokenExpiry(access);
    this.tokenRefreshTimer = setTimeout(
      () => this.refreshAccessToken(),
      (expiresIn - 5 * 60) * 1000
    );
  }

  async refreshAccessToken() {
    const response = await fetch('/api/v1/auth/refresh', {
      method: 'POST',
      credentials: 'include', // Send refresh token cookie
    });

    if (response.ok) {
      const { accessToken } = await response.json();
      this.accessToken = accessToken;
      // Reschedule next refresh
      this.scheduleRefresh(accessToken);
    } else {
      // Refresh failed, user needs to login again
      this.logout();
    }
  }

  logout() {
    this.accessToken = null;
    this.refreshToken = null;
    if (this.tokenRefreshTimer) {
      clearTimeout(this.tokenRefreshTimer);
    }
    // Clear all local data
    db.delete();
  }
}
```

### 3.2 Transport Security

#### TLS Configuration

```nginx
# NGINX SSL configuration

ssl_protocols TLSv1.3 TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

# HSTS (Force HTTPS)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://api.feelink.com;" always;
```

#### API Security Headers

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# CORS - restrict to production domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.feelink.com"],  # Production only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# Trusted Host
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["app.feelink.com", "api.feelink.com"]
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### 3.3 Database Security

#### Encryption at Rest

```sql
-- PostgreSQL with encryption

-- 1. Enable pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 2. Encrypt sensitive columns (optional, for extra security)
-- Example: Encrypting notes field

ALTER TABLE entries
ADD COLUMN notes_encrypted BYTEA;

-- Encrypt on insert
INSERT INTO entries (user_id, entry_date, notes_encrypted)
VALUES (1, '2025-11-15', pgp_sym_encrypt('Sensitive note text', 'encryption_key'));

-- Decrypt on select
SELECT
    id,
    entry_date,
    pgp_sym_decrypt(notes_encrypted, 'encryption_key') AS notes
FROM entries;
```

**Note**: For MVP, database-level encryption (filesystem encryption) is sufficient. Column-level encryption adds complexity and performance overhead.

#### Access Controls

```sql
-- Database roles with minimal permissions

-- Application role (used by backend)
CREATE ROLE feelink_app WITH LOGIN PASSWORD 'secure_password';

-- Grant only necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO feelink_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO feelink_app;

-- Read-only role (for analytics/reporting)
CREATE ROLE feelink_readonly WITH LOGIN PASSWORD 'readonly_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO feelink_readonly;

-- Deny direct superuser access in production
REVOKE ALL ON DATABASE feelink FROM PUBLIC;
```

#### SQL Injection Prevention

```python
# ALWAYS use parameterized queries

# ❌ BAD - SQL Injection vulnerable
user_id = request.query_params.get("user_id")
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# ✅ GOOD - Parameterized query
user_id = request.query_params.get("user_id")
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

# ✅ BEST - ORM (SQLAlchemy)
user = db.query(User).filter(User.id == user_id).first()
```

### 3.4 Input Validation & Sanitization

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import bleach

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def password_strength(cls, v):
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class EntryCreate(BaseModel):
    entry_date: str = Field(..., regex=r'^\d{4}-\d{2}-\d{2}$')
    notes: Optional[str] = None

    @validator('notes')
    def sanitize_notes(cls, v):
        if v:
            # Remove potentially dangerous HTML/scripts
            return bleach.clean(v, tags=[], strip=True)
        return v

    @validator('entry_date')
    def validate_date_not_future(cls, v):
        from datetime import date
        entry_date = date.fromisoformat(v)
        if entry_date > date.today():
            raise ValueError('Entry date cannot be in the future')
        return v
```

### 3.5 Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply rate limits
@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(request: Request, credentials: LoginRequest):
    # ...

@app.post("/api/v1/entries")
@limiter.limit("60/minute")  # Max 60 entries per minute
async def create_entry(request: Request, entry: EntryCreate):
    # ...

@app.get("/api/v1/analytics/correlations")
@limiter.limit("10/minute")  # Expensive operation
async def get_correlations(request: Request):
    # ...
```

---

## 4. Privacy Features

### 4.1 Data Minimization

**We only collect what's necessary:**

| Data Type | Purpose | Optional? |
|-----------|---------|-----------|
| Email | Authentication, account recovery | Required |
| Password | Authentication | Required |
| Language | UI localization | Optional (default: browser) |
| Timezone | Correct date/time display | Optional (default: browser) |
| Metrics | User-defined tracking | User-controlled |
| Entries | Daily logging | User-controlled |

**We DO NOT collect:**
- Name
- Address
- Phone number
- Payment details (stored by payment processor)
- Device fingerprinting
- Behavioral tracking for ads
- IP addresses (beyond temporary rate limiting)

### 4.2 Data Export (GDPR Right to Portability)

```python
# GET /api/v1/export/all

from datetime import datetime
import json

@app.get("/api/v1/export/all")
async def export_all_data(current_user: User = Depends(get_current_user)):
    """
    Export all user data in JSON format.
    GDPR Article 20: Right to data portability.
    """

    # Fetch all user data
    metrics = await get_user_metrics(current_user.id)
    entries = await get_user_entries(current_user.id)
    settings = await get_user_settings(current_user.id)

    export_data = {
        "export_metadata": {
            "version": "1.0",
            "export_date": datetime.utcnow().isoformat(),
            "user_id": current_user.id
        },
        "personal_information": {
            "email": current_user.email,
            "language": current_user.language,
            "timezone": current_user.timezone,
            "account_created": current_user.created_at.isoformat(),
        },
        "metrics": [metric.dict() for metric in metrics],
        "entries": [entry.dict() for entry in entries],
        "settings": settings.dict() if settings else {}
    }

    # Return as downloadable JSON
    return JSONResponse(
        content=export_data,
        headers={
            "Content-Disposition": f"attachment; filename=feelink_export_{current_user.id}_{datetime.now().strftime('%Y%m%d')}.json"
        }
    )
```

### 4.3 Data Deletion (GDPR Right to Erasure)

```python
# DELETE /api/v1/users/me

@app.delete("/api/v1/users/me")
async def delete_account(
    confirmation: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Permanently delete user account and all associated data.
    GDPR Article 17: Right to erasure.
    """

    # Require explicit confirmation
    if confirmation != "DELETE MY ACCOUNT":
        raise HTTPException(
            status_code=400,
            detail="Please confirm account deletion by providing exact confirmation text"
        )

    # Delete all user data (cascading deletes handle related records)
    # 1. Metrics (cascade to entry_values)
    # 2. Entries (cascade to entry_values)
    # 3. User settings
    # 4. User account

    db.delete(current_user)
    db.commit()

    # Log deletion for compliance
    await audit_log.info(f"User {current_user.id} account deleted")

    return {"message": "Account and all data permanently deleted"}
```

### 4.4 Consent Management

```typescript
// Frontend consent tracking

interface UserConsent {
  essential: boolean;       // Always true (required for app to function)
  analytics: boolean;       // Optional - usage analytics
  communications: boolean;  // Optional - email notifications
  thirdPartySharing: boolean; // Always false (we never share)
}

class ConsentManager {
  async getConsent(): Promise<UserConsent> {
    return {
      essential: true,
      analytics: false,     // Default to privacy-friendly
      communications: false,
      thirdPartySharing: false
    };
  }

  async updateConsent(consent: UserConsent) {
    await api.patch('/api/v1/users/me/consent', consent);
    this.applyConsent(consent);
  }

  private applyConsent(consent: UserConsent) {
    if (!consent.analytics) {
      // Disable analytics
      this.disableAnalytics();
    }

    if (!consent.communications) {
      // Disable email notifications
      this.disableNotifications();
    }
  }
}
```

### 4.5 Privacy Policy

**Required Disclosures:**

```markdown
# FeelInk Privacy Policy

Last Updated: 2025-11-15

## 1. Information We Collect

### Information You Provide:
- Email address (for authentication)
- Password (encrypted, never stored in plain text)
- Mental health tracking data (metrics, entries, notes)
- Preferences (language, timezone)

### Information We Automatically Collect:
- Login timestamps (for security)
- Error logs (for debugging)
- Aggregated usage statistics (if you opt in)

## 2. How We Use Your Information

- **Provide the Service**: Process and store your tracking data
- **Security**: Detect and prevent unauthorized access
- **Improvement**: Analyze aggregate patterns to improve features (opt-in only)
- **Communication**: Send critical service updates (opt-out available)

## 3. How We Protect Your Information

- TLS encryption for all data in transit
- Database encryption at rest
- Access controls and authentication
- Regular security audits
- No third-party data sharing

## 4. Your Rights

Under GDPR, you have the right to:
- ✅ Access your data (export anytime)
- ✅ Correct your data (edit anytime)
- ✅ Delete your data (delete account anytime)
- ✅ Port your data (CSV/JSON export)
- ✅ Withdraw consent (opt-out of analytics)

## 5. Data Retention

- Active accounts: Data retained indefinitely
- Deleted accounts: All data permanently deleted within 30 days
- Backups: Retained for 90 days, then permanently deleted

## 6. Third-Party Services

We use minimal third-party services:
- Cloud hosting (AWS/Azure/GCP)
- Email delivery (for password reset)
- Payment processing (no payment data stored by us)

No data is sold or shared with advertisers.

## 7. Children's Privacy

FeelInk is not intended for users under 16. We do not knowingly collect data from children.

## 8. Changes to This Policy

We will notify users of material changes via email.

## 9. Contact

Privacy questions: privacy@feelink.com
Data requests: dpo@feelink.com
```

---

## 5. Security Best Practices for Development

### 5.1 Environment Variables

```bash
# .env (NEVER commit to git!)

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/feelink

# Authentication
SECRET_KEY=generate-with-openssl-rand-hex-32
JWT_SECRET_KEY=generate-with-openssl-rand-hex-32

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.xxx

# Sentry (Error tracking)
SENTRY_DSN=https://xxx@sentry.io/xxx
```

```python
# Load from environment
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    jwt_secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### 5.2 Dependency Security

```bash
# Python - Check for vulnerable dependencies
pip install safety
safety check

# JavaScript - Check for vulnerable dependencies
npm audit
npm audit fix
```

### 5.3 Code Security Scanning

```yaml
# .github/workflows/security.yml

name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Python security
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r backend/

      # JavaScript security
      - name: Run npm audit
        run: |
          cd frontend
          npm audit

      # Dependency check
      - name: OWASP Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
```

---

## 6. Incident Response Plan

### 6.1 Security Incident Classification

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Data breach, unauthorized access | Immediate (< 1 hour) |
| **High** | Vulnerability actively exploited | 4 hours |
| **Medium** | Vulnerability discovered, not exploited | 24 hours |
| **Low** | Minor security issue | 7 days |

### 6.2 Breach Notification

**GDPR requires breach notification within 72 hours.**

```python
# Incident response template

class SecurityIncident:
    def __init__(self, severity: str, description: str):
        self.severity = severity
        self.description = description
        self.discovered_at = datetime.utcnow()

    async def notify(self):
        # 1. Notify security team
        await send_alert_to_security_team(self)

        # 2. If Critical/High and affects users
        if self.severity in ["Critical", "High"] and self.affects_user_data:
            # Notify affected users
            await notify_affected_users(self)

            # Notify regulatory authorities (GDPR)
            if self.user_count > 100:
                await notify_data_protection_authority(self)

        # 3. Log incident
        await log_incident(self)
```

---

## 7. Compliance Checklist

### ✅ GDPR Compliance

- [ ] Privacy policy published and accessible
- [ ] Cookie consent (if using cookies for non-essential purposes)
- [ ] Data export functionality
- [ ] Data deletion functionality
- [ ] Right to rectification (edit data)
- [ ] Lawful basis for processing documented
- [ ] Data Protection Impact Assessment (DPIA) completed
- [ ] Data Processing Agreement with cloud provider
- [ ] Breach notification procedure in place
- [ ] Data Protection Officer appointed (if required)

### ✅ Security Best Practices

- [ ] HTTPS/TLS encryption
- [ ] Password hashing (bcrypt/argon2)
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (input sanitization)
- [ ] CSRF protection
- [ ] Rate limiting
- [ ] Security headers (CSP, HSTS, etc.)
- [ ] Dependency vulnerability scanning
- [ ] Regular security audits
- [ ] Incident response plan

### ✅ Data Security

- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Access controls
- [ ] Audit logging
- [ ] Secure backups
- [ ] Secure deletion (data is unrecoverable)

---

## 8. Related Documents

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical architecture
- [DATA_MODEL.md](./DATA_MODEL.md) - Data structures
- [REQUIREMENTS.md](./REQUIREMENTS.md) - Security requirements

---

**Status**: Security framework ready for implementation
**Next Steps**: Security audit before production launch
