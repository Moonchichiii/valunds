# Valunds

A Nordic competence platform connecting talent and employers across Sweden, Denmark, Norway, Finland, and Iceland — built on transparency, trust, and technology.

📋 Table of Contents

About

Features

Technology Stack

Installation & Quick Start

Project Structure

Backend Architecture

Frontend Overview

AI & Matching System

Security & Compliance

Testing & Quality

Development Guidelines

Environment Configuration

📝 About

Valunds is a next-generation Nordic job and competence platform that combines verified data, AI-assisted matching, and privacy-first design.
It empowers employers to find skilled candidates and job seekers to present verified competencies — all within a GDPR-first, AI-moderated, and Nordic-focused environment.

✨ Features
🧭 Nordic Competence Network

Focused exclusively on Sweden, Denmark, Norway, Finland, and Iceland

Verified employers and candidates

Support for multiple Nordic languages

🤝 AI-Powered Matching

Contextual job–candidate recommendations using custom AI models

Weighted skill, location, and cultural-fit metrics

Continuous improvement through anonymized feedback

📑 GDPR-First Design

Full data portability and deletion control

Explicit user consent for analytics, storage, and AI usage

Secure and transparent data lifecycle policies

💼 Employer Tools

Job creation, management, and scheduling

AI-assessed candidate recommendations

Digital contract signing (integrated signing API)

👤 Candidate Tools

CV builder with skill weighting

AI-guided profile recommendations

In-platform job application and status tracking

⚙️ Integrated Scheduling & Communication

Zoom / Teams integration for interviews

Built-in meeting calendar with iCal / ICS support

🛠 Technology Stack
🧩 Backend

Framework: Django 5.2 + Django REST Framework

Auth: django-allauth + dj-rest-auth + SimpleJWT

Database: PostgreSQL (prod) / SQLite (dev)

Task Queue: Celery + Redis

Cache: Django-Redis

Storage: Cloudinary + WhiteNoise

Email: Configurable SMTP (secure, privacy-respecting setup)

Documentation: drf-spectacular (OpenAPI)

Security: django-csp + django-axes + django-ratelimit

⚡ Frontend

Framework: React 19 + TypeScript 5.8

Build: Vite 6.x + pnpm

Styling: Tailwind CSS 4.1

Testing: Playwright + Vitest

Data Layer: TanStack Query v5

Integration: HTMX for progressive enhancement

🧰 DevOps

Dockerized local + production environments

CI/CD: GitHub Actions + Trivy + Docker Scout

VS Code Dev Containers for standardized setup

🚀 Installation & Quick Start

```bash
# Clone repository
git clone <https://github.com/your-username/valunds.git>
cd valunds

# --- Backend ---
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Environment
setx DJANGO_ENV "dev"
python manage.py migrate
python manage.py runserver

# --- Frontend ---
cd ../frontend
pnpm install
pnpm dev
```

📁 Project Structure

```
valunds/
├── backend/
│   ├── config/                 # Django settings & root URLs
│   ├── apps/                   # Modular Django apps
│   │   ├── accounts/           # Custom user model & auth logic
│   │   ├── jobs/               # Job postings & management
│   │   ├── applications/       # Candidate applications
│   │   ├── matching/           # AI matching engine
│   │   ├── contracts/          # Digital contract signing
│   │   ├── payments/           # Payment integration
│   │   ├── ratings/            # Review & trust system
│   │   ├── moderation/         # AI & admin moderation
│   │   ├── scheduling/         # Interview scheduling
│   │   ├── search/             # Advanced filtering & indexing
│   │   ├── api/                # API v1 router
│   │   └── core/               # Shared utilities & base models
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── assets/
│   └── vite.config.ts
├── .env.dev
├── .env.prod
└── README.md
```

## Backend Architecture

Apps organized by domain (apps/accounts, apps/jobs, etc.)

Strict environment separation: .env.dev, .env.prod

Automatic env loader in settings.py

API versioning → /api/v1/

JWT Authentication

Extensible model layer for AI integration

## Environment Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| DJANGO_ENV | Environment selector | dev / prod |
| DJANGO_SECRET_KEY | Django secret key | your-secure-key |
| DATABASE_URL | Database connection string | postgres://user:pass@localhost:5432/db |
| CLOUDINARY_URL | Media storage | cloudinary://... |
| CORS_ALLOWED_ORIGINS | Allowed origins | <http://localhost:5173> |

## Testing & Quality

pytest + pytest-django for backend

Factory Boy + Faker for model tests

Coverage.py for metrics

Playwright for full E2E frontend flows

Pre-commit hooks: Ruff (lint + format + imports)

## AI & Matching System

Valunds integrates a custom AI matching engine (planned phase 2) that:

Analyzes candidate profiles and job postings semantically

Weighs skill relevance, region, and experience

Continuously learns from user ratings and feedback loops

## Security & Compliance

✅ GDPR and ePrivacy compliant

🔐 CSP headers and rate-limiting via middleware

🛡️ Auto-blocking brute force via django-axes

🧾 Consent versioning and AI moderation planned

## Development Guidelines

Python: 3.12 +

Frontend: Vite + React + TypeScript + Tailwind

Code Quality: Ruff only (lint + format + type checks)

Containers: Docker (dev + prod variants)

Branches: feature/, fix/, chore/, docs/

Commits: Conventional Commits enforced
