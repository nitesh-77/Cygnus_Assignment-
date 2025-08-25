from typing import List, Dict, Optional
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import json

class RAGPipeline:
    def __init__(self, vector_store, model_name: str = "mistral"):
        self.vector_store = vector_store
        self.model_name = model_name
        self.llm = None
        self.memory = None
        self.qa_chain = None
        
        self._initialize_llm()
        self._setup_memory()
        self._setup_qa_chain()
    
    def _initialize_llm(self) -> None:
        """Initialize the language model."""
        try:
            self.llm = ChatOllama(model=self.model_name, temperature=0.7)
            print(f"Successfully initialized LLM: {self.model_name}")
        except Exception as e:
            print(f"Error initializing LLM {self.model_name}: {e}")
            raise e
    
    def _setup_memory(self) -> None:
        """Setup conversation memory."""
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    
    def _setup_qa_chain(self) -> None:
        """Setup the QA chain with retrieval."""
        if self.vector_store.vector_store is None:
            print("Vector store not initialized. Cannot setup QA chain.")
            return
        
        # Define the prompt template
        prompt_template = """You are a helpful AI assistant that answers questions based on provided context.
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Helpful Answer:"""
        
        PROMPT = ChatPromptTemplate.from_template(prompt_template)
        
        try:
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store.vector_store.as_retriever(
                    search_kwargs={"k": 4}
                ),
                memory=self.memory,
                return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": PROMPT}
            )
            print("QA chain setup complete")
        except Exception as e:
            print(f"Error setting up QA chain: {e}")
    
    def ask_question(self, question: str) -> Dict[str, any]:
        """Ask a question and get an answer with sources."""
        if self.qa_chain is None:
            return {
                "answer": "System not ready. Please upload documents first.",
                "source_documents": [],
                "error": True
            }
        
        try:
            result = self.qa_chain({"question": question})
            
            # Extract source information
            sources = []
            for doc in result.get("source_documents", []):
                sources.append({
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                })
            
            return {
                "answer": result["answer"],
                "source_documents": sources,
                "error": False
            }
        except Exception as e:
            return {
                "answer": f"Error processing question: {str(e)}",
                "source_documents": [],
                "error": True
            }
    
    def clear_memory(self) -> None:
        """Clear conversation memory."""
        if self.memory:
            self.memory.clear()
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the current chat history."""
        if self.memory is None:
            return []
        
        try:
            messages = self.memory.chat_memory.messages
            history = []
            for message in messages:
                history.append({
                    "type": message.type,
                    "content": message.content
                })
            return history
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    def get_system_info(self) -> Dict[str, any]:
        """Get system status information."""
        vector_info = self.vector_store.get_store_info()
        
        return {
            "model_name": self.model_name,
            "vector_store_status": vector_info["status"],
            "document_count": vector_info.get("count", 0),
            "memory_initialized": self.memory is not None,
            "qa_chain_initialized": self.qa_chain is not None
        }