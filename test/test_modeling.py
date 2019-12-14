import pytest
import random
import numpy as np
from test.fixtures import *
from rousette.models import lda

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


@pytest.fixture
def docs():
    bat_docs = [(f"bat{i}", gen_doc_from_lang_model(BACKGROUND*.2 + BATS*.8, 100)) for i in range(20)]
    dog_docs = [(f"dog{i}", gen_doc_from_lang_model(BACKGROUND*.2 + DOGS*.8, 100)) for i in range(20)]
    bird_docs = [(f"bird{i}", gen_doc_from_lang_model(BACKGROUND*.2 + BIRDS*.8, 100)) for i in range(20)]
    all_docs = bat_docs + dog_docs + bird_docs
    random.shuffle(all_docs)
    return all_docs

@pytest.fixture
def doc_queue(docs, queue, parser):
    for doc_id, doc in docs:
        queue.put(doc_id, parser(doc))
    return queue

def test_lda(config, doc_queue, parser):
    vectorizer, model = lda(config, doc_queue, 3)
    assert set(vectorizer.vocabulary_) == set(VOCAB)
    bat_doc1 = gen_doc_from_lang_model(BACKGROUND*.2 + BATS*.8, 100)
    bat_doc2 = gen_doc_from_lang_model(BACKGROUND*.2 + BATS*.8, 100)
    dog_doc = gen_doc_from_lang_model(BACKGROUND*.2 + DOGS*.8, 100)
    bird_doc = gen_doc_from_lang_model(BACKGROUND*.2 + BIRDS*.8, 100)
    bat_vector1 = model.transform(vectorizer.transform(parser(bat_doc1)))
    bat_vector2 = model.transform(vectorizer.transform(parser(bat_doc2)))
    dog_vector = model.transform(vectorizer.transform(parser(dog_doc)))
    bird_vector = model.transform(vectorizer.transform(parser(bird_doc)))
    assert np.argmax(bat_vector1) == np.argmax(bat_vector2)
    assert np.argmax(bat_vector1) != np.argmax(dog_vector)
    assert np.argmax(bat_vector1) != np.argmax(bird_vector)
    assert np.argmax(bird_vector) != np.argmax(dog_vector)