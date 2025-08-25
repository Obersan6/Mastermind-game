# Unit tests for the compute_score() helper.
# These confirm scoring works correctly across win/loss cases and difficulties.

from app import compute_score

def test_score_win_easy():
    assert compute_score("easy", attempts_left=6, won=True) == 50 + 6*10

def test_score_win_hard_zero_left():
    assert compute_score("hard", attempts_left=0, won=True) == 100

def test_score_loss_any():
    assert compute_score("medium", attempts_left=5, won=False) == 0

