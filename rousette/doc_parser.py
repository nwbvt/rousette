"""
Module for parsing documents
"""
from collections import Counter
from rousette import env

def bag_of_words(document):
    """
    Simple bag of words parser
    """
    words = document.split()
    counter = Counter(words)
    return counter

def get_parser(config):
    """
    Get the document parser
    """
    if config['PARSER']['TYPE'] == env.PARSER_TYPE_BAG_OF_WORDS:
        return bag_of_words