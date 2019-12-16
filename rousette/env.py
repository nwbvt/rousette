"""
Basic environemtn stuff
"""
from rousette import queue, db, models

QUEUE_TYPE_MEMORY = "memory"
QUEUE_TYPE_KAFKA = "kafka"
QUEUE_TYPE_DB = "db"

PARSER_TYPE_BAG_OF_WORDS = "bag_of_words"

def init(config):
    db.init_db(config)
    queue.init(config)
    if config.get('SCORER', {}).get('EMBEDDED'):
        scorer = models.Scorer(config)
        scorer.start()