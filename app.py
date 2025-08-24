# /Mastermind-game/app.py 

from flask import Flask, render_template, request, redirect, url_for, session
import os, secrets
import requests
from collections import Counter
from config import apply_config
from models import db

app = Flask(__name__)

apply_config(app)  
db.init_app(app)    

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
    """Initialize a new game session.
       Session state structure":
       - session['secret_code']: list of 4 integers (0-7)
       - session['max_guesses']: integer (total guesses allowed)
       - session['history']: list[dict] of {'guess': list[int], 'exact_guess': int, 'number_only': int}
    """
    if 'secret_code' not in session:
        session['secret_code'] = fetch_secret_code()
        session['max_guesses'] = MAX_GUESSES
        session['history'] = []
        session['game_over'] = False

def guess_score(guess, secret_code):
    """
    Compare a guess with secret_code.
    
    Returns (exact_guess, number_only) where:
    - exact_guess: correct digits, correct position
    - number_only: correct digits, wrong position 
    """

    # 1st iteration: count exact matches, remove them and collect remaining digits (both guesses and secret_code)
    exact_guess = 0
    remaining_guess = []
    remaining_secret_code = []

    for g, s in zip(guess, secret_code):
        if g == s:
            exact_guess += 1
        else:
            remaining_guess.append(g)
            remaining_secret_code.append(s)
    
    # 2nd iteration: Build bag of remaining digits of secret_code & count number-only matches from remaining_guess (using a bag so duplicates don't overcount)
    
    bag = Counter(remaining_secret_code)
    number_only = 0

    for g in remaining_guess:
        if bag[g] > 0:
            number_only += 1 
            bag[g] -= 1 
    
    return exact_guess, number_only

# Homepage route where the game starts   
@app.get('/')
def home():
    """Render homepage with game instructions and start session."""
    start_game_session()
    guesses_left = session['max_guesses'] - len(session['history'])

    return render_template(
        'home.html',
        max_guesses=session['max_guesses'], 
        guesses_left=guesses_left,
        history=session['history'],
        game_over=session.get('game_over', False)
    )

# Guess route to process user guesses
@app.post('/guess')
def make_guess():
    """Process a user's guess, update session state, and redirect to home."""

    start_game_session()

    # Stop accepting guesses if game is over 
    if session.get('game_over'):
        return redirect(url_for('home'))  

    # Accept a single input like "0123" or return early if invalid
    guess_input = (request.form.get('guess') or '').strip()

    if len(guess_input) !=4 or any(char not in '01234567' for char in guess_input):
        return redirect(url_for('home'))
    
    guess = [int(char) for char in guess_input]

    exact_guess, number_only = guess_score(guess, session['secret_code'])

    session['history'].append({
        'guess': guess,
        'exact_guess': exact_guess,
        'number_only': number_only 
    })
    # Tell Flask the session changed (so updates inside lists/dicts actually get saved)
    session.modified = True

    # Stop input from user if limit guesses reached or user wins
    if exact_guess == 4 or len(session['history']) >= session['max_guesses']:
        session['game_over'] = True

    if session.get('game_over'):
        return redirect(url_for('home'))
    
    return redirect(url_for('home'))

# Start a new game
@app.post('/new')
def new_game():
    """Reset game session to start a new game."""

    session.clear()
    start_game_session()
    
    return redirect(url_for('home'))
