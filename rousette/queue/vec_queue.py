"""Module for queues for the vectorized documents from the models"""
from rousette import env
from rousette.queue import memory_queue


def get_queue(config):
    """
    Get the queue
    """
    if config['QUEUE']['TYPE'] == env.QUEUE_TYPE_MEMORY:
        return memory_queue.get_vec_queue()
    return None
