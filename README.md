# DocMind 🧠

> Upload a document. Ask anything. Get answers straight from your content.

DocMind is a RAG (Retrieval-Augmented Generation) application that lets you chat with your own PDF or text files using natural language. It combines semantic search with GPT-4o-mini to return precise, grounded answers — not hallucinations.

---

## How it works

```
┌─────────────────────────────────────────────────────────┐
│                    INDEXING PIPELINE                    │
│                                                         │
│  PDF / TXT  ──►  Text extraction  ──►  Chunking        │
│                                        (500 tokens,     │
│                                         50 overlap)     │
│                        │                                │
│                        ▼                                │
│               OpenAI Embeddings       ChromaDB          │
│            (text-embedding-3-small) ──► storage/        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     QUERY PIPELINE                      │
│                                                         │
│  User question  ──►  Embed question                     │
│                            │                            │
│                            ▼                            │
│                   Top-3 similar chunks                  │
│                   retrieved from ChromaDB               │
│                            │                            │
│                            ▼                            │
│                    GPT-4o-mini generates                │
│                    answer from context                  │
│                            │                            │
│                            ▼                            │
│                     Answer in chat                      │
└─────────────────────────────────────────────────────────┘
```

ChromaDB persists to disk — documents remain indexed across sessions, no need to re-upload.

---

## Tech stack

| Layer        | Technology                     |
|--------------|-------------------------------|
| UI           | Streamlit                     |
| RAG framework| LlamaIndex                    |
| LLM          | OpenAI GPT-4o-mini            |
| Embeddings   | OpenAI text-embedding-3-small |
| Vector store | ChromaDB (persistent)         |
| PDF reader   | PyMuPDF                       |

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/stevkouakam/DocMind.git
cd DocMind
```

**2. Create a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install streamlit llama-index llama-index-llms-openai llama-index-embeddings-openai \
            llama-index-vector-stores-chroma llama-index-readers-file \
            chromadb pymupdf python-dotenv
```

**4. Add your OpenAI API key**

Create a `.env` file at the project root:
```
OPENAI_API_KEY=your_openai_key_here
```

**5. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Usage

1. Upload a **PDF** or **TXT** file using the file uploader
2. Wait for indexing to complete
3. Type any question about the document in the chat input
4. DocMind retrieves the 3 most relevant passages and generates a grounded answer

---

## Project structure

```
DocMind/
├── app.py          # Streamlit interface
├── rag.py          # Indexing and query engine
├── .env            # API key (not committed)
├── .env.example    # Config template
└── storage/        # ChromaDB vector database (not committed)
```

---

## License

MIT
