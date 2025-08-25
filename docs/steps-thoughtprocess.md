# Steps - Thought Process & Planning

This document outlines my thought process, planning, and staged development for the Mastermind Game.  
It is structured to show time management, prioritization, and possible enhancements beyond the basic requirements.

---

## Phase 1: Baseline (Take-Home Challenge Requirements)

In this phase I will implement only the minimal requirements as specified in the challenge.  
This ensures I meet the core requirements first and can demonstrate time management skills.

### Assumptions & Interpretations
- The secret code length is **4 digits**, each between **0–7**.
- **Duplicates are allowed** (per *Implementation* section of the challenge spec, even though “Game rules” say “different numbers”). I follow the *Implementation* spec for consistency with the API examples.
- The computer provides **counts only** (“correct digit, correct position” and “correct digit, wrong position”) — it never reveals which digit is correct.
- Session is stored **server-side**, no accounts or persistence required in Phase 1.

### Acceptance Criteria
- Player can submit a 4-digit guess (digits 0–7).
- Game responds with feedback:
  - `exact_guess` = correct digit in correct position.
  - `number_only` = correct digit in wrong position (no double counting).
- Feedback history is displayed.
- Remaining attempts counter is displayed.
- Game locks input when:
  - Player guesses all 4 digits correctly, or
  - Player reaches 10 attempts without success.
- Player can start a new game at any point.

### Things I Need
- Create virtual environment & download dependencies.
- Include elements to ignore in `.gitignore`.
- Implement sessions (server-side) to keep track of game state (secret, attempts, guesses).
- README.md explaining rules and how to run.
- *(Optional)* Include a short local run demo video.

### Baseline Tech Stack
- Python & Flask  
- Jinja2 templates (for rendering the game UI)  
- GitHub for hosting repository

### Test Plan (Phase 1)

I verified functionality by manually playing the game several times, covering different scenarios:

1. **General flow**
   - Played multiple games, verifying session persisted state between guesses.
   - Confirmed feedback is consistent when repeating the same guess twice.

2. **Winning condition**
   - Entered the correct code within the limit.
   - Verified game ends immediately.
   - Verified **“New Game” button** resets the session correctly.

3. **Losing condition**
   - Entered incorrect guesses until the 10th attempt.
   - Verified game ends automatically at 10 attempts.

4. **Duplicates handling**
   - Tested guesses with duplicates against codes containing duplicates.
   - Verified counts did not overcount (bag-based logic worked).

5. **New Game before completion**
   - Pressed “New Game” mid-game and confirmed session resets cleanly.

6. **Input validation**
   - Submitted invalid values (too short, letters, digits outside 0–7).
   - Verified these guesses were ignored (no crash, no history entry).

> Note: Phase-1 intentionally avoids database integration to keep the baseline minimal and easy to review.

---

## Phase 2: Additions (Extensions & Differentiation)

Once Phase-1 is completed, I plan to implement as many enhancements as possible before the deadline and may add others if time permits.  
Remaining ideas will be documented as **future enhancements** in the README.

> Even though all features can be achieved without a database or models, I may introduce them in Phase-2 to demonstrate additional backend skills and create a more structured foundation for possible extensions later.

---

### Gameplay Features
- **Timer (3 minutes for entire game)** – *challenge idea*  
- **Difficulty levels (adjust timer or number of attempts)** – *hybrid (challenge + my idea)*  
- **Hints (bounded, tied to difficulty)** – *challenge idea*  
- **Encouraging messages when losing / Celebration messages when winning** – *UX polish*  
- **Basic scoring system (attempts left = score)** – prepares for leaderboard or multiplayer  

### Testing
- Unit tests for:
  - `guess_score()` logic (including duplicates handling)
  - Timer enforcement
  - Input validation
- Simple route tests (happy-path game flow)

---

### Updated Tech Stack for Phase-2
- **Python & Flask** (web framework, routes, session management)  
- **Jinja2 templates** (UI rendering)  
- **Requests** (Random.org API)  
- **Secrets / os** (secure fallback random generation, secret key)  
- **Bootstrap** (quick styling, simple responsive UI) if time allows  
- **Pytest / unittest** (unit testing)  
- **PostgreSQL** (stretch: persistence for scores/users if user auth is added)  

---

### Additional Project Needs
- Update `.gitignore` as required (e.g., test artifacts, database files, venv).  
- Expand documentation in `README.md` to explain how to run Phase-2 and what extensions are included.  
- Provide a **video demo** if deployment time is too short.  

---

### Closing Note for Phase-2
The focus will be on **timer, difficulty levels, hints, and user feedback** as the primary extensions, since they balance feasibility with impact.  
If time allows, I will extend to **scoring/leaderboard**, laying the foundation for multiplayer mode during the technical interview.
