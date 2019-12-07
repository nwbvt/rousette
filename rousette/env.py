"""
Basic environemtn stuff
"""
from rousette.queue import doc_queue

QUEUE_TYPE_MEMORY = "memory"
QUEUE_TYPE_KAFKA = "kafka"
QUEUE_TYPE_DB = "db"

PARSER_TYPE_BAG_OF_WORDS = "bag_of_words"

def init(config):
    doc_queue.init(config)