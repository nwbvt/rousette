"""
A memory backed queue
"""
from rousette import doc_parser, env

_DOC_QUEUE = None
_VEC_QUEUE = None

def init_queue():
    global _DOC_QUEUE
    global _VEC_QUEUE
    _DOC_QUEUE = MemoryQueue()
    _VEC_QUEUE = MemoryQueue()


def get_doc_queue():
    return _DOC_QUEUE


def get_vec_queue():
    return _VEC_QUEUE


class MemoryQueue:
    """
    In memory implementation of a document queue
    Only applicable for small datasets
    """
    def __init__(self):
        self.docs = []
        self.by_id = {}
        self.listeners = []

    def put(self, doc_id, doc):
        """
        Submit a document
        It will make a good faith effort to not reinsert an existing document, but this is not guarenteed
        """
        if doc_id in self.by_id:
            return self.by_id[doc_id]
        self.docs.append((doc_id, doc))
        self.by_id[doc_id] = self.docs.index((doc_id, doc))
        for listener in self.listeners:
            listener.notify(doc_id, doc)

    def get_by_id(self, doc_id):
        """
        Get a document by id
        """
        if doc_id in self.by_id:
            return self.docs[self.by_id[doc_id]][1]

    def iter(self, n=0, since=0):
        """
        Get an iterator over the documents
        :param n: the maximum number of items in the iterator
        :param since: the documents since an index
        """
        start = -n or since
        return iter(self.docs[start:])
    
    def register_listener(self, listener):
        """
        Register a listener
        """
        self.listeners.append(listener)