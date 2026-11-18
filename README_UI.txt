Scholarship Eligibility Assistant - UI notes
============================================

Local URL: http://localhost:5173 (after `npm run dev` in src/frontend)
Backend:   http://localhost:3000 (API mounted under /api)

Design
------
Light, minimal dashboard theme:
- Background #f8fafc with a soft indigo radial glow
- White cards, 1px subtle borders, soft shadows
- Plus Jakarta Sans / Inter typography
- Blue (#2563eb) primary action colour
- Interactive custom cursor on desktop (disabled on touch and when
  prefers-reduced-motion is set)

Layout
------
- Header with live status indicator and refresh action
- Overview hero with the scholarship count
- Stats grid (students / scholarships / recommendations)
- Forms grid: register student, add scholarship
- Results grid: eligibility check, ranked recommendations
- Footer

Files
-----
src/frontend/index.html   The whole UI in one file (React UMD + Babel via CDN)
src/frontend/vite.config.js  Dev server + /api proxy to the backend

Deployment
----------
See README.md for Vercel deployment steps.

GitHub: https://github.com/jaynagda06/-Scholarship-Eligibility-Assistant
