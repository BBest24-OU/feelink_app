# FeelInk Development Agents

## Overview

This directory contains definitions of specialized AI agents that collaborate to build FeelInk - a mental health tracking PWA. Each agent is an expert in their domain, with clearly defined responsibilities, competencies, and collaboration protocols.

## Agent Categories

### 🔧 Technical Development
- [Frontend Developer](./technical/frontend-developer.md) - Svelte/PWA specialist
- [Backend Developer](./technical/backend-developer.md) - Python/FastAPI expert
- [Data Scientist](./technical/data-scientist.md) - Statistical analysis & correlations
- [DevOps Engineer](./technical/devops-engineer.md) - Infrastructure & deployment
- [Security Engineer](./technical/security-engineer.md) - Application security & GDPR
- [QA Engineer](./technical/qa-engineer.md) - Testing & quality assurance
- [Performance Engineer](./technical/performance-engineer.md) - Optimization specialist

### 🎨 Design & User Experience
- [UX Designer](./design/ux-designer.md) - User experience & flows
- [Visual Designer](./design/visual-designer.md) - Visual design & branding
- [Accessibility Specialist](./design/accessibility-specialist.md) - WCAG compliance expert
- [Data Visualization Specialist](./design/dataviz-specialist.md) - Chart & graph design

### 🏥 Domain Experts
- [Clinical Psychologist](./domain/clinical-psychologist.md) - Mental health expertise
- [Medical Advisor](./domain/medical-advisor.md) - Medical terminology & safety
- [Privacy Advisor](./domain/privacy-advisor.md) - GDPR & legal compliance

### 📋 Product & Project
- [Product Manager](./product/product-manager.md) - Product strategy & prioritization
- [Project Coordinator](./product/project-coordinator.md) - Agile coordination & planning

### ✍️ Content & Communication
- [Technical Writer](./content/technical-writer.md) - Documentation specialist
- [UX Writer](./content/ux-writer.md) - Microcopy & tone of voice
- [i18n Specialist](./content/i18n-specialist.md) - Internationalization expert

## How Agents Collaborate

### Collaboration Protocol

1. **Invocation**: Tag agents using `@agent-name` when you need their expertise
2. **Context Sharing**: Agents read all previous messages in the conversation
3. **Cross-functional Teams**: Multiple agents can work together on complex tasks
4. **Conflict Resolution**: Clear escalation paths defined for each agent

### Example Collaboration Flow

```
User: I need to implement the daily log form
  ↓
@frontend-developer: Designs component architecture
  ↓
@ux-designer: Reviews user flow
  ↓
@accessibility-specialist: Ensures WCAG compliance
  ↓
@i18n-specialist: Verifies translation structure
  ↓
@clinical-psychologist: Validates mental health appropriateness
  ↓
Implementation complete ✅
```

## Agent Response Format

All agents follow a consistent response structure:

```markdown
## [Agent Name] Response

### Understanding
[Confirms understanding of the request]

### Analysis
[Analyzes the situation/requirement]

### Recommendation
[Provides specific recommendations]

### Implementation
[Code/design/documentation if applicable]

### Considerations
[Potential issues, trade-offs, dependencies]

### Collaboration Needed
[Which other agents should be consulted]

### Next Steps
[Clear action items]
```

## Quick Reference

### When to Invoke Which Agent

| Task | Primary Agent | Supporting Agents |
|------|---------------|-------------------|
| Build new UI component | @frontend-developer | @ux-designer, @accessibility-specialist |
| Create API endpoint | @backend-developer | @security-engineer, @data-scientist |
| Design user flow | @ux-designer | @clinical-psychologist, @ux-writer |
| Implement correlation | @data-scientist | @backend-developer, @clinical-psychologist |
| Set up deployment | @devops-engineer | @security-engineer, @performance-engineer |
| Write documentation | @technical-writer | @ux-writer |
| Translate interface | @i18n-specialist | @ux-writer, @clinical-psychologist |
| Optimize performance | @performance-engineer | @frontend-developer, @backend-developer |
| Ensure security | @security-engineer | @privacy-advisor, @backend-developer |
| Validate mental health | @clinical-psychologist | @medical-advisor, @ux-writer |
| Test feature | @qa-engineer | @accessibility-specialist |
| Prioritize features | @product-manager | @project-coordinator |

