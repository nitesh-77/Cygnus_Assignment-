import streamlit as st
import os
from pathlib import Path
import time
from document_processor import DocumentProcessor
from vector_store import VectorStore
from rag_pipeline import RAGPipeline

# Page configuration
st.set_page_config(
    page_title="Local AI Q&A Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = VectorStore()

if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None

if 'document_processor' not in st.session_state:
    st.session_state.document_processor = DocumentProcessor()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Helper functions
def format_time(seconds):
    """Format time in seconds to appropriate unit."""
    if seconds < 0.001:
        return f"{seconds*1000:.2f}ms"
    elif seconds < 1:
        return f"{seconds*1000:.1f}ms"
    else:
        return f"{seconds:.2f}s"

def initialize_rag_pipeline():
    """Initialize the RAG pipeline if vector store has documents."""
    if st.session_state.vector_store.get_store_info()["count"] > 0:
        try:
            st.session_state.rag_pipeline = RAGPipeline(
                st.session_state.vector_store
            )
            return True
        except Exception as e:
            st.error(f"Error initializing RAG pipeline: {e}")
            return False
    return False

def process_uploaded_files(uploaded_files):
    if not uploaded_files:
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    all_documents = []
    
    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        
        # Save uploaded file
        file_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process file
        documents = st.session_state.document_processor.process_file(file_path)
        all_documents.extend(documents)
        
        progress_bar.progress((idx + 1) / len(uploaded_files))
    
    if all_documents:
        status_text.text("Creating vector store...")
        st.session_state.vector_store.create_vector_store(all_documents)
        
        status_text.text("Initializing RAG pipeline...")
        initialize_rag_pipeline()
        
        progress_bar.empty()
        status_text.empty()
        st.success(f"Processed {len(uploaded_files)} files with {len(all_documents)} total chunks!")

def clear_all_data():
    st.session_state.vector_store.clear_store()
    st.session_state.rag_pipeline = None
    st.session_state.messages = []
    st.session_state.uploaded_files = []
    
    # Clear uploads directory
    import shutil
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")
    
    st.success("All data cleared!")
    st.rerun()

# Sidebar
with st.sidebar:
    st.title(" Local AI Q&A Bot")
    st.markdown("---")
    
    # Model selection
    st.subheader("Model Settings")
    model_name = st.selectbox(
        "Select Model",
        ["llama3.2", "mistral", "gemma2"],
        index=0
    )
    
    # Vector store info
    st.subheader("System Status")
    if st.session_state.vector_store:
        store_info = st.session_state.vector_store.get_store_info()
        st.metric("Documents", store_info.get("count", 0))
        st.metric("Status", store_info.get("status", "unknown"))
    
    # Clear data button
    if st.button("Clear All Data", type="secondary"):
        clear_all_data()
    
    st.markdown("---")
    st.markdown("### Instructions")
    st.markdown("""
    1. Upload PDF, TXT, or MD files
    2. Wait for processing to complete
    3. Ask questions about your documents
    4. View sources in the sidebar
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.title("💬 Chat with your Documents")
    
    # File upload section
    st.subheader("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF, TXT, or MD files",
        type=['pdf', 'txt', 'md'],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files and uploaded_files != st.session_state.uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        with st.spinner("Processing documents..."):
            process_uploaded_files(uploaded_files)
    
    # Chat interface
    st.subheader("💬 Chat")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show performance metrics if available
            if "metrics" in message and message["metrics"]:
                with st.expander("Performance Metrics", expanded=False):
                    metrics = message["metrics"]
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Retrieval", format_time(metrics["retrieval_time"]))
                    with col2:
                        st.metric("Generation", format_time(metrics["generation_time"]))
                    with col3:
                        st.metric("Total", format_time(metrics["total_time"]))
            
            if "sources" in message and message["sources"]:
                with st.expander("View Sources"):
                    for source in message["sources"]:
                        st.markdown(f"**From:** {source['metadata'].get('source', 'Unknown')}")
                        st.markdown(f"**Content:** {source['content']}")
    
    # Chat input
    if st.session_state.rag_pipeline is None:
        st.info("Please upload some documents first to start chatting!")
    else:
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response with performance tracking
            import time
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    start_time = time.time()
                    
                    # Track retrieval time
                    retrieval_start = time.time()
                    response = st.session_state.rag_pipeline.ask_question(prompt)
                    retrieval_end = time.time()
                    
                    if response["error"]:
                        st.error(response["answer"])
                        assistant_message = response["answer"]
                        sources = []
                        metrics = None
                    else:
                        end_time = time.time()
                        
                        # Calculate metrics
                        total_time = end_time - start_time
                        retrieval_time = retrieval_end - retrieval_start
                        generation_time = total_time - retrieval_time
                        
                        metrics = {
                            "total_time": total_time,
                            "retrieval_time": retrieval_time,
                            "generation_time": generation_time
                        }
                        
                        st.markdown(response["answer"])
                        assistant_message = response["answer"]
                        sources = response["source_documents"]
                        
                        # Display performance metrics
                        with st.expander("Performance Metrics", expanded=False):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Retrieval Time", format_time(retrieval_time))
                            with col2:
                                st.metric("Generation Time", format_time(generation_time))
                            with col3:
                                st.metric("Total Time", format_time(total_time))
                        
                        if sources:
                            with st.expander("View Sources"):
                                for source in sources:
                                    st.markdown(f"**From:** {source['metadata'].get('source', 'Unknown')}")
                                    st.markdown(f"**Content:** {source['content']}")
            
            # Add assistant message to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message,
                "sources": sources,
                "metrics": metrics
            })

with col2:
    st.subheader("📊 Chat History")
    
    if st.session_state.rag_pipeline:
        try:
            history = st.session_state.rag_pipeline.get_chat_history()
            if history:
                for entry in history[-10:]:  # Show last 10 messages
                    role = "👤 User" if entry["type"] == "human" else "🤖 Assistant"
                    st.markdown(f"**{role}:** {entry['content'][:100]}...")
            else:
                st.info("No chat history yet")
        except Exception as e:
            st.error("Could not load chat history")
    
    # System info
    st.subheader("ℹ️ System Info")
    if st.session_state.rag_pipeline:
        try:
            info = st.session_state.rag_pipeline.get_system_info()
            st.json(info)
            
            # Add performance metrics section
            st.subheader("📊 Performance Stats")
            
            # Create a simple performance test
            if st.button("Run Performance Test"):
                import time
                
                with st.spinner("Running performance test..."):
                    # Test retrieval speed
                    test_query = "test query"
                    start_time = time.time()
                    _ = st.session_state.vector_store.similarity_search(test_query, k=3)
                    retrieval_test_time = time.time() - start_time
                    
                    st.write(f"**Retrieval Speed**: {format_time(retrieval_test_time)} for 3 documents")
        except Exception as e:
            st.error("Could not load system info")

# Initialize system on startup
if st.session_state.rag_pipeline is None:
    st.session_state.vector_store.load_existing_store()
    initialize_rag_pipeline()