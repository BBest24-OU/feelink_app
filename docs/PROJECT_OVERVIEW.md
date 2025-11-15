# FeelInk - Mood & Mental Health Tracking Application

## 🎯 Project Vision

FeelInk is a Progressive Web Application (PWA) designed to empower individuals in tracking and understanding their mental health, mood, and overall well-being. The application enables users to discover meaningful correlations between external factors and their mental state through simple daily tracking and advanced statistical analysis.

## 🌟 Core Philosophy

**Simple in Use, Sophisticated in Results**

- **1-Minute Daily Commitment**: Quick, effortless data entry that takes less than a minute per day
- **Personalized Tracking**: Users define what matters to them, not a rigid template
- **Actionable Insights**: After just one week, discover patterns and correlations invisible to the naked eye
- **Clinical Value**: Generate comprehensive reports for healthcare professionals, maximizing therapeutic session efficiency

## 🎭 The Problem We Solve

### For Patients:
- **Time-consuming consultations**: 10-15 minutes spent describing "how things are" instead of solving problems
- **Forgotten details**: Hard to remember mood patterns from weeks ago
- **Hidden patterns**: Difficulty connecting external triggers with mental state changes
- **Expensive sessions**: Wasted time means wasted money in private healthcare

### For Healthcare Providers:
- **Incomplete information**: Relying on patient memory and subjective recall
- **Limited session time**: Spending valuable time on data gathering instead of treatment
- **Lack of objective data**: Difficulty spotting patterns across multiple sessions

## 💡 Our Solution

FeelInk transforms mental health tracking from a chore into a powerful diagnostic tool:

1. **Flexible Metric System**: Track anything that matters - physical symptoms, psychological states, triggers, medications, self-care activities, wellness practices
2. **Smart Correlation Engine**: Automatically discover relationships (e.g., "alcohol consumption → mood decrease after 3 days")
3. **Professional Reports**: One-page summaries with correlations, cross-correlations, and lag effects
4. **Data Ownership**: Full export capabilities (PDF, CSV, JSON) - your data belongs to you

## 🎯 Key Differentiators

1. **No Vendor Lock-in**: Complete data export functionality - we're proud of it
2. **Offline-First**: Works without internet, syncs when available
3. **Privacy-Focused**: User owns their data completely
4. **Mobile-First**: Optimized for quick daily mobile use
5. **Clinically Useful**: Generates reports that healthcare professionals actually want to see

## 👥 Target Users

### Primary Users:
- Individuals tracking mental health for therapy/psychiatry
- People with mood disorders (depression, bipolar, anxiety)
- Chronic illness patients tracking symptom correlations
- Anyone interested in quantified self and wellness optimization

### Secondary Users:
- Therapists and psychologists
- Psychiatrists
- General practitioners
- Mental health coaches

## 📊 Metric Categories

Users can create custom metrics within these categories:

| Category | Examples |
|----------|----------|
| **Physical Symptoms** | Pain level, fatigue, headaches, muscle tension |
| **Psychological Symptoms** | Mood, anxiety, irritability, focus, energy |
| **Triggers** | Stressful events, conflicts, deadlines, social situations |
| **Medications** | Dosage tracking, side effects, effectiveness |
| **Self-Care** | Meditation, journaling, therapy sessions, breaks |
| **Wellness** | Exercise, sleep hours/quality, diet, social connection |
| **Notes** | Free-form observations |

## 📱 Metric Value Types

Each metric can use different data types:
- **Range (min-max)**: e.g., Mood 1-10, Pain 0-100
- **Number**: e.g., Hours slept, glasses of water
- **Boolean (yes/no)**: e.g., Took medication, exercised today
- **Count**: e.g., Panic attacks, social interactions
- **Free text note**: Optional for any entry

## 🔍 Analysis Examples

After consistent tracking, FeelInk might reveal:

- "Sleep < 6 hours correlates with irritability increase (r=0.73, p<0.01) the next day"
- "Working >8 hours/day leads to sleep problems (lag 0 days), which causes irritability (lag 1 day)"
- "Alcohol consumption correlates with mood decrease 3 days later (lag correlation)"
- "Meditation practice correlates with reduced anxiety (cumulative effect over 7 days)"

## 🏗️ Technical Stack Overview

### Frontend:
- **Framework**: Modern JavaScript framework (React/Vue/Svelte)
- **PWA**: Service Workers, offline capability, installable
- **UI**: Mobile-first, responsive design
- **Styling**: Light, clean, professional aesthetic
- **Charts**: Advanced visualization libraries

### Backend:
- **Framework**: Lightweight Python (Flask/FastAPI)
- **Database**: Cloud-based with local caching
- **API**: RESTful design
- **Analytics**: Statistical correlation engine

## 🌍 Internationalization

- **Initial languages**: Polish and English
- **Architecture**: Externalized strings from day one
- **Scalable**: Ready for additional languages

## 🎨 Design Principles

1. **Clarity over complexity**: Clean, uncluttered interface
2. **Speed**: Fast load times, instant interactions
3. **Accessibility**: WCAG compliant
4. **Consistency**: Centralized theme management (colors, typography, spacing)
5. **Professional aesthetics**: Trust-building visual design

## 📈 Success Metrics

- **User engagement**: Daily completion rate >70%
- **Time to complete**: <1 minute average
- **Clinical adoption**: Therapists requesting patient reports
- **Data insights**: Users discovering at least 3 meaningful correlations within 30 days
- **Export usage**: High CSV/JSON export rates (proving data ownership)

## 🚀 Development Phases

### Phase 1: Foundation (MVP)
- Metric creation and categorization
- Daily logging interface
- Local data storage
- Basic visualizations

### Phase 2: Analytics
- Correlation engine
- Advanced visualizations
- Report generation (PDF)

### Phase 3: Cloud & Collaboration
- Cloud synchronization
- Multi-device support
- Data export (CSV/JSON)

### Phase 4: Enhancement
- Advanced analytics (lag correlations, cross-correlations)
- AI-powered insights suggestions
- Integration with wearables

## 🔒 Privacy & Security

- **Data ownership**: User has complete control
- **Export freedom**: Full data portability
- **Transparent privacy**: Clear privacy policy
- **Secure storage**: Encryption at rest and in transit
- **Optional sharing**: User controls who sees their data

## 💪 Competitive Advantages

1. **Flexibility**: Not prescriptive - user defines what to track
2. **Clinical utility**: Built for real healthcare use cases
3. **Speed**: Respects user's time (1-minute commitment)
4. **Sophistication**: Advanced correlation analysis, not just graphs
5. **Freedom**: True data ownership and portability

---

## 📝 Document Status

**Version**: 0.1.0
**Last Updated**: 2025-11-15
**Status**: Initial Draft
**Next Review**: After requirements finalization

## 🔗 Related Documents

- [REQUIREMENTS.md](./REQUIREMENTS.md) - Detailed functional requirements
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical architecture
- [UI_UX_GUIDELINES.md](./UI_UX_GUIDELINES.md) - Design system
- [DATA_MODEL.md](./DATA_MODEL.md) - Data structures
- [CORRELATION_ALGORITHMS.md](./CORRELATION_ALGORITHMS.md) - Statistical methods
- [PRIVACY_AND_SECURITY.md](./PRIVACY_AND_SECURITY.md) - Privacy approach
- [CLAUDE.md](./CLAUDE.md) - Development team structure
