# Mastermind Game

## Description
Implementation of the classic **Mastermind** game as part of the **LinkedIn REACH** backend challenge.

A player tries to guess a secret **4-digit code** (digits **0–7**, duplicates allowed). After each guess, the game provides feedback on:

- **Exact matches** — correct digit in the correct position  
- **Number-only matches** — correct digit in the wrong position (no double counting)

The player has **10 attempts** to guess the secret code.  
Session state (secret code, history, attempts, game status) is stored **server-side**.

---

## Development & Challenge Planning

Before writing code, I outlined the approach and intentionally split the work into phases:

- **Phase-1 (`phase-1` branch)** — A clear, minimal solution that meets all baseline requirements. It’s spec-accurate, easy to run, and easy to review.
- **Phase-2 (`main` branch)** — Backend-focused upgrades: a **server-enforced timer with difficulty-based time limits**, **non-persistent scoring** (`score = guesses_left`), explicit **game status** tracking, **flash/feedback messages** with a supportive tone, a **database + models** layer (including a basic `User` with `password_hash` for future auth), and a **pytest** suite. **The UI remains intentionally minimal to emphasize server-side architecture.**
- **Future (Phase-3+)** — Selective enhancements that add value without scope creep (e.g., **multiplayer support**, **hints system**, **leaderboard**, **auth & user management**, small rewards/competitive feedback).

This phased approach mirrors how I deliver under tight deadlines:
1. **Ship the spec-accurate baseline first** to de-risk requirements and provide a complete, verifiable solution.  
2. **Layer strategic improvements next** to demonstrate backend depth and disciplined complexity management.

**Repository navigation is straightforward: one branch per milestone, each with comprehensive documentation.**

---

## Implementation Plan

### Phase-1 — Baseline (completed)
Meets the minimum challenge requirements:

- Generate 4-digit secret code (Random.org with secure Python `secrets` fallback).  
- Allow digits **0–7** (duplicates allowed per implementation spec).  
- Track guess history and display feedback after each attempt.  
- Show number of guesses remaining.  
- Lock input once the game is **won** or after **10 attempts**.  
- **New Game** available at any time.  
- Implemented with **Flask** + **Jinja2** (server-rendered UI).

**Milestone links**
- **Phase-1 baseline code** — `branch: phase-1`  
  https://github.com/Obersan6/Mastermind-game/tree/phase-1
- **Video Demo – Phase-1** — *(link if available)*
- **Steps — Thought Process & Planning (Phase-1)**  
  **https://github.com/Obersan6/Mastermind-game/blob/phase-1/docs/steps-thoughtprocess.md**

---
# Mastermind Game – Phase 2 (Upgraded Version)

- **[Video Demo - Phase-2](https://youtu.be/oSHFfTpTDzw)**
- **Steps — Thought Process & Planning (Phase-1)**

**https://github.com/Obersan6/Mastermind-game/blob/main/docs/steps-thoughtprocess.md**

Focused on strengthening **backend logic** while keeping the UI **minimal and clear** (this is a **server-side challenge**, so styling is simple and time goes into enforceable logic and tests).

---

## Features

- **Difficulty-based timer (10 attempts remain constant)**  
   ```
   DIFFICULTY_OPTIONS = {'easy': 180, 'medium': 120, 'hard': 90}
   ```

- **Timer** — starts on New Game; after expiry guesses are blocked with a clear message.  
- **Scoring (non-persistent)** — score = guesses_left on win. Per-game only, no leaderboard yet.  
- **Game status** — enforced server-side: `in_progress → win | loss` (loss = attempts exhausted or timer expired).  
- **Flash & feedback messages** — immediate, supportive copy that explains each guess's outcome (e.g., "2 exact, 1 misplaced"), celebrates wins and softens losses with a brief encouragement. The tone keeps players engaged and informed without distracting from the core gameplay.
- **Database & models** — three tables for clean persistence:  

  - **User**: `id`, `username` (unique), `password_hash`, `created_at`  
  - **Game**: `id`, `user_id`, `secret_code`, `status`, `difficulty`, `max_guesses`, `attempts_used`, `guesses_left`, `started_at`, `expires_at`, `timer_total_s`, `score`, `player_username`  
  - **Guess**: `id`, `game_id`, `digits`, `exact_guess`, `number_only`, `created_at`  

- **Password hashing** — bcrypt for `users.password_hash` (future auth readiness).  
- **Randomness** — Random.org primary; Python secrets fallback (also for generating `SECRET_KEY`).  
- **Tests** — pytest for scoring, validation, timer enforcement, and happy-path routes.  

*Note: Hints deferred to Phase-3.*

---

## Quick Start

### 1) Clone
```
git clone https://github.com/Obersan6/Mastermind-game.git
cd Mastermind-game
```

### 2) Create & activate a virtual environment
```
python -m venv venv

# Windows (PowerShell / Git Bash)
source venv/Scripts/activate

# macOS/Linux
source venv/bin/activate
```

### 3) Install dependencies
```bash
# Recommended: pinned versions for reproducibility
pip install -r requirements.txt

# Fallback (manual)
pip install Flask Jinja2 python-dotenv pytest SQLAlchemy "psycopg[binary]" bcrypt requests
```

### 4) Configure environment
Create a `.env` file at project root:
```
SECRET_KEY=generated via secrets.token_hex(32)
APP_ENV=dev
# DATABASE_URL=postgresql+psycopg://postgres:<password>@localhost:5432/mastermind_db
```

Generate a strong key:
```
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5) Initialize database schema & seed (**required**)
Apply the schema (and included seed rows) before running the app:
```
psql -d mastermind_db -f docs/schema.sql
```

### 6) Run
```
flask run 
# open http://127.0.0.1:5000/
```

---

## Rules & Mechanics

- Secret = 4 digits, 0–7, duplicates allowed.  
- Feedback per guess:  
  - **exact_guess** — right digit & position  
  - **number_only** — right digit, wrong position (no double counting)  
- Game ends on win, attempts exhausted (10), or timer expiry.  
- New Game resets session and timer.

---

## Routes (Server-Rendered)

- `GET /` — Home: current game, attempts, timer, history, messages  
- `POST /new` — Start a new game (difficulty = easy|medium|hard, default medium)  
- `POST /guess` — Submit a guess (validated: 4 digits, 0–7)  

---

## Database & Seed

- Schema & seed in `docs/schema.sql` (DDL + example rows).  
- Apply with:  
  ```
  psql -d mastermind_db -f docs/schema.sql
  ```  
- bcrypt used for `users.password_hash` only (auth readiness).  
- DB credentials kept in `.env` (never committed).  

---

## Security & Secrets

- `.env` holds `SECRET_KEY` and DB credentials (never committed).  
- bcrypt secures user passwords.  
- DB password not hashed — use strong values in `.env`.  

---

## Testing
```
pytest -q
# run specific file, e.g.:
pytest tests/test_timer.py -q
```

Coverage priorities:
- guess_score duplicate handling  
- Timer start/expiry enforcement  
- Input validation (length/charset)  
- Happy-path routes + guardrails  

---

## Tech Stack

- Python 3  
- Flask  
- Jinja2, python-dotenv  
- Requests (Random.org), secrets (fallback RNG)  
- PostgreSQL with SQLAlchemy + psycopg (core persistence layer)  
- bcrypt (optional; for future user authentication)  
- Pytest (tests)


## Phase-3 — Planned Enhancements

- Rewards system (extra hints, more time, medal icons)  
- Hints (bounded, non-spoiling) 
- player or multiplayer mode  
- Analytics dashboard (game statistics, win rates)  
- User sign in / sign up (auth & validation)   

---
