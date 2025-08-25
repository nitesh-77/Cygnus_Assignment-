import os
from typing import List, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.vector_store = None
        
        # Try to use Ollama embeddings first, fallback to Sentence Transformers
        try:
            self.embeddings = OllamaEmbeddings(model="mistral")
            print("Using Ollama embeddings with mistral")
        except Exception as e:
            print(f"Ollama embeddings not available, using Sentence Transformers: {e}")
            self.embeddings = SentenceTransformerEmbeddings(
                model_name="all-MiniLM-L6-v2"
            )
    
    def create_vector_store(self, documents: List[Document]) -> None:
        """Create a new vector store from documents."""
        if not documents:
            print("No documents provided to create vector store")
            return
        
        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        else:
            # Add documents to existing vector store
            self.vector_store.add_documents(documents)
        
        print(f"Vector store created with {len(documents)} document chunks")
    
    def load_existing_store(self) -> bool:
        """Load existing vector store if it exists."""
        try:
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                print("Loaded existing vector store")
                return True
        except Exception as e:
            print(f"Error loading existing vector store: {e}")
        
        return False
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents."""
        if self.vector_store is None:
            print("Vector store not initialized")
            return []
        
        return self.vector_store.similarity_search(query, k=k)
    
    def get_store_info(self) -> dict:
        """Get information about the vector store."""
        if self.vector_store is None:
            return {"status": "not_initialized", "count": 0}
        
        try:
            count = self.vector_store._collection.count()
            return {"status": "active", "count": count}
        except Exception as e:
            return {"status": "error", "count": 0, "error": str(e)}
    
    def clear_store(self) -> None:
        """Clear the vector store."""
        if self.vector_store is not None:
            try:
                self.vector_store.delete_collection()
                self.vector_store = None
                print("Vector store cleared")
            except Exception as e:
                print(f"Error clearing vector store: {e}")
        
        # Remove the persist directory
        import shutil
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)