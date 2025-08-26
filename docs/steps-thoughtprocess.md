# Steps - Thought Process & Planning

This document outlines my thought process, planning, and staged development for the Mastermind Game.  
It is structured to show time management, prioritization, and possible enhancements beyond the basic requirements.  
The file will be linked from the README.md in the repository.

## Phase 1 — Baseline (short recap)

For the longer, more descriptive Phase-1 version of this same file, see the phase-1 branch: **https://github.com/Obersan6/Mastermind-game/tree/phase-1**

### Core rules
* Secret is **4 digits**, each **0–7**; **duplicates allowed**.
* Feedback is **counts only** (never reveal which digit/position).

### Session-only
* No accounts and no database in Phase-1.

## Phase 2 — Plan (working notes)

Now Phase 1 is complete, so for this phase (Phase-2) I'll try to implement the following to make the game feel more alive while keeping it simple and solid:

* **Timer for the whole game (3 minutes):** starts on **New Game**; when time runs out, guesses are blocked and the round counts as a **loss** with a clear message.
* **Difficulty options:** `easy | medium | hard` control how many attempts you get (e.g., 12 / 10 / 8). Timer stays 3 minutes for all.
* **Supportive messages:** short feedback after each guess (e.g., "2 exact, 1 misplaced"), a small celebration on win, and a gentle note on loss.
* **Per-game scoring (non-persistent):** on win, `score = guesses_left`. No leaderboard yet.
* **Server-side enforcement:** inputs, attempts, and timer are all enforced on the backend so rules hold even without JS.
* **Randomness:** try Random.org first; fall back to Python `secrets`. Also use `secrets` to generate a strong `SECRET_KEY`.
* **Persistence:** use a clean PostgreSQL model layer (games and guesses); the app can still run session-only if needed, but Phase-2 includes DB support.

### What I will need

* **Environment & config**
  * `.env` with `SECRET_KEY` and `DATABASE_URL` (PostgreSQL DSN).
  * Update `.gitignore` as needed (venv, env files, caches).

* **Game state fields**
  * Timer: `started_at`, `expires_at = started_at + 180` (seconds).
  * Difficulty caps: set `max_guesses` per level; track `attempts_used`; compute/display `guesses_left`.

* **UX copy**
  * Short, supportive feedback per guess; quick celebration on win; gentle nudge on loss.

* **Models & schema (PostgreSQL)**
  * **User:** `id`, `username (unique)`, `password_hash` (bcrypt-ready), `created_at`
  * **Game:** `id`, `user_id (nullable)`, `secret_code (4×0–7)`, `status (in_progress|win|loss)`, `difficulty`, `max_guesses`, `attempts_used`, *(optionally stored)* `guesses_left`, `started_at`, `expires_at`, `timer_total_s`, `score`, `player_username`
  * **Guess:** `id`, `game_id`, `digits (4×0–7)`, `exact_guess (0–4)`, `number_only (0–4)`, `created_at`
  * Keep schema/seed in `docs/schema.sql`. Real secrets live in `.env`.

* **Testing (focused)**
  * `guess_score` handles duplicates correctly (no double counting).
  * Timer expiry blocks `/guess` and marks loss.
  * One happy-path route test covering `/new` + a couple of valid guesses.

### Tech stack (Phase-2)

* **Python 3, Flask, Jinja2, python-dotenv**
* **Requests** (Random.org), **secrets** (fallback RNG + secret keys)
* **SQLAlchemy + psycopg (PostgreSQL)**
* **bcrypt** (for `users.password_hash` readiness)
* **pytest** (small, focused tests)

## Phase 3 — Possible additions (later)

* **Hints** (bounded, non-spoiling; possibly tied to difficulty)
* **Leaderboard** (persist scores and compare across users)
* **Two-player / multiplayer** modes
* **Rewards** (small bonuses: medal icon, more hints, more minutes or more attempts)
* **Sign in / sign up** (bcrypt) and simple profile settings
* Optional **client-side countdown** (visual only; rules remain enforced on the server)
* **Basic analytics** (e.g., win rates)