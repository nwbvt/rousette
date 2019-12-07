"""
A memory backed queue
"""
from rousette import doc_parser, env

_QUEUE = None

def init_queue(config):
    global _QUEUE
    if config['PARSER']['TYPE'] == env.PARSER_TYPE_BAG_OF_WORDS:
        parser = doc_parser.bag_of_words
    _QUEUE = MemoryDocumentQueue(parser)

def get_queue():
    return _QUEUE

class MemoryDocumentQueue:
    """
    In memory implementation of a document queue
    Only applicable for small datasets
    """
    def __init__(self, doc_parser):
        self.doc_parser = doc_parser
        self.docs = []
        self.by_id = {}

    def submit_doc(self, doc_id, body):
        """
        Submit a document
        It will make a good faith effort to not reinsert an existing document, but this is not guarenteed
        """
        parsed = self.doc_parser(body)
        if doc_id in self.by_id:
            return self.by_id[doc_id]
        self.docs.append(parsed)
        self.by_id[doc_id] = self.docs.index(parsed)

    def get_doc(self, doc_id):
        """
        Get a document by id
        """
        if doc_id in self.by_id:
            return self.docs[self.by_id[doc_id]]

    def iter(self, n):
        """
        Get an iterator over the documents
        :param n: the maximum number of items in the iterator
        """
        return iter(self.docs[-n:])