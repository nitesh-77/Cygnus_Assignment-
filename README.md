#  Local AI Q&A Bot

A privacy-focused, offline Retrieval-Augmented Generation (RAG) chatbot that answers questions about your documents using local AI models via Ollama.


## Quick Start

### Prerequisites

1. **Install Ollama**: [Download here](https://ollama.com/download)
2. **Pull a model**:
   ```bash
   ollama pull mistral
   # or
   ollama pull llama3.2
   ```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/local-ai-qa-bot.git
   cd local-ai-qa-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`

### Core Components

- **app.py**: Streamlit web interface
- **document_processor.py**: File parsing and text chunking
- **vector_store.py**: ChromaDB vector storage with embeddings
- **rag_pipeline.py**: LangChain RAG implementation with memory
- **requirements.txt**: All dependencies


**⭐ Star this repo if you find it useful!**