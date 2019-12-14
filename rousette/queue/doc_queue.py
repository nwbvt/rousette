"""
Module for defining document queues
"""
from rousette import env
from rousette.queue import memory_queue

def init(config):
    """
    Creates a queue from a config
    """
    if config['QUEUE']['TYPE'] == env.QUEUE_TYPE_MEMORY:
        memory_queue.init_queue()

def get_queue(config):
    """
    Get the queue
    """
    if config['QUEUE']['TYPE'] == env.QUEUE_TYPE_MEMORY:
        return memory_queue.get_doc_queue()
    return None