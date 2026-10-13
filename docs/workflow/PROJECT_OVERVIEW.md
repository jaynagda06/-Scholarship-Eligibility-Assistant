PROJECT OVERVIEW

Scholarship Eligibility Assistant
=================================
A Design-Thinking-inspired platform that centralises scholarship information,
uses AI/NLP for eligibility matching, and provides multilingual voice + text
support with deadline alerts.

Inspiration: Scholarship_Eligibility_Assistant_-_Design_Thinking_Style_-_6_Slides.pptx

=== WHAT THIS PORTAL DOES ===
- Centralised scholarship database (rules, deadlines, documents)
- AI/NLP eligibility engine matching student profiles to scholarships
- Multilingual support (voice + text, regional languages)
- Personalised recommendations with document checklists
- Deadline alerts and reminders
- Future: gov portal integration, automated application assistance

=== KEY CONCEPTS FROM THE PPT ===
1. Problem: fragmented info, manual eligibility, missed deadlines, no personalisation, language barrier
2. Objectives: centralised info, AI matching, personalised recs, multilingual voice+text, deadline guidance
3. Architecture: Student input -> NLP -> AI engine -> Central DB -> Recommendations + checklist + alerts
4. Outcomes: rapid discovery, improved eligibility, better preparedness, equitable access, fewer missed deadlines
5. Stakeholders: Students, Parents, Institutions, Government, NGOs

=== TARGET STACK ===
- Backend: Python (FastAPI) + SQLite (MVP)
- AI/NLP: spaCy / OpenAI API / Google Gemini
- Frontend: React (web) + React Native / Flutter (mobile)
- Voice: Web Speech API / OpenAI Realtime Voice
- Deployment: Docker + AWS / Azure / GCP
- Search: Elasticsearch (optional, later)
