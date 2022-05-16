"""Constants."""
# GLOBAL
APP_NAME = "Chess Tournament Manager"

UPDATE_TOURNAMENT_PROMPT = "O"
UPDATE_PLAYERS_LIST_PROMPT = "O"

SEPARATOR_TYPE = "#"
SEPARATOR = SEPARATOR_TYPE * 79

# MODELS
# Tournament
NUMBER_OF_PLAYERS = 8
DEFAULT_NUMBER_OF_ROUNDS = 4
TIME_CONTROL_BLITZ = 0
TIME_CONTROL_BULLET = 1
TIME_CONTROL_RAPID = 2

TIME_CONTROL_BLITZ_PROMPT = "BL"
TIME_CONTROL_BULLET_PROMPT = "BU"
TIME_CONTROL_RAPID_PROMPT = "R"

# Player
GENDER_M = 0
GENDER_W = 1

GENDER_M_PROMPT = "H"
GENDER_W_PROMPT = "F"

# Round
FIRST_ROUND_ID = 0

# Match
WIN_SCORE = 1.0
LOSE_SCORE = 0
DRAW_SCORE = 0.5

WIN_PROMPT = "V"
LOSE_PROMPT = "D"
DRAW_PROMPT = "N"

# DATABASE
DB_TOURNAMENT_NAME = "name"
DB_TOURNAMENT_PLACE = "place"
DB_TOURNAMENT_DATE = "date"
DB_TOURNAMENT_TIME_CONTROL = "time_control"
DB_TOURNAMENT_DESCRIPTION = "description"
DB_TOURNAMENT_NUMBER_OF_ROUNDS = "number_of_rounds"

DB_PLAYER_ID = "id"
DB_PLAYER_LAST_NAME = "last_name"
DB_PLAYER_FIRST_NAME = "first_name"
DB_PLAYER_DATE_OF_BIRTH = "date_of_birth"
DB_PLAYER_GENDER = "gender"
DB_PLAYER_RANK = "rank"

DB_MATCH_FIRST_PLAYER_ID = "first_player_id"
DB_MATCH_FIRST_PLAYER_SCORE = "first_player_score"
DB_MATCH_SECOND_PLAYER_ID = "second_player_id"
DB_MATCH_SECOND_PLAYER_SCORE = "second_player_score"
