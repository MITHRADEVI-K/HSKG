# HSKG - Hybrid Semantic Knowledge Graph

Intelligent knowledge extraction and graph construction system that transforms unstructured data into structured, queryable knowledge graphs using NLP and machine learning.

## Overview

HSKG is an automated data processing pipeline that extracts concepts, entities, and relationships from raw text and organizes them into a searchable knowledge graph. It combines traditional NLP with deep learning to create both symbolic and similarity-based connections.

The system handles text documents, web-scraped content, and uploaded files, processing them through multiple stages to build a comprehensive knowledge representation.

## Why We Built This

HSKG automates the extraction of concepts and relationships from unstructured data, transforming scattered information into queryable knowledge graphs. It enables semantic search across research papers, enterprise documents, and large datasets using hybrid rule-based and AI-driven methods.

## Key Features

**Hybrid Graph Architecture** combines symbolic edges for explicit relationships like is-a, part-of, and relates-to with semantic edges based on embedding similarity scores.

**Multi-source Data Ingestion** supports web scraping with BeautifulSoup, direct file uploads, and text input processing.

**Advanced NLP Pipeline** uses spaCy and NLTK for tokenization, part-of-speech tagging, named entity recognition, and concept extraction with automatic category mapping.

**Multiple Embedding Methods** implements BERT transformers, LSTM networks, and Word2Vec for generating semantic representations of concepts.

**Graph Persistence** stores the complete knowledge graph and vector embeddings in PostgreSQL for efficient querying and retrieval.

## How It Works

```
┌─────────────────┐
│ Data Ingestion  │  Web scraping, file uploads, text input
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ NLP Processing  │  Tokenization, POS tagging, NER (spaCy/NLTK)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Concept Extract │  Identify & categorize entities and terms
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Embedding Gen   │  BERT/LSTM/Word2Vec vector representations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Graph Building  │  Symbolic edges + Similarity edges (cosine)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Storage (PSQL)  │  Persist graph & embeddings with indexing
└─────────────────┘
```

## Results and Impact

**Knowledge Discovery:** The hybrid approach uncovers both obvious and hidden relationships between concepts that would be missed by rule-based systems alone.

**Query Performance:** Graph structure enables complex multi-hop queries to execute efficiently, finding connections across multiple relationship types.

**Scalability:** The pipeline processes large document collections, building comprehensive knowledge graphs from thousands of sources.

**Accuracy:** Combining symbolic reasoning with neural embeddings improves precision in relationship detection compared to either method alone.

**Flexibility:** The modular architecture allows swapping embedding models or adding new relationship types without rebuilding the entire system.

## Getting Started

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the main pipeline:
```bash
python main.py
```

For a quick demo of the text processing:
```bash
python demo_text_pipeline.py
```

The system requires Python 3.8+ and PostgreSQL for graph storage. Configuration for embedding models and similarity thresholds can be adjusted in the main pipeline script.

## Technical Stack

**NLP Processing:** spaCy, NLTK  
**Embeddings:** BERT, LSTM, Word2Vec  
**Web Scraping:** BeautifulSoup  
**Database:** PostgreSQL  
**Language:** Python

## Project Structure

The repository contains the main pipeline implementation, demo scripts for testing individual components, a web dashboard for visualization, sample datasets, and configuration files for development environments.
