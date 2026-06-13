# ⚽ World Cup 2026 Pool

Web app for managing FIFA World Cup 2026 predictions. Built in Python with Streamlit and Supabase.

## How It Works

The participant goes through 7 steps to complete the full prediction:

| Step | Stage |
|---|---|
| 1 | Registration (name, phone, email) |
| 2 | Group Stage - choose 1st and 2nd place from each of the 12 groups (A-L) |
| 3 | Round of 32 - 16 matchups generated from the official FIFA bracket |
| 4 | Round of 16 - 8 matchups |
| 5 | Quarterfinals - 4 matchups |
| 6 | Semifinals - 2 matchups |
| 7 | Third-place Playoff + Grand Final |

The **8 best third-place teams** are drawn automatically from the teams that were not chosen as 1st or 2nd in each group, following the simplification defined in the pool rules.

The knockout bracket follows the official FIFA 2026 structure, with matchups generated automatically from the participant's predictions.

## Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **Database**: [Supabase](https://supabase.com) (PostgreSQL)
- **Language**: Python 3.12

## Database Structure

| Table | Contents |
|---|---|
| `participantes` | Registration data |
| `palpites` | 1st and 2nd place by group (12 rows per participant) |
| `terceiros` | 8 teams drawn as the best third-place finishers |
| `fases_palpites` | Predictions for each knockout stage (R32 -> Final) |

## Running Locally

**1. Clone the repository**
```bash
git clone https://github.com/mauroroc/BolaoCopa26.git
cd BolaoCopa26
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure secrets**

Copy the template and fill it with your Supabase credentials:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

```toml
# .streamlit/secrets.toml
SUPABASE_URL      = "https://<project-ref>.supabase.co"
SUPABASE_ANON_KEY = "<anon-public-key>"
```

The `SUPABASE_ANON_KEY` is available in: **Supabase Dashboard -> Settings -> API -> anon public**.

**4. Create the tables in Supabase**

Run the files in `migrations/` in order in the Supabase **SQL Editor**:
```
migrations/001_schema.sql
migrations/002_grant_anon.sql
migrations/003_fases_palpites.sql
```

**5. Run the app**
```bash
streamlit run app.py
```

## Deploying to Streamlit Cloud

1. Fork or use this repository on [Streamlit Cloud](https://share.streamlit.io)
2. Configure the secrets under **Settings -> Secrets**:
```toml
SUPABASE_URL      = "https://<project-ref>.supabase.co"
SUPABASE_ANON_KEY = "<anon-public-key>"
```
3. Set the main file to `app.py` and click **Deploy**

## Groups - World Cup 2026

Draw held on December 5, 2025, at the Kennedy Center, Washington D.C.

| Group | Teams |
|---|---|
| A | Mexico, South Africa, South Korea, Czech Republic |
| B | Canada, Bosnia and Herzegovina, Qatar, Switzerland |
| C | Brazil, Morocco, Haiti, Scotland |
| D | United States, Paraguay, Australia, Turkey |
| E | Germany, Curaçao, Ivory Coast, Ecuador |
| F | Netherlands, Japan, Sweden, Tunisia |
| G | Belgium, Egypt, Iran, New Zealand |
| H | Spain, Cape Verde, Saudi Arabia, Uruguay |
| I | France, Senegal, Iraq, Norway |
| J | Argentina, Algeria, Austria, Jordan |
| K | Portugal, DR Congo, Uzbekistan, Colombia |
| L | England, Croatia, Ghana, Panama |
