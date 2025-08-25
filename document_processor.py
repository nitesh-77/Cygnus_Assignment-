import os
from typing import List, Dict
from pathlib import Path
import pypdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """Load and process PDF files."""
        documents = []
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    text += page.extract_text() + "\n"
                
                # Split into chunks
                chunks = self.text_splitter.split_text(text)
                
                for i, chunk in enumerate(chunks):
                    documents.append(Document(
                        page_content=chunk,
                        metadata={
                            "source": file_path,
                            "type": "pdf",
                            "chunk": i,
                            "total_chunks": len(chunks)
                        }
                    ))
        except Exception as e:
            print(f"Error loading PDF {file_path}: {str(e)}")
        
        return documents
    
    def load_txt(self, file_path: str) -> List[Document]:
        """Load and process TXT files."""
        documents = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
                # Split into chunks
                chunks = self.text_splitter.split_text(text)
                
                for i, chunk in enumerate(chunks):
                    documents.append(Document(
                        page_content=chunk,
                        metadata={
                            "source": file_path,
                            "type": "txt",
                            "chunk": i,
                            "total_chunks": len(chunks)
                        }
                    ))
        except Exception as e:
            print(f"Error loading TXT {file_path}: {str(e)}")
        
        return documents
    
    def load_md(self, file_path: str) -> List[Document]:
        """Load and process Markdown files."""
        documents = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
                # Split into chunks
                chunks = self.text_splitter.split_text(text)
                
                for i, chunk in enumerate(chunks):
                    documents.append(Document(
                        page_content=chunk,
                        metadata={
                            "source": file_path,
                            "type": "markdown",
                            "chunk": i,
                            "total_chunks": len(chunks)
                        }
                    ))
        except Exception as e:
            print(f"Error loading Markdown {file_path}: {str(e)}")
        
        return documents
    
    def process_file(self, file_path: str) -> List[Document]:
        """Process a file based on its extension."""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.load_pdf(file_path)
        elif file_extension == '.txt':
            return self.load_txt(file_path)
        elif file_extension == '.md':
            return self.load_md(file_path)
        else:
            print(f"Unsupported file type: {file_extension}")
            return []
    
    def process_directory(self, directory_path: str) -> List[Document]:
        """Process all supported files in a directory."""
        documents = []
        
        for file_path in Path(directory_path).glob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.md']:
                print(f"Processing: {file_path}")
                documents.extend(self.process_file(str(file_path)))
        
        return documents