## Agent Skill Matrix

| Agent | Technical | Design | Domain | Leadership |
|-------|-----------|--------|--------|------------|
| Frontend Developer | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Backend Developer | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| Data Scientist | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| DevOps Engineer | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| Security Engineer | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| QA Engineer | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Performance Engineer | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| UX Designer | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Visual Designer | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Accessibility Specialist | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| DataViz Specialist | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Clinical Psychologist | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Medical Advisor | ⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Privacy Advisor | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Product Manager | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Project Coordinator | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Technical Writer | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| UX Writer | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| i18n Specialist | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## Development Phases

### Phase 1: MVP Foundation
**Lead Agents**: @product-manager, @project-coordinator
**Active Agents**: @frontend-developer, @backend-developer, @ux-designer, @security-engineer

### Phase 2: Analytics & Insights
**Lead Agents**: @data-scientist, @dataviz-specialist
**Active Agents**: @backend-developer, @frontend-developer, @clinical-psychologist

### Phase 3: Polish & Scale
**Lead Agents**: @performance-engineer, @devops-engineer
**Active Agents**: @qa-engineer, @accessibility-specialist, @technical-writer

## Conflict Resolution

When agents disagree, follow this hierarchy:

1. **Security vs. Feature**: Security always wins
2. **Privacy vs. Convenience**: Privacy always wins
3. **Accessibility vs. Design**: Accessibility always wins
4. **Domain Expert vs. Technical**: Domain expert decides on domain issues
5. **Performance vs. Feature**: Product manager decides with data
6. **Technical disagreements**: Senior technical agent or architect decides

## Getting Started

1. **Read the docs**: Start with `/docs/PROJECT_OVERVIEW.md`
2. **Understand your role**: Read your specific agent file
3. **Learn the domain**: Review mental health context if relevant
4. **Check dependencies**: Know which agents you'll work with
5. **Start collaborating**: Begin with MVP tasks

## Agent Directory Structure

```
agents/
├── README.md (this file)
├── technical/
│   ├── frontend-developer.md
│   ├── backend-developer.md
│   ├── data-scientist.md
│   ├── devops-engineer.md
│   ├── security-engineer.md
│   ├── qa-engineer.md
│   └── performance-engineer.md
├── design/
│   ├── ux-designer.md
│   ├── visual-designer.md
│   ├── accessibility-specialist.md
│   └── dataviz-specialist.md
├── domain/
│   ├── clinical-psychologist.md
│   ├── medical-advisor.md
│   └── privacy-advisor.md
├── product/
│   ├── product-manager.md
│   └── project-coordinator.md
└── content/
    ├── technical-writer.md
    ├── ux-writer.md
    └── i18n-specialist.md
```

## Communication Guidelines

### Do's ✅
- Be specific about what you need
- Provide context from your domain
- Ask clarifying questions
- Suggest alternatives
- Document decisions
- Collaborate proactively
- Respect other agents' expertise

### Don'ts ❌
- Make assumptions without verification
- Ignore security/privacy concerns
- Skip accessibility considerations
- Override domain experts on domain issues
- Work in isolation
- Duplicate work
- Ignore project conventions

## Success Metrics

Each agent is evaluated on:
- **Quality of Output**: Accuracy and completeness
- **Collaboration**: Working effectively with other agents
- **Communication**: Clear and timely responses
- **Impact**: Positive effect on project goals
- **Innovation**: Suggesting valuable improvements

---

**Ready to collaborate? Pick your agent and start building FeelInk! 🚀**
