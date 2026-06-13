# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational Python project for a World Cup 2026 pool (bolão). Users register and predict the top two teams in each group; the 8 best third-place qualifiers are assigned randomly.

## Tech Stack

- **Frontend/UI**: Streamlit (deployed on Streamlit Cloud)
- **Language**: Python 3.12
- **Database**: Supabase (project ref `cuoxkjhuszigxgqmndpn`)

## Design Reference

See [picture/Print - Simulador Copa do Mundo.png](picture/Print%20-%20Simulador%20Copa%20do%20Mundo.png) for the UI layout reference — a group-stage simulator showing all 12 groups with team standings columns.

## Business Rules

- Participants register with **name**, **phone**, and **email**.
- Each participant selects the **1st and 2nd place** finishers for each of the 12 groups (A–L).
- The **8 best 3rd-place teams** are assigned randomly (to simplify bracket logic).
- From the round of 16 onward, bracket progression follows standard FIFA World Cup 2026 rules.

## Project Structure

```
app.py                          # Streamlit entry point (3 steps: register → predict → confirm)
db.py                           # Supabase client and DB operations (reads from st.secrets)
copa_data.py                    # 12 groups with 4 teams each (update if FIFA changes groups)
migrations/001_schema.sql       # Creates tables + RLS policies — run once in Supabase SQL Editor
.streamlit/secrets.toml         # Local dev secrets (gitignored)
.streamlit/secrets.toml.example # Template for secrets
```

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## Secrets

Secrets are managed via `st.secrets` — **never via `.env`** in production.

**Local development** — fill in `.streamlit/secrets.toml` (already gitignored):
```toml
SUPABASE_URL      = "https://cuoxkjhuszigxgqmndpn.supabase.co"
SUPABASE_ANON_KEY = "<anon-public-key>"
```

**Streamlit Cloud** — add the same keys in:
App dashboard → **Settings → Secrets** (TOML format)

The anon key is found at: Supabase Dashboard → Settings → API → **anon public**.

## Database setup

Run `migrations/001_schema.sql` in the Supabase SQL Editor before the first deploy.
Creates tables `participantes` and `palpites` with RLS policies allowing anonymous inserts.

## Deploy to Streamlit Cloud

1. Push the repo to GitHub (`.env` and `.streamlit/secrets.toml` are gitignored — safe to push)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select the repo, branch `main`, main file `app.py`
4. Under **Advanced settings → Secrets**, paste the TOML secrets block
5. Click **Deploy**
