# Media Storage App

A small FastAPI app for managing media categories and uploads, now with simple environment-based authentication.

## Environment variables

Place a `.env` file next to `main.py` (same folder) or set real OS environment variables. See `.env.example` for a template.

Required keys:

- `SESSION_SECRET`: Secret key to sign session cookies. Use a long random string in production.
- `AUTH_USERNAME`: Fixed username allowed to log in (e.g., `admin`).
- `AUTH_PASSWORD`: Fixed password allowed to log in.

## Login & Logout

- Visit `/login` to sign in. After login, you are redirected to the home page.
- Click the Logout button in the header or visit `/logout` to end the session.
- All main routes (`/`, `/upload`, `/create-category/`, `/get_images/{folder}`) require authentication.

## Run locally

Install dependencies and run with Uvicorn (adjust paths as needed):

```cmd
pip install fastapi uvicorn jinja2
uvicorn main:app --reload --port 8000
```

Then open http://localhost:8000 in your browser.

## Notes on "Enable Claude Sonnet 4.5 for all clients"

This repository does not include a model routing layer or feature flags for external LLMs. If you need to enable a specific model (e.g., "Claude Sonnet 4.5") for your clients, please share where that configuration lives (separate service, gateway, or env flags) and we can integrate a toggle or environment-controlled setting here.
