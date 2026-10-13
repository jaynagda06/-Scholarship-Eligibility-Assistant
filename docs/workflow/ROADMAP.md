# DEVELOPMENT ROADMAP

## 1. Research & Discovery
- [ ] Gather existing scholarship portals (NSP, state portals, private schemes)
- [ ] Interview 5-10 students about scholarship search pain points
- [ ] Map data fields: academic, personal, financial, category
- [ ] Requirement gathering from stakeholders
- [ ] Define MVP scope vs future scope (slide 6)

## 2. Design & Prototyping
- [ ] Create user personas: Student, Parent, Institution, NGO
- [ ] Wireframe: Registration -> Profile -> Search -> Results -> Apply
- [ ] Design system: multilingual labels, region-specific colors
- [ ] Create Figma/Adobe XD prototype for mobile + web
- [ ] Usability test with 3-5 students

## 3. Data Architecture & Schema Design
- [ ] Design Scholarship: id, name, org, category, criteria, deadline, documents, url, status
- [ ] Design Student: id, phone, name, school, degree, year, income, category, disability, preferred_language
- [ ] Design Application tracker: id, student_id, scholarship_id, status
- [ ] Data source strategy: scrape + manual entry + govt API

## 4. Backend Development
- [ ] Set up FastAPI project with Pydantic models
- [ ] Database: SQLite (MVP) -> PostgreSQL (later)
- [ ] Authentication: JWT + phone OTP
- [ ] Scholarship CRUD APIs (admin panel first, then public)
- [ ] Student profile API with NLP processing
- [ ] Simple rule engine: compare profile to scholarship criteria
- [ ] Deadline alert scheduler (Celery + Redis + cron)

## 5. AI/NLP Eligibility Matching
- [ ] Profile parsing: extract structured data from free-text
- [ ] NER for: degree, year, category, income, institution
- [ ] Hard-rules matcher: AND/OR criteria evaluation
- [ ] Soft-rules scorer: fuzzy matching with confidence scores
- [ ] Vector search (optional): semantic similarity
- [ ] Ranking algorithm: score * urgency * relevance

## 6. Frontend Development
- [ ] Web app: React + Vite + Tailwind CSS (mobile-first)
- [ ] Mobile app: React Native or Flutter
- [ ] Voice search: Web Speech API (browser) / OpenAI Realtime
- [ ] Multilingual: i18n (react-i18next) with Hindi, Marathi, Gujarati, English
- [ ] Dashboard: profile, recommendations, document checklist, deadlines
- [ ] Push notifications: Firebase Cloud Messaging

## 7. Integration & Automation
- [ ] Govt portal scraping/APIs for live scheme data
- [ ] Document upload and OCR
- [ ] Automated SMS/WhatsApp reminder service
- [ ] Application status tracking with agencies

## 8. Testing
- [ ] Unit tests: pytest (coverage > 70%)
- [ ] Integration tests: test DB, APIs, search
- [ ] E2E tests: Cypress or Playwright
- [ ] Accessibility tests: screen reader + keyboard nav

## 9. Deployment
- [ ] Dockerize app + DB + worker
- [ ] CI/CD: GitHub Actions
- [ ] Cloud: AWS (RDS + Lambda + S3) or Azure
- [ ] Domain + SSL + analytics

## 10. Iteration
- [ ] Soft launch with 1 college
- [ ] Collect feedback, fix bugs, add missing languages
- [ ] Scale to district/state level
- [ ] Government partnership for live data
