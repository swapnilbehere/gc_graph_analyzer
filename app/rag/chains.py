# app/rag/chains.py

import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import logging

logger = logging.getLogger(__name__)

class RAGChainManager:
    """Manages RAG chains for chromatogram analysis."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
    
    def create_diagnosis_chain(self, txt_output_dir: str):
        """
        Create RAG chain for chromatogram diagnosis.
        
        Args:
            txt_output_dir: Directory containing reference chromatogram text files
            
        Returns:
            RAG chain for diagnosis
        """
        try:
            # Load reference documents
            documents = self._load_text_documents(txt_output_dir)
            splits = self.text_splitter.split_documents(documents)
            
            # Create vector store
            vectorstore = FAISS.from_documents(splits, self.embeddings)
            retriever = vectorstore.as_retriever()
            
            # Create prompt template
            prompt = ChatPromptTemplate.from_template("""
You are an expert chromatograph analyzer. Use this context of reference chromatograms to compare with a new chromatograph and diagnose issues.

<context>
{context}
</context>

Metadata:
{metadata}

Chromatograph Data:
{input}

Give a brief, clear diagnosis of any errors found.
""")
            
            # Create chain
            combine_chain = create_stuff_documents_chain(self.llm, prompt)
            rag_chain = create_retrieval_chain(retriever, combine_chain)
            
            return rag_chain
            
        except Exception as e:
            logger.error(f"Error creating diagnosis chain: {str(e)}")
            raise
    
    def create_troubleshooting_chain(self, knowledge_base_dir: str):
        """
        Create RAG chain for troubleshooting advice.
        
        Args:
            knowledge_base_dir: Directory containing troubleshooting documents
            
        Returns:
            RAG chain for troubleshooting
        """
        try:
            # Load PDF documents
            documents = self._load_pdf_documents(knowledge_base_dir)
            splits = self.text_splitter.split_documents(documents)
            
            # Create vector store
            vectorstore = FAISS.from_documents(splits, self.embeddings)
            retriever = vectorstore.as_retriever()
            
            # Create prompt template
            prompt = ChatPromptTemplate.from_template("""
You are a chromatography troubleshooting expert.

<context>
{context}
</context>

Diagnosis Report:
{input}

Provide a concise explanation of what may have caused these issues and how to resolve them.
""")
            
            # Create chain
            combine_chain = create_stuff_documents_chain(self.llm, prompt)
            rag_chain = create_retrieval_chain(retriever, combine_chain)
            
            return rag_chain
            
        except Exception as e:
            logger.error(f"Error creating troubleshooting chain: {str(e)}")
            raise
    
    def _load_text_documents(self, txt_dir: str) -> List:
        """Load text documents from directory."""
        from langchain_community.document_loaders import TextLoader
        
        documents = []
        for filename in os.listdir(txt_dir):
            if filename.endswith(".txt"):
                try:
                    loader = TextLoader(os.path.join(txt_dir, filename))
                    documents.extend(loader.load())
                except Exception as e:
                    logger.warning(f"Error loading {filename}: {str(e)}")
        
        return documents
    
    def _load_pdf_documents(self, pdf_dir: str) -> List:
        """Load PDF documents from directory."""
        from langchain_community.document_loaders import PyMuPDFLoader
        
        documents = []
        for filename in os.listdir(pdf_dir):
            if filename.endswith(".pdf"):
                try:
                    loader = PyMuPDFLoader(os.path.join(pdf_dir, filename))
                    documents.extend(loader.load())
                except Exception as e:
                    logger.warning(f"Error loading {filename}: {str(e)}")
        
        return documents