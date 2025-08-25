# 🧠 Local AI Q&A Bot

A privacy-focused, offline Retrieval-Augmented Generation (RAG) chatbot that answers questions about your documents using local AI models via Ollama.

## ✨ Features

- **🔒 100% Private**: All processing happens locally on your machine
- **📄 Multi-format Support**: PDF, TXT, and Markdown files
- **🤖 Model Flexibility**: Switch between mistral, llama3.2, gemma2
- **💬 Chat History**: Persistent conversation memory
- **📊 Performance Metrics**: Real-time retrieval and generation timing
- **🎯 Source Citation**: View which documents were used for each answer
- **🔄 Dynamic Upload**: Add new documents without restarting

## 🚀 Quick Start

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

## 📋 Usage

### 1. Upload Documents
- Click "Browse files" or drag & drop
- Supports PDF, TXT, and Markdown files
- Multiple files can be uploaded at once

### 2. Ask Questions
- Type your question in the chat input
- The bot will retrieve relevant context and generate answers
- View performance metrics and sources for each response

### 3. Switch Models
- Use the sidebar to change between different local models
- Compare responses from different models

### 4. Manage Data
- Clear all uploaded data with the "Clear All Data" button
- Start fresh without losing your Ollama models

## 🛠️ Technical Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Document        │────│  Vector Store   │
│   (app.py)      │    │  Processor       │    │  (ChromaDB)     │
└─────────────────┘    │  (chunking)      │    └─────────────────┘
                       └──────────────────┘             │
                                                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   RAG Pipeline  │────│  Local LLM       │────│  Ollama         │
│   (rag_pipeline)│    │  (mistral/       │    │  (mistral,      │
│                 │    │   llama3.2)      │    │  llama3.2)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Core Components

- **app.py**: Streamlit web interface
- **document_processor.py**: File parsing and text chunking
- **vector_store.py**: ChromaDB vector storage with embeddings
- **rag_pipeline.py**: LangChain RAG implementation with memory
- **requirements.txt**: All dependencies

## 📊 Performance Monitoring

The app includes built-in performance metrics:

- **Retrieval Time**: How long to find relevant documents
- **Generation Time**: How long to create the AI response
- **Total Time**: Complete query processing time
- **System Stats**: Real-time performance testing

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set default model
export DEFAULT_MODEL=mistral

# Optional: Set chunk size for processing
export CHUNK_SIZE=1000
export CHUNK_OVERLAP=200
```

### Model Selection
Available models in the sidebar:
- **mistral**: Fast and accurate (recommended)
- **llama3.2**: Balanced performance
- **gemma2**: Lightweight option

## 🧪 Testing

Run the test suite:

```bash
# Basic functionality test
python test_simple.py

# Performance test
python test_system_safe.py
```

## 🐛 Troubleshooting

### Common Issues

1. **"Model not found" error**:
   ```bash
   ollama pull mistral
   ```

2. **Port already in use**:
   ```bash
   streamlit run app.py --server.port 8502
   ```

3. **Permission errors on Windows**:
   - Run as administrator or use WSL

4. **Memory issues with large documents**:
   - Reduce chunk size in document_processor.py
   - Process files in smaller batches

### Debug Mode
```bash
streamlit run app.py --logger.level debug
```

## 📁 Project Structure

```
local-ai-qa-bot/
├── app.py                    # Streamlit web interface
├── document_processor.py     # File processing and chunking
├── vector_store.py          # Vector database management
├── rag_pipeline.py          # RAG implementation
├── test_simple.py           # Basic functionality tests
├── test_system_safe.py      # Performance tests
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── uploads/                 # Temporary file storage (created automatically)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://python.langchain.com/) for the RAG framework
- [Ollama](https://ollama.com/) for local LLM serving
- [Streamlit](https://streamlit.io/) for the web interface
- [ChromaDB](https://www.trychroma.com/) for vector storage

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/local-ai-qa-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/local-ai-qa-bot/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/local-ai-qa-bot/wiki)

---

**⭐ Star this repo if you find it useful!**