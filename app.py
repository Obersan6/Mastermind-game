# /Mastermind-game/app.py 

from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets
import requests
from collections import Counter
from datetime import datetime, timezone, timedelta
from config import apply_config
from models import db, Game, Guess

app = Flask(__name__)

apply_config(app)  
db.init_app(app)    

def _utcnow():
    """Return timezone‑aware 'now' in UTC to match timezone=True columns."""
    return datetime.now(timezone.utc)

RANDOM_INTS_URL = 'https://www.random.org/integers/'

def fetch_secret_code():
    """Return 4 integers between 0 and 7 (inclusive). Duplicates allowed.
    Note: The 'Game rules' paragraph mentions 'four different numbers', but the
    'Implementation' section explicitly allows duplicates. This app follows the
    Implementation spec (duplicates allowed) for consistency with the API examples.
    """

    try:
        response = requests.get(
            RANDOM_INTS_URL, 
            params={'num': 4, 'min': 0, 'max': 7, 'col': 1, 'base': 10, 'format': 'plain', 'rnd': 'new'}, 
            timeout=5,
        )

        response.raise_for_status()
        return [int(line) for line in response.text.strip().splitlines()]
    
    except Exception:
        # Default to secrets if the API call fails (app remains functional even when offline)
        return [secrets.randbelow(8) for _ in range(4)]

MAX_GUESSES = 10

def start_game_session():
    """Ensure session keys used by templates exist (idempotent)."""
    session.setdefault('history', [])
    session.setdefault('game_over', False)

def score_guess(secret: str, guess: str) -> tuple[int, int]:
    """Return (exact_guess, number_only) comparing 4-digit strings with digits 0–7."""
    exact = sum(1 for s, g in zip(secret, guess) if s == g)
    sc = Counter(secret)
    gc = Counter(guess)
    present = sum(min(sc[d], gc[d]) for d in sc.keys())
    number_only = present - exact
    return exact, number_only

def _seconds_left(game):
    if not game or not game.expires_at:
        return 0
    remaining = int((game.expires_at - _utcnow()).total_seconds())
    return max(0, remaining)


# Homepage route where the game starts   
@app.get('/')
def home():
    start_game_session()

    game = None
    seconds_left = 0
    guesses_left = 0      # default 0
    max_guesses = 0       # default 0

    gid = session.get('game_id')
    if gid:
        game = db.session.get(Game, gid)
        if game:
            max_guesses = game.max_guesses or 0
            guesses_left = game.guesses_left or 0
            if game.status == 'active':
                seconds_left = _seconds_left(game)

    return render_template(
        'home.html',
        game=game,
        seconds_left=seconds_left,
        max_guesses=max_guesses,
        guesses_left=guesses_left,
        history=session.get('history', []),
        game_over=session.get('game_over', False)
    )


