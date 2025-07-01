# app/rag/loaders.py

import os
from typing import List, Dict, Any
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
import logging

logger = logging.getLogger(__name__)

class DocumentLoader:
    """Handles loading and preprocessing of documents for RAG."""
    
    def __init__(self, supported_text_formats: List[str] = None, 
                 supported_pdf_formats: List[str] = None):
        self.supported_text_formats = supported_text_formats or ['.txt']
        self.supported_pdf_formats = supported_pdf_formats or ['.pdf']
    
    def load_documents_from_directory(self, directory_path: str, 
                                    file_types: List[str] = None) -> List:
        """
        Load all supported documents from a directory.
        
        Args:
            directory_path: Path to directory
            file_types: List of file extensions to load (e.g., ['.txt', '.pdf'])
            
        Returns:
            List of loaded documents
        """
        if not os.path.exists(directory_path):
            logger.warning(f"Directory does not exist: {directory_path}")
            return []
        
        documents = []
        file_types = file_types or (self.supported_text_formats + self.supported_pdf_formats)
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext in file_types:
                try:
                    if file_ext in self.supported_text_formats:
                        docs = self._load_text_document(file_path)
                    elif file_ext in self.supported_pdf_formats:
                        docs = self._load_pdf_document(file_path)
                    else:
                        continue
                    
                    documents.extend(docs)
                    logger.info(f"Successfully loaded {filename}")
                    
                except Exception as e:
                    logger.error(f"Error loading {filename}: {str(e)}")
        
        return documents
    
    def _load_text_document(self, file_path: str) -> List:
        """Load a text document."""
        loader = TextLoader(file_path)
        return loader.load()
    
    def _load_pdf_document(self, file_path: str) -> List:
        """Load a PDF document."""
        loader = PyMuPDFLoader(file_path)
        return loader.load()
    
    def get_document_metadata(self, documents: List) -> Dict[str, Any]:
        """
        Extract metadata from loaded documents.
        
        Args:
            documents: List of loaded documents
            
        Returns:
            Dictionary containing metadata
        """
        if not documents:
            return {}
        
        total_docs = len(documents)
        total_chars = sum(len(doc.page_content) for doc in documents)
        avg_chars = total_chars / total_docs if total_docs > 0 else 0
        
        return {
            'total_documents': total_docs,
            'total_characters': total_chars,
            'average_characters_per_document': avg_chars,
            'document_sources': list(set(doc.metadata.get('source', 'unknown') for doc in documents))
        }