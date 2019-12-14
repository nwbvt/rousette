from rousette import env

QUEUE = {"TYPE": env.QUEUE_TYPE_MEMORY}
PARSER = {"TYPE": env.PARSER_TYPE_BAG_OF_WORDS}
MODEL = {"SAVE_LOC": "./test/tmp", "MAX_DOCS": 100}
DB = {"CONNECTION_STRING": "sqlite:///{file}", "CONN_PARAMS": {"file": "test/db.sql"}}