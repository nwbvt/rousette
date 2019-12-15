"""
Package for working with queues
"""
from rousette import env
from rousette.queue.doc_queue import get_queue as get_doc_queue
from rousette.queue.vec_queue import get_queue as get_vec_queue
from rousette.queue import memory_queue

def init(config):
    """
    Creates a queue from a config
    """
    if config['QUEUE']['TYPE'] == env.QUEUE_TYPE_MEMORY:
        memory_queue.init_queue()