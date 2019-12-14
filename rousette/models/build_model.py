"""Module for building models"""
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from smart_open import open

def filename(config, model_id):
    "Get the filename for a model"
    save_loc = config['MODEL']['SAVE_LOC']
    filename = f"{save_loc}/{model_id}.pkl"

def build_model(config, doc_queue, num_topics, model_id):
    """Build and save a model"""
    model = lda(config, doc_queue, num_topics)
    with open(filename(config, model_id), 'wb') as f:
        pickle.dump(model, f)
    return filename


def lda(config, doc_queue, num_topics):
    """Build an LDA model"""
    max_docs = config['MODEL']['MAX_DOCS']
    docs = doc_queue.iter(n=max_docs)
    vectorizer = DictVectorizer()
    features = vectorizer.fit_transform(docs)
    lda = LatentDirichletAllocation(n_components=num_topics)
    lda.fit(features)
    return vectorizer, lda