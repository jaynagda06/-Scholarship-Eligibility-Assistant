# ARCHITECTURE

## Backend

### APIs
- `POST /auth/register` - student registration with OTP
- `GET /scholarships` - paginated list
- `POST /scholarships` - admin: add/update scholarship
- `POST /students` - registration
- `GET /students` - list students
- `POST /students/{id}/eligibility` - check matching scholarships
- `GET /alerts/upcoming` - deadlines within N days
- `POST /notifications/send` - trigger SMS/WhatsApp

### DB Schema
```
scholarships(id, name, org, category, criteria, deadline, documents, url, status)
students(id, phone, name, school, degree, year, income, category, disability, language, created_at)
student_scholarships(id, student_id, scholarship_id, status, matched_at)
```

### Rule Engine
- Hard rules: AND of exact/range matches (degree, year, category, income ceiling)
- Soft rules: regex / keyword / fuzzy match on name, description
- Confidence score = weighted sum
- Timeout: 5 sec per request

## Frontend

### Web App
- Pages: Home / Search / Profile / Dashboard / Results / Apply
- Tech: React 19 + Vite + Tailwind CSS + shadcn/ui
- i18n: react-i18next (English, Hindi, Gujarati, Marathi)
- Voice: Web Speech API (recognition) + SSML (synthesis)

### Mobile
- Native-ish: React Native or Flutter
- Offline: cached scholarships, push notifications

## AI/NLP

### Pipeline
1. Input: spoken / typed profile (regional language)
2. NLP: extract entities (degree, year, institution, category, income)
3. Normalise: standardise categories per govt classification
4. Match: hard-rule evaluator + vector similarity
5. Rank: score + deadline urgency + scholarship reputation

### Regional NLP
- spaCy + IndicNLP for Hindi/Marathi/Gujarati
- Google Gemini Multilingual for fallback
- Whisper for voice-to-text transcription

## Deployment

### Docker Compose
```yaml
services:
  app: image built from ./src/backend
  db: postgres:16-16-alpine
  redis: redis:7-alpine
  minio: minio/minio
  worker: celery worker
volumes:
  pgdata, redata, mdata
```

### CI/CD (GitHub Actions)
1. On push: lint + type-check + unit tests
2. On tag: build Docker images, push to ECR/GCR
3. On main: deploy staging, run integration tests
4. After merge: deploy prod + blue/green

## Testing Strategy
- Backend: pytest (70% coverage target)
- Frontend: Vitest + Vitest React, Playwright
- AI: property-based tests, compare against hand-labelled test set
- E2E: real profile -> speech -> matched scholarships -> validate

## Key Risks
| Risk | Mitigation |
|------|------------|
| Regional NLP quality | Start with English + Hindi, add Gujarati/Marathi later |
| Govt data accuracy | Manual curation first; API integration later |
| AI hallucination | Confidence threshold + human-in-the-loop |
| User adoption | Partner with one college; soft launch |
| Voice latency | Cache common queries; fallback to text |
| API cost | Use local llama.cpp or Google Gemini for free tier |

## Next Immediate Actions
1. Set up project repo with README, license, .gitignore
2. Create database schema (init migration)
3. Create student profile + scholarship CRUD API skeleton
4. Add FastAPI + SQLAlchemy
5. Add simple rule engine (hard rules only, no AI yet)
6. Build basic React web app with profile + scholarship list
7. Add Web Speech API voice search
8. Set up Docker + docker-compose for local dev
