Scrape / ingest raw data (BeautifulSoup, file uploads)
NLP preprocessing (spaCy + NLTK) → tokens, POS, NER
Concept extraction & category mapping (_categorize_concepts)
Embedding (BERT/LSTM/Word2Vec)
Build hybrid graph:
Symbolic edges (is-a, part-of, relates-to)
Similarity edges (cosine ≥ θ)
Persist graph & vectors (PostgreSQL for now)