# Guess route to process user guesses
@app.post('/guess')
def make_guess():
    """Process a user's guess, persist it, enforce timer, and redirect to home."""

    start_game_session()

    if session.get('game_over'):
        return redirect(url_for('home'))

    game_id = session.get('game_id')
    if not game_id:
        flash("No active game.")
        return redirect(url_for('home'))

    game = db.session.get(Game, game_id)
    if not game or game.status != 'active':
        flash("No active game.")
        return redirect(url_for('home'))

    # --- TIMER ENFORCEMENT ---
    now = _utcnow()
    if game.expires_at and now >= game.expires_at:
        game.status = 'lost'   # treat timeout as a loss 
        db.session.commit()
        session['game_over'] = True
        flash("⏰ Time’s up! You ran out of time — start a new round and you’ll do even better.")
        return redirect(url_for('home'))
    # --------------------------

    # Read and validate the guess (expects "0123")
    guess_input = (request.form.get('guess') or '').strip()

    if len(guess_input) != 4 or any(ch not in '01234567' for ch in guess_input):
        flash("Please enter exactly 4 digits from 0–7 (e.g., 0123). You’ve got this!")
        return redirect(url_for('home'))

    # Score the guess against the DB secret (strings)
    exact_guess, number_only = score_guess(game.secret_code, guess_input)

    # Persist the guess row
    g_row = Guess(
        game_id     = game.id,
        digits      = guess_input,
        exact_guess = exact_guess,
        number_only = number_only,
    )
    db.session.add(g_row)

    # Increment attempts on the game
    game.attempts_used = (game.attempts_used or 0) + 1

    # Win condition
    if exact_guess == 4:
        game.status = 'won'
        # Optional mini-score: seconds_left + 5 * guesses_left (pre-commit estimate)
        seconds_left = max(0, int((game.expires_at - now).total_seconds())) if game.expires_at else 0
        guesses_left_est = max(0, (game.max_guesses or 0) - (game.attempts_used or 0))
        game.score = seconds_left + 5 * guesses_left_est
        db.session.commit()

        # Mirror a concise entry to session history for your template
        session.setdefault('history', []).append({
            'guess': [int(c) for c in guess_input],
            'exact_guess': exact_guess,
            'number_only': number_only
        })
        session.modified = True
        session['game_over'] = True
        flash("🎉 Exact match — fantastic! You cracked the code!")
        return redirect(url_for('home'))

    # Out-of-guesses loss (after this attempt)
    if game.attempts_used >= game.max_guesses:
        game.status = 'lost'
        db.session.commit()

        session.setdefault('history', []).append({
            'guess': [int(c) for c in guess_input],
            'exact_guess': exact_guess,
            'number_only': number_only
        })
        session.modified = True
        session['game_over'] = True
        flash("So close! You’ve used all attempts — start a new game and try a fresh pattern.")
        return redirect(url_for('home'))

    # Non-terminal case: commit and encourage
    db.session.commit()

    session.setdefault('history', []).append({
        'guess': [int(c) for c in guess_input],
        'exact_guess': exact_guess,
        'number_only': number_only
    })
    session.modified = True

    # Gentle feedback
    if exact_guess > 0:
        flash(f"Nice! {exact_guess} exact, {number_only} correct digits in other positions.")
    elif number_only > 0:
        flash(f"{number_only} digit(s) are in the code — shuffle positions and try again!")
    else:
        flash("No matches this time. Refine and fire another guess — you’ve got this.")

    return redirect(url_for('home'))


# Start a new game
@app.route('/new', methods=['GET', 'POST'])
def new_game():
    """Reset and start a new DB-backed game with a timer."""
    # Hard reset (clears any previous session state, including name)
    session.clear()

    # Initialize per-session keys you rely on (idempotent)
    start_game_session()

    # Support both query (?difficulty=) and form (<select name="difficulty">)
    difficulty = (
        request.form.get('difficulty') or
        request.args.get('difficulty') or
        'medium'
    )

    DIFFICULTY_OPTIONS = {'easy': 180, 'medium': 120, 'hard': 90}
    total_s = DIFFICULTY_OPTIONS.get(difficulty, 120)

    # Capture player name (POST preferred, fallback to any ?player_username=)
    player_username = (
        request.form.get('player_username') or
        request.args.get('player_username') or
        session.get('player_username')
    )
    if player_username:
        session['player_username'] = player_username

    # Generate the secret and create the game
    secret_list = fetch_secret_code()
    secret_str = ''.join(str(d) for d in secret_list)

    now = _utcnow()
    game = Game(
        player_username=session.get('player_username'),
        difficulty=difficulty,
        status='active',
        secret_code=secret_str,
        timer_total_s=total_s,
        started_at=now,
        expires_at=now + timedelta(seconds=total_s),
    )

    db.session.add(game)
    db.session.commit()

    session['game_id'] = game.id
    flash(f"New game started (difficulty: {difficulty}). You have {total_s // 60} minutes. Good luck!")
    return redirect(url_for('home'))