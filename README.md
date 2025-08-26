# Mastermind Game

## Description  
Implementation of the classic **Mastermind** game as part of the LinkedIn REACH backend challenge.  
A player tries to guess a secret 4-digit code (digits 0–7). After each guess, the game provides feedback on:  
- **Exact matches**: correct digit in the correct position  
- **Number-only matches**: correct digit in the wrong position  

The player has **10 attempts** to guess the secret code.  
Session state (secret code, history, attempts, game status) is stored server-side.  

---

## Development & Challenge Planning  
Before writing code, I outlined my approach and intentionally split the project into two phases:  

- **Phase-1 (this branch):** a clear, minimal solution that meets all requirements  
- **Phase-2 (main branch):** an enhanced version with additional features and tests  
- **Future (beyond scope):** possible enhancements such as multiplayer or analytics  

In a real-world scenario, it might be more efficient to begin with some upgrades you know will be included. Here, however, I chose to structure the work in phases as an explicit demonstration of my development approach:  

- Deliver the **baseline requirements first**, ensuring a complete and reviewable solution  
- Then add enhancements if time allows  

This demonstrates my mindset of **prioritizing core deliverables under tight deadlines while continuously seeking opportunities to add value**. It also makes the project evolution easier to follow for reviewers: first the essentials, then the extensions.  

---

## Implementation Plan  

### Phase-1 – Baseline (completed)  
The baseline version meets **all minimum challenge requirements**:  

- Generate 4-digit secret code using Random.org API (fallback to Python `secrets` if API is unavailable)  
- Allow digits 0–7 (**duplicates allowed** as per challenge spec)  
- Track guess history and display feedback after each attempt  
- Show number of guesses remaining  
- Lock input once the game is won or after 10 attempts  
- Option to start a new game at any time  
- Implemented with **Flask** and **Jinja2 templates**  

**Milestone links:**  
- **[Phase-1 baseline code](https://github.com/Obersan6/Mastermind-game/tree/phase-1)**  
- **[Video Demo – Phase-1](https://youtu.be/FbGLsqKqNGc)**  

**Related documentation:**  
- **[Steps – Thought Process & Planning - Phase-1](https://github.com/Obersan6/Mastermind-game/blob/phase-1/docs/steps-thoughtprocess.md)**

---

### Phase-2 – Upgraded Version  
Phase-2 introduces features such as timer, scoring, hints, difficulty levels, database integration, and tests.  

- **[Phase-2 updated code (branch main)](https://github.com/Obersan6/Mastermind-game/tree/main)**  
- **[Video demo - Phase-2](https://youtu.be/oSHFfTpTDzw)**  

---

### Phase-3 – Future Enhancements (beyond challenge scope)  
Not part of the take-home, but possible next steps:  

- **2-player or multiplayer mode** (e.g., competitive guessing or alternating turns)  
- **Signin/Signup (auth & validation)** to support personalized sessions *(optional)*  
- **Analytics dashboard** (game statistics, win rates)  
- **Rewards system** — e.g., extra hints, more time, or achievement icons  

---

## How to Run Locally  

1. Clone the repository:  
   ```bash
   git clone https://github.com/Obersan6/Mastermind-game.git
   cd Mastermind-game

2. Create a virtual environment:
   ```

   Windows (PowerShell / Git Bash / Hyper):

   python -m venv venv
   source venv/Scripts/activate


   macOS / Linux:

   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```

   Windows (PowerShell):

   set FLASK_APP=app.py
   flask run
   

   macOS / Linux:

   export FLASK_APP=app.py
   flask run
   ```

5. Open the game in your browser at:

   http://127.0.0.1:5000

## Tech Stack
```
Python 3  
Flask  
Jinja2 templates (bundled with Flask)  
Requests (Random.org API integration)  
GitHub for version control & documentation
```