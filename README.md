# Multi-Agent-Fact-Check-System
Multi Agent system where two LLM agents argue opposite sides of a claim, a third agent judges based on retrieved evidence, and a final verdict is issued with confidence score. LangGraph is used for multi-agent orchestration. Applied it to detect misinformation on Indian news.
An AI-powered multi-agent fact verification system that evaluates the truthfulness of user claims using web search, local knowledge base retrieval, and LLM-based reasoning agents.

It combines:

🔍 Retrieval-Augmented Generation (RAG)

🌐 Live web search (Tavily API)

📚 Local FAISS knowledge base (Indian news corpus)

🤖 Multi-agent debate system (Advocate vs Refuter vs Judge)

🎯 Final structured verdict with confidence scoring

🖥️ Gradio UI for interactive use



🚀 Features
✔️ Fact-checks any user claim in real time

✔️ Uses trusted Indian sources (PIB, AltNews, BoomLive, Wikipedia, etc.)

✔️ Hybrid retrieval: FAISS + Web Search

✔️ Multi-agent reasoning:

Advocate Agent → supports claim

Refuter Agent → challenges claim

Judge Agent → final verdict

✔️ Structured JSON output (verdict, confidence, reasoning)

✔️ Interactive Gradio web interface

✔️ Modular LangGraph-based pipeline



🏗️ Architecture


User Claim

   ↓
   
Retriever Agent

   ├── Tavily Web Search
   
   └── FAISS Vector Search
   
   ↓
   
Advocate Agent (supports claim)

   ↓
   
Refuter Agent (debunks claim)

   ↓

Judge Agent (final decision)

   ↓
   
Gradio UI Output


📂 Project Structure
fact-check/

│

├── app.py                  # Gradio UI entry point

├── graph.py               # LangGraph pipeline orchestration

├── utils.py              # LLM (Groq) setup

│

├── agents/

│   ├── retriever.py

│   ├── advocate.py

│   ├── refuter.py

│   └── judge.py

│

├── retrieval/

│   ├── ingest.py         # Build FAISS index

│   ├── vector_store.py   # Local semantic search

│   └── web_search.py    # Tavily API search

│

├── indian_news/         # Raw dataset (PDF/TXT sources)

├── indian_news_index/   # FAISS vector database

│

├── requirements.txt

└── README.md


⚙️ Installation
1. Clone repository
git clone https://github.com/your-username/Multi-Agent-Fact-Check-System.git
cd Multi-Agent-Fact-Check-System
2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
🧠 Build Knowledge Base

Run ingestion to create FAISS index:

python retrieval/ingest.py
▶️ Run the Application
python app.py

Then open:

http://127.0.0.1:7860
🧪 Example

Input:

NEET 2024 paper was leaked before exam.

Output:

{
  "verdict": "TRUE / FALSE / UNVERIFIABLE",
  "confidence": 0.82,
  "reasoning": "Explanation based on evidence...",
  "sources": ["PIB article", "AltNews report"]
}


📊 Future Improvements
🔹 Evaluation benchmark dataset
🔹 Hallucination detection module
🔹 PDF report generation of verdict
🔹 Deployment on HuggingFace / Render


⚠️ Notes
Uses Groq LLM (ensure valid API key)
FAISS index must be built before running app
Large model calls may hit rate limits (free tier)


👨‍💻 Tech Stack
LangGraph / LangChain
Groq LLM (LLaMA 3)
FAISS
Tavily Search API
HuggingFace Embeddings
Gradio UI
Python
