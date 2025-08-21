# Mastermind Game

## Description
Implementation of the classic **Mastermind** game as part of the LinkedIn REACH backend challenge.  
A player tries to guess a secret 4-digit code (digits 0–7). After each guess, the game provides feedback on:
- **Exact matches**: correct digit in the correct position.
- **Number-only matches**: correct digit in the wrong position.

The player has **10 attempts** to guess the secret code.  
Session state (secret code, history, attempts, game status) is stored server-side.

---

## Implementation Plan

### Phase 1 - Baseline (completed)
The baseline version meets **all minimum challenge requirements**:

- Generate 4-digit secret code using Random.org API (fallback to Python `secrets` if API is unavailable).  
- Allow digits 0–7 (**duplicates allowed** as per challenge Implementation spec).  
- Track guess history and display feedback after each attempt.  
- Show number of guesses remaining.  
- Lock input once the game is won or after 10 attempts.  
- Option to start a new game at any time.  
- Implemented with **Flask** and **Jinja2 templates**.

**Milestone links:**
- [Phase 1 baseline code](https://github.com/Obersan6/Mastermind-game/tree/phase-1)  
- [Video Demo - Phase 1](https://youtube.com)  

**Related documentation:**
- [Steps - Thought Process & Planning](docs/steps-thoughtprocess.md)  

---

### Phase 2 - Extensions (in progress)
Phase 2 will explore **possible extensions** to showcase additional skills.  
These are **ideas under consideration** - not all may be implemented depending on available time:

- Hints  
- Levels of difficulty (different number ranges or hints)  
- Rewards or celebratory feedback when winning  
- Timer (per game or per guess)  
- 2-player or multiplayer mode  
- Additional tests (scoring logic, validation, win/lose conditions)  

If time allows, the app may also be deployed; otherwise a demo video will be provided.

Milestone link (when ready):  
- [Phase 2 snapshot](https://github.com/Obersan6/Mastermind-game/tree/phase-2)

---

### Phase 3 - Future Enhancements (beyond challenge scope)
Not part of the take-home, but showing possible future directions:

- Real-time multiplayer (using WebSockets)  
- Analytics dashboard (game statistics, win rates)  

---

## How to Run Locally

1. Clone the repository:
   ```
   git clone https://github.com/Obersan6/Mastermind-game.git
   cd Mastermind-game
   ```
2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
    source venv/Scripts/activate   # Windows Git Bash / Hyper
    pip install flask requests
   ```
3. Run the application:
   ```
   export FLASK_APP=app.py
   flask run
   ```
4. Open the game in your browser at `http://127.0.0.1:5000`

## Tech Stack

- Python 3
- Flask
- Jinja2 templates
- Requests (Random.org API integration)
- GitHub for version control & documentation
