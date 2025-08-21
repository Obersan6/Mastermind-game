# Steps - Thought Process & Planning

This document outlines my thought process, planning, and staged development for the Mastermind Game.  
It is structured to show time management, prioritization, and possible enhancements beyond the basic requirements.  
The file will be linked from the README.md in the repository.

---

## Phase 1: Baseline (Take-Home Challenge Requirements)

In this phase I will implement only the minimal requirements as specified in the challenge.  
This ensures I meet the core requirements first and can demonstrate time management skills.

### Assumptions & Interpretations
- The secret code length is **4 digits**, each between **0–7**.
- **Duplicates are allowed** (per *Implementation* section of the challenge spec, even though “Game rules” say “different numbers”). I follow the *Implementation* spec for consistency with the API examples.
- The computer provides **counts only** (“correct digit, correct position” and “correct digit, wrong position”) - it never reveals which digit is correct.
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
- User flow documentation.
- README.md explaining rules and how to run.
- (Optional Phase 1) Deployment on Render.

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

---

## Phase 2: Additions (Extensions & Differentiation)

Once the baseline is complete and functional, I will add features to differentiate my submission and show architecture skills.  
These additions are grouped into themes for clarity.

### Gameplay Feature Ideas
At this stage, these are **ideas under consideration** for Phase 2.  
Different features could be implemented instead (or alongside these).  
They showcase possible extensions but may not all be implemented, depending on available time:
- Hints
- Levels of difficulty (more numbers or fewer hints)
- Rewards when guessing & winning
- Timer (per game or per guess)
- 2-player or multiplayer mode
- Tests for scoring logic, input validation, and win/lose conditions

### User Features
- User sign in / sign up (authentication & validation)
- User management
- Player score & Leaderboard with other users’ scores

### UX Enhancements
- Encouraging messages even when losing
- Celebration messages when winning
- Competitive feedback (e.g., warning a history winner that another user is improving their score)

### Additional Things I Need
- Download additional dependencies
- Update `.gitignore` as needed
- Add models | tables | db | templates | error messages | table diagrm | user flow
- Link from README.md to the baseline version of the game (code link) 
- Optionally deploy the app (if time permits); otherwise provide a video demo
- Expanded tests for new features

### Extended Tech Stack
- PostgreSQL (for persistence of scores, history, users)
- Jinja2 templates (if expanding UI)
- Bootstrap (chosen over Tailwind CSS for simplicity and speed)

---

## Phase 3: Possible Enhancements (Future Consideration)

These are not in scope for the take-home or additions, but show foresight and architectural thinking.  
They can be mentioned in the README as future possibilities.

- Real-time multiplayer (using WebSockets)
- Analytics dashboard (game statistics, win rates)

---

## Closing Note

The project will be developed in stages:  
1. Deliver the baseline version (Phase 1).  
2. Extend with additional features (Phase 2).  
3. Document possible future enhancements (Phase 3).  

This staged approach demonstrates planning, time management, and ability to think beyond immediate requirements.
