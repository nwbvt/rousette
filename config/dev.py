from rousette import env

QUEUE = {"TYPE": env.QUEUE_TYPE_MEMORY}
PARSER = {"TYPE": env.PARSER_TYPE_BAG_OF_WORDS}
DB = {"CONNECTION_STRING": "sqlite:///db.sql"}
MODEL = {"SAVE_LOC": "./models", "MAX_DOCS": 100}