"""Module for building models"""
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from smart_open import open
from sqlalchemy import select
from rousette.db import get_db, MODEL
from rousette.queue import doc_queue, vec_queue

def filename(config, model_id):
    "Get the filename for a model"
    save_loc = config['MODEL']['SAVE_LOC']
    return f"{save_loc}/{model_id}.pkl"


def build_model(config, doc_queue, num_topics):
    """Build and save a model"""
    db = get_db(config)
    with db.connect() as conn:
        result = conn.execute(MODEL.insert().values(num_features=num_topics))
        model_id = result.inserted_primary_key[0]
    model = lda(config, doc_queue, num_topics)
    model_location = filename(config, model_id)
    with open(model_location, 'wb') as f:
        pickle.dump(model, f)
    with db.connect() as conn:
        conn.execute(MODEL.update().where(MODEL.c.model_id == model_id)
                     .values(defintion_location=model_location))
    return model_id


def lda(config, doc_queue, num_topics):
    """Build an LDA model"""
    max_docs = config['MODEL']['MAX_DOCS']
    docs = doc_queue.iter(n=max_docs)
    vectorizer = DictVectorizer()
    features = vectorizer.fit_transform([doc for _, doc in docs])
    lda = LatentDirichletAllocation(n_components=num_topics)
    lda.fit(features)
    return vectorizer, lda


def load_model(config, model_id):
    """Load a model"""
    with get_db(config).connect() as conn:
        filename = conn.execute(select([MODEL.c.defintion_location])
                                .where(MODEL.c.model_id == model_id)).fetchone()[0]
    with open(filename, 'rb') as f:
        return pickle.load(f)

    
def load_scorer(config, model_id):
    vectorizer, model = load_model(config, model_id)
    def score(doc):
        vect = vectorizer.transform(doc)
        return model.transform(vect)
    return score


def load_all_scorers(config):
    """Load all the scoring functions"""
    db = get_db(config)
    with db.connect() as conn:
        model_ids = conn.execute(select([MODEL.c.model_id]))
    return {model_id: load_scorer(config, model_id) for model_id, in model_ids}


class Scorer:
    def __init__(self, config):
        self.config = config
        self.scorers = load_all_scorers(config)
        self.vec_queue = vec_queue.get_queue(config)

    def start(self):
        in_queue = doc_queue.get_queue(self.config)
        in_queue.register_listener(self)
        for doc_id, doc in in_queue.iter():
            self.score_doc(doc_id, doc)

    def score_doc(self, doc_id, doc):
        for model_id, scorer in self.scorers.items():
            self.vec_queue.put((doc_id, model_id), scorer(doc))
    
    def notify(self, doc_id, doc):
        self.score_doc(doc_id, doc)