from rousette import doc_parser, doc_queue

QUEUE_TYPE_MEMORY = "memory"
QUEUE_TYPE_KAFKA = "kafka"

PARSER_TYPE_BAG_OF_WORDS = "bag_of_words"

_QUEUE = None

def create_queue(config):
    """
    Creates a queue from a config
    """
    global _QUEUE
    parser = None
    if config.Parser['type'] == PARSER_TYPE_BAG_OF_WORDS:
        parser = doc_parser.bag_of_words
    if config.Queue['type'] == QUEUE_TYPE_MEMORY:
        _QUEUE = doc_queue.MemoryDocumentQueue(parser)

def get_queue():
    """
    Get the queue
    """
    return _QUEUE