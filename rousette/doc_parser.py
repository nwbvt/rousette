"""
Module for parsing documents
"""
from collections import Counter

def bag_of_words(document):
    """
    Simple bag of words parser
    """
    return Counter(document.split())
