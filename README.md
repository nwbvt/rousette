# Rousette
Scalable Document Vectorizer

## Overview

Rousette is designed to be an app that can be used to vectorize large numbers of documents.
It runs as a web app and has four primary endpoints.

1. `POST /docs`
  - `{"doc_id": "document identifier", "body": "The actual document text"}`
  - This adds a document to be vectorized. 
2. `POST /models`
  - `{"num_topics": numberOfTopics}`
  - This generates a model for vectorizing, where `num_topics` is the number of features the model will generate for each doc
  - There must be documents previously added
3. `GET /docs/doc_id/repr`
  - This returns the internal representation of the document
4. `GET /docs/doc_id/vector/model_id`
  - This returns the vectorized model

## Internals

Documents are stored in a bag of words format in an internal queue. Models are build using Latent Dirichlet allocation.
Internal representations of documents and their vectorizations are stored in a queue. The system is designed to use a distributed queue system such as Apache Kafka, however at the current time only an in memory queue is supported

## Install

1. `pip install -r requirements.txt`
2. `pip install ./`

## Running

1. `ROUSETTE_ENV=../config/dev.yaml FLASK_APP=rousette flask run`
2. A test script is provided to generate dummy documents in bulk. `python test/test_runner.py --length 1000 --num_docs 200` will generate 200 documents of 1000 words each and submit them to the api.
3. A document can be viewed using curl, `curl localhost:5000/docs/sample/doc_0/repr`
4. A model can be generaged `curl -d '{"num_topics": 3}' -H "Content-Type: application/json" localhost:5000/models`
5. Then the vector representation can be retrieved `curl localhost:5000/docs/sample/doc_0/vector/0`