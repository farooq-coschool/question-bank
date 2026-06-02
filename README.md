# Question Bank Generator

Web app for generating ICSE/CBSE question banks (Objective, Subjective, RTC, RAD, MTF, Glossary, LO, PLT) for Biology, Physics, Chemistry, Mathematics, English, Civics, Geography, History, and Commerce.

- **Frontend:** single-file `question_bank_generator_4.html`
- **Backend:** `server.py` — proxy that injects Anthropic API keys server-side based on subject
- **Hosting:** Render (auto-deploys on push to `main`)

## Local development

```bash
python server.py
# open http://localhost:8000/question_bank_generator_4.html
```

## Environment variables

Set one Anthropic key per subject in your hosting platform's environment:

```
BIOLOGY_KEY=sk-ant-...
PHYSICS_KEY=sk-ant-...
CHEMISTRY_KEY=sk-ant-...
MATHEMATICS_KEY=sk-ant-...
ENGLISH_KEY=sk-ant-...
COMMERCE_KEY=sk-ant-...
SOCIAL_KEY=sk-ant-...     # used as fallback for Social / Civics / Geography / History
```

Keys never reach the browser — the proxy reads `x-subject` from each request and attaches the matching `x-api-key` server-side.

## Deploy

`git push origin main` → Render auto-deploys at https://question-bank-9bwr.onrender.com.
