"""Constants."""

# Tournament
NUMBER_OF_PLAYERS = 8
DEFAULT_NUMBER_OF_ROUNDS = 4
TIME_CONTROL_BULLET = 0
TIME_CONTROL_BLITZ = 1
TIME_CONTROL_RAPID = 2

# Player
PLAYERS_LAST_NAMES = ["DUPONT", "MARTIN", "PEREZ", "ROBERT"]
PLAYERS_FIRST_NAMES = ["Camille", "Charlie", "Dominique", "Sam"]
PLAYERS_BIRTH_DATES = ["03/08/1995", "25/02/2000", "09/12/1987", "10/10/1996"]
GENDER_M = 0
GENDER_F = 1
GENDERS = [GENDER_M, GENDER_F]

FIRST_ROUND_ID = 0

UPDATE_TOURNAMENT_PROMPT = "O"
UPDATE_PLAYERS_LIST_PROMPT = "O"

WIN_PROMPT = 'V'
LOSE_PROMPT = 'D'
DRAW_PROMPT = 'N'
SCORE_PROMPT = [WIN_PROMPT, LOSE_PROMPT, DRAW_PROMPT]
WIN_SCORE = 1
LOSE_SCORE = 0
DRAW_SCORE = 0.5
