# SHL Assessment Recommendation Agent

A stateless conversational recommendation agent for SHL assessments built using FastAPI, FAISS, and Sentence Transformers.

The system recommends SHL Individual Test Solutions based on multi-turn conversational context, supports clarification and refinement flows, and performs grounded comparisons using catalog data only.

---

# Features

* Stateless conversational API
* SHL catalog grounded retrieval
* Multi-turn clarification and refinement
* Assessment recommendation (1–10 items)
* Comparison support (e.g. OPQ vs GSA)
* Prompt injection and off-topic refusal
* FAISS vector search + reranking
* FastAPI deployment-ready architecture

---

# Architecture

```text
User
  ↓
FastAPI API Layer
  ↓
Conversation Orchestrator
  ↓
Retriever
  ↓
FAISS Vector Search
  ↓
Rule-based Reranker
  ↓
Structured Response Formatter
```

---

# Tech Stack

* Python 3.10+
* FastAPI
* FAISS
* Sentence Transformers
* Uvicorn
* Pydantic

---

# Project Structure

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── retrieval/
│   │   ├── build_index.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   └── intent_detector.py
│   │
│   ├── services/
│   │   ├── orchestrator.py
│   │   ├── comparison.py
│   │   ├── normalize_catalog.py
│   │   └── test_type_mapper.py
│   │
│   └── evaluation/
│       └── test_queries.py
│
├── data/
│   ├── faiss.index
│   ├── metadata.pkl
│   └── raw/
│
├── requirements.txt
└── README.md
```

---

# API Endpoints

## Health Check

### GET `/health`

Response:

```json
{
  "status": "ok"
}
```

---

## Chat Endpoint

### POST `/chat`

Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "We need a solution for senior leadership"
    }
  ]
}
```

Response:

```json
{
  "reply": "Could you share more about the role, seniority level, and whether you need technical, cognitive, or personality assessments?",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

# Recommendation Response Example

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

# Test Type Mapping

| Code | Category               |
| ---- | ---------------------- |
| P    | Personality & Behavior |
| K    | Knowledge & Skills     |
| A    | Ability & Aptitude     |
| C    | Competencies           |
| D    | Development & 360      |

---

# Retrieval Pipeline

## 1. Query Understanding

The orchestrator analyzes:

* leadership intent
* technical intent
* cognitive intent
* personality intent
* comparison intent
* refinement intent

---

## 2. Semantic Retrieval

Sentence Transformer embeddings are used with FAISS vector search to retrieve relevant SHL assessments.

Model used:

```text
all-MiniLM-L6-v2
```

---

## 3. Reranking

A lightweight deterministic reranker adjusts scores using:

* lexical overlap
* category alignment
* leadership vs cognitive intent
* technical keyword matching
* assessment type weighting

This improves ranking precision while keeping behavior deterministic and evaluator-stable.

---

# Comparison Support

The system supports grounded catalog comparisons such as:

```text
Compare OPQ and GSA
What is the difference between OPQ32r and GSA?
```

Comparisons are generated only from catalog metadata and retrieved assessment entries.

---

# Clarification & Refinement

The agent:

* asks clarification questions for vague requests
* refines recommendations when constraints change
* reconstructs conversation state from full message history

No server-side session memory is used.

---

# Safety & Scope Control

The system:

* refuses off-topic requests
* blocks prompt injection attempts
* only recommends SHL catalog assessments
* never generates external URLs

---

# Local Setup

## 1. Clone Repository

```bash
git clone <your_repo_url>
cd backend
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Build FAISS Index

```bash
python app/retrieval/build_index.py
```

---

## 5. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## 6. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# Evaluation

The system was tested against:

* vague query clarification
* leadership recommendation flows
* technical hiring scenarios
* refinement conversations
* grounded comparison prompts
* prompt injection attempts
* off-topic refusal cases

---

# Design Decisions

* Deterministic orchestration was preferred over LLM routing for:

  * lower latency
  * evaluator stability
  * reduced hallucination risk
  * predictable schema compliance

* Retrieval quality was prioritized using:

  * FAISS semantic search
  * lightweight reranking
  * category-aware intent weighting

* The API is fully stateless:

  * every `/chat` request contains complete conversation history
  * no server-side conversation memory is stored

---

# Future Improvements

* Hybrid BM25 + vector retrieval
* Better comparison summarization
* Improved leadership ranking precision
* Expanded evaluation harness
* Optional frontend UI

---

# License

This project was built for the SHL AI Internship Assignment.
