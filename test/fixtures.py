import pytest
import random
import numpy as np
from os import remove
import rousette
from test import test_config
from rousette.queue import get_doc_queue
from rousette.doc_parser import get_parser
from rousette.db import get_db, init_db
from rousette.models import Scorer, build_model

@pytest.fixture
def config_def():
    return test_config

@pytest.fixture
def app(config_def):
    return rousette.create_app(config_def)

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def config(app):
    return app.config

@pytest.fixture
def doc_queue(config):
    return get_doc_queue(config)

@pytest.fixture
def parser(config):
    return get_parser(config)

@pytest.fixture
def db(config):
    remove(config["DB"]["CONN_PARAMS"]["file"])
    init_db(config)
    return get_db(config)
    

VOCAB = ["the", "he", "she", "it", "is", "a", "an",
         "bat", "night", "echolocation", "cave",
         "dog", "bark", "sniff", "breed",
         "bird", "egg", "sing", "avian",
         "flying", "mammal", "alive", "pet"]

BACKGROUND = np.array([.12, .12, .12, .12, .12, .12, .12,
                       .01, .01, .01, .01,
                       .01, .01, .01, .01,
                       .01, .01, .01, .01,
                       .01, .01, .01, .01])

BATS = np.array([.01, .01, .01, .01, .01, .01, .01,
                 .12, .12, .12, .12,
                 .01, .01, .01, .01,
                 .01, .01, .01, .01,
                 .12, .12, .12, .01])

DOGS = np.array([.01, .01, .01, .01, .01, .01, .01,
                 .01, .01, .01, .01,
                 .12, .12, .12, .12,
                 .01, .01, .01, .01,
                 .01, .12, .12, .12])

BIRDS = np.array([.01, .01, .01, .01, .01, .01, .01,
                  .01, .01, .01, .01,
                  .01, .01, .01, .01,
                  .12, .12, .12, .12,
                  .12, .01, .12, .12])


def gen_doc_from_lang_model(probabilities, doc_length):
    """
    Generate a document from an a priori language model
    """
    choices = random.choices(VOCAB, probabilities, k=doc_length)
    return " ".join(choices)

def bat_doc(doc_length):
    return gen_doc_from_lang_model(BACKGROUND*.2 + BATS*.8, doc_length)

def dog_doc(doc_length):
    return gen_doc_from_lang_model(BACKGROUND*.2 + DOGS*.8, doc_length)

def bird_doc(doc_length):
    return gen_doc_from_lang_model(BACKGROUND*.2 + BIRDS*.8, doc_length)

@pytest.fixture
def docs():
    bat_docs = [(f"bat{i}", bat_doc(100)) for i in range(30)]
    dog_docs = [(f"dog{i}", dog_doc(100)) for i in range(30)]
    bird_docs = [(f"bird{i}", bird_doc(100)) for i in range(30)]
    all_docs = bat_docs + dog_docs + bird_docs
    random.shuffle(all_docs)
    return all_docs

@pytest.fixture
def populated_queue(docs, doc_queue, parser):
    for doc_id, doc in docs:
        doc_queue.put(doc_id, parser(doc))
    return doc_queue


@pytest.fixture
def model(config, populated_queue, parser, db):
    model_id = build_model(config, 3)
    return model_id

@pytest.fixture
def scorer(populated_queue, config, request, model, db):
    scorer = Scorer(config)
    scorer.start()
    request.addfinalizer(lambda: scorer.close())
    return scorer