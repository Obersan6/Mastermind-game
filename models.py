# project-root/models.py
"""SQLAlchemy models for users, games, guesses."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Integer, String, Text, DateTime, SmallInteger, ForeignKey,
    CheckConstraint, Computed, text
)
from sqlalchemy.sql import func

db = SQLAlchemy()

# ---------------------------
# Users
# ---------------------------
class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(Integer, primary_key=True)
    username      = db.Column(String(50), nullable=False, unique=True)
    password_hash = db.Column(Text, nullable=False)
    created_at    = db.Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    games = db.relationship("Game", backref="user", lazy=True)

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"


# ---------------------------
# Games
# ---------------------------
class Game(db.Model):
    __tablename__ = "games"

    id              = db.Column(Integer, primary_key=True)
    user_id         = db.Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    secret_code     = db.Column(String(4), nullable=False)  # regex check in __table_args__
    status          = db.Column(Text, nullable=False, server_default=text("'active'"))
    difficulty      = db.Column(Text, nullable=False, server_default=text("'medium'"))

    max_guesses     = db.Column(Integer, nullable=False, server_default=text("10"))
    attempts_used   = db.Column(Integer, nullable=False, server_default=text("0"))

    # GENERATED ALWAYS AS (max_guesses - attempts_used) STORED
    guesses_left    = db.Column(Integer, Computed("max_guesses - attempts_used", persisted=True))

    started_at      = db.Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at      = db.Column(DateTime(timezone=True))
    timer_total_s   = db.Column(Integer)  # validated by CHECK below

    score           = db.Column(Integer)
    player_username = db.Column(String(80))

    __table_args__ = (
        CheckConstraint("secret_code ~ '^[0-7]{4}$'", name="ck_games_secret_code_digits"),
        CheckConstraint("status IN ('active','won','lost')", name="ck_games_status"),
        CheckConstraint("difficulty IN ('easy','medium','hard')", name="ck_games_difficulty"),
        CheckConstraint("max_guesses > 0", name="ck_games_max_guesses_pos"),
        CheckConstraint("attempts_used BETWEEN 0 AND max_guesses", name="ck_games_attempts_between"),
        CheckConstraint("(timer_total_s IS NULL) OR (timer_total_s > 0)", name="ck_games_timer_pos_or_null"),
    )

    def __repr__(self):
        return f"<Game id={self.id} status={self.status} diff={self.difficulty} score={self.score}>"


# ---------------------------
# Guesses
# ---------------------------
class Guess(db.Model):
    __tablename__ = "guesses"

    id          = db.Column(Integer, primary_key=True)
    game_id     = db.Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)

    digits      = db.Column(String(4), nullable=False)        # regex check in __table_args__
    exact_guess = db.Column(SmallInteger, nullable=False)     # 0..4
    number_only = db.Column(SmallInteger, nullable=False)     # 0..4

    created_at  = db.Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    game = db.relationship("Game", backref=db.backref("guesses", lazy=True))

    __table_args__ = (
        CheckConstraint("digits ~ '^[0-7]{4}$'", name="ck_guesses_digits"),
        CheckConstraint("exact_guess BETWEEN 0 AND 4", name="ck_guesses_exact_range"),
        CheckConstraint("number_only BETWEEN 0 AND 4", name="ck_guesses_present_range"),
    )

    def __repr__(self):
        return f"<Guess id={self.id} game_id={self.game_id} exact={self.exact_guess} number={self.number_only}>"