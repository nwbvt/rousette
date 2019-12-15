import pytest
from test.fixtures import *
from rousette.models import lda, build_model, load_scorer, load_all_scorers
from rousette.db import MODEL


def test_lda(config, populated_queue, parser):
    vectorizer, model = lda(config, populated_queue, 3)
    assert set(vectorizer.vocabulary_) == set(VOCAB)
    bat_doc1 = bat_doc(200)
    bat_doc2 = bat_doc(200)
    dog_doc1 = dog_doc(200)
    bird_doc1 = bird_doc(200)
    bat_vector1 = model.transform(vectorizer.transform(parser(bat_doc1)))
    bat_vector2 = model.transform(vectorizer.transform(parser(bat_doc2)))
    dog_vector = model.transform(vectorizer.transform(parser(dog_doc1)))
    bird_vector = model.transform(vectorizer.transform(parser(bird_doc1)))
    assert np.argmax(bat_vector1) == np.argmax(bat_vector2)
    assert np.argmax(bat_vector1) != np.argmax(dog_vector)
    assert np.argmax(bat_vector1) != np.argmax(bird_vector)
    assert np.argmax(bird_vector) != np.argmax(dog_vector)

def test_build_model(config, populated_queue, parser, db):
    model_id = build_model(config, populated_queue, 3)
    result = db.execute(MODEL.select().where(MODEL.c.model_id==model_id)).fetchall()
    assert len(result) == 1
    score = load_scorer(config, model_id)
    bat_doc1 = parser(bat_doc(200))
    bat_doc2 = parser(bat_doc(200))
    assert np.argmax(score(bat_doc1)) == np.argmax(score(bat_doc2))

def test_load_all_models(config, model):
    scorers = load_all_scorers(config)
    assert model in scorers

def test_scorer(scorer, model):
    assert model in scorer.scorers