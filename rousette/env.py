from rousette import doc_parser, doc_queue
import yaml

QUEUE = None

def create_queue(config):
    """
    Creates a queue from a config
    """
    global QUEUE
    parser = None
    if config['parser']['type'] == "bag_of_words":
        parser = doc_parser.bag_of_words
    if config['queue']['type'] == "memory":
        QUEUE = doc_queue.MemoryDocumentQueue(parser)

def get_queue():
    """
    Get the queue
    """
    return QUEUE

def load_config(config_file):
    """
    Load the configuration
    """
    with open(config_file) as f:
        return yaml.load(f)