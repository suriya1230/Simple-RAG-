# ⚡ NovaDocs — RAG with Groq + Llama 3 / Mixtral

Ultra-fast Retrieval-Augmented Generation using **Groq's free API** and open-source LLMs.

---

## 🚀 Quickstart

```bash
pip install -r requirements.txt
streamlit run app.py
```

Get a **free** Groq API key → https://console.groq.com

---

## 🤖 Available Models

| Label | Model ID | Best for |
|---|---|---|
| Llama 3.3 · 70B | `llama-3.3-70b-versatile` | Best quality answers |
| Llama 3.1 · 8B  | `llama-3.1-8b-instant`   | Fastest responses |
| Mixtral 8×7B    | `mixtral-8x7b-32768`     | Long context, versatile |
| Llama 3 · 70B   | `llama3-70b-8192`        | Stable, reliable |
| Llama 3 · 8B    | `llama3-8b-8192`         | Lightweight |
| Gemma 2 · 9B    | `gemma2-9b-it`           | Google's open model |

---

## 🏗 Architecture

```
Document (PDF/TXT/MD)
    ↓ chunking (word-based, configurable overlap)
TF-IDF Index (pure Python, no ML libs)
    ↓ cosine similarity retrieval
Top-K relevant chunks
    ↓ prompt engineering
Groq API → Llama 3 / Mixtral (streaming)
    ↓
Streamed Answer + Source chunks shown
```

---

## 📁 Files

```
rag_groq/
├── app.py           # Streamlit app
├── requirements.txt
└── README.md
```

Website Link: https://dbrrxeuyntidanxeug4s7n.streamlit.app
