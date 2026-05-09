# SHL Assessment Recommendation Agent

A stateless conversational recommendation system for SHL assessments built with FastAPI, FAISS, and semantic retrieval.

## Overview

This project implements an AI-powered recommendation agent that:

* Recommends relevant SHL assessments from the SHL product catalog
* Handles multi-turn conversations using stateless conversation history
* Clarifies vague hiring or assessment requirements before recommending
* Supports refinement of recommendations when constraints change
* Compares SHL assessments using grounded catalog information
* Refuses off-topic or unsafe requests

The system is optimized for evaluator stability, low hallucination risk, deterministic behavior, and schema compliance.

---

## Features

### Conversational Behaviors

* Clarification for vague queries
* Assessment recommendation (1–10 recommendations)
* Recommendation refinement
* Grounded comparison between assessments
* Off-topic refusal and prompt-injection resistance

### Retrieval Pipeline

* FAISS vector similarity search
* Sentence-transformer semantic embeddings
* Lightweight deterministic reranking
* Intent-aware ranking boosts
* Leadership vs cognitive balancing

### Deployment

* FastAPI backend
* Stateless API design
* Render deployment ready
* Swagger/OpenAPI support

---

## Tech Stack

| Component     | Technology            |
| ------------- | --------------------- |
| API Framework | FastAPI               |
| Vector Search | FAISS                 |
| Embeddings    | sentence-transformers |
| Language      | Python 3.10           |
| Deployment    | Render                |
| Validation    | Pydantic              |

---

## Project Structure

```text
shl_assessment/
│
├── backend/
│   ├── app/
│   │   ├── evaluation/
│   │   ├── models/
│   │   ├── retrieval/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── data/
│   │   ├── catalog.json
│   │   ├── faiss.index
│   │   └── metadata.pkl
│   │
│   └── requirements.txt
│
├── render.yaml
├── runtime.txt
├── .python-version
├── .gitignore
└── README.md
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

### Chat Endpoint

```http
POST /chat
```

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Executive leadership benchmark"
    }
  ]
}
```

Response:

```json
{
  "reply": "Recommended assessments based on the current context.",
  "recommendations": [
    {
      "name": "OPQ Leadership Report",
      "url": "https://www.shl.com/products/product-catalog/view/opq-leadership-report/",
      "test_type": "P"
    }
  ],
  "end_of_conversation": true
}
```

---

## Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/shl_assessment.git
cd shl_assessment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Run Application

```bash
cd backend
uvicorn app.main:app --reload
```

Application runs at:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## Deployment

This project is configured for deployment on Render.

### Build Command

```bash
pip install -r backend/requirements.txt
```

### Start Command

```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Retrieval Design

### Semantic Retrieval

The system uses sentence-transformer embeddings with FAISS vector search to retrieve semantically relevant SHL assessments.

### Deterministic Reranking

A lightweight reranker adjusts ranking using:

* lexical overlap
* detected intents
* job levels
* category relevance
* leadership weighting
* cognitive weighting

This keeps the system:

* deterministic
* evaluator-stable
* low latency
* low hallucination

---

## Supported Assessment Categories

* Personality & Behavior
* Ability & Aptitude
* Knowledge & Skills
* Competencies
* Development & 360

---

## Example Queries

### Leadership

```text
Executive leadership benchmark
```

### Technical Hiring

```text
Java backend developer assessment
```

### Cognitive Assessment

```text
Graduate aptitude screening
```

### Comparison

```text
What is the difference between OPQ and GSA?
```

---

## Notes

* The API is fully stateless.
* Every `/chat` request contains the full conversation history.
* No conversation state is stored server-side.
* All recommendations are grounded in the SHL catalog.
* Returned URLs originate from catalog data only.

---

## Public Deployment

Production URL:

```text
https://shl-assessment-agent-z5nt.onrender.com
```

---

## Author

Arjun Mehra
