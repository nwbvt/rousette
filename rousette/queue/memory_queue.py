"""
A memory backed queue
"""
from rousette import doc_parser, env

_DOC_QUEUE = None

def init_queue():
    global _DOC_QUEUE
    _DOC_QUEUE = MemoryDocumentQueue()

def get_doc_queue():
    return _DOC_QUEUE

class MemoryDocumentQueue:
    """
    In memory implementation of a document queue
    Only applicable for small datasets
    """
    def __init__(self):
        self.docs = []
        self.by_id = {}

    def submit_doc(self, doc_id, doc):
        """
        Submit a document
        It will make a good faith effort to not reinsert an existing document, but this is not guarenteed
        """
        if doc_id in self.by_id:
            return self.by_id[doc_id]
        self.docs.append(doc)
        self.by_id[doc_id] = self.docs.index(doc)

    def get_doc(self, doc_id):
        """
        Get a document by id
        """
        if doc_id in self.by_id:
            return self.docs[self.by_id[doc_id]]

    def iter(self, n=0, since=0):
        """
        Get an iterator over the documents
        :param n: the maximum number of items in the iterator
        :param since: the documents since an index
        """
        start = -n or since
        return iter(self.docs[start:])