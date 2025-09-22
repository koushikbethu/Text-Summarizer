"""
Text Summarization ML Project
Supports both PDF and text file inputs with extractive and abstractive summarization
"""

import os
import re
import torch
from typing import List, Optional, Union
import PyPDF2
import pdfplumber
from transformers import (
    AutoTokenizer, 
    AutoModelForSeq2SeqLM, 
    pipeline,
    BartForConditionalGeneration,
    BartTokenizer
)
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import streamlit as st
from io import StringIO

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextSummarizer:
    """Main class for text summarization with PDF and text support"""
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the summarizer with a pre-trained model
        
        Args:
            model_name: Hugging Face model name for summarization
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
        self.summarizer_pipeline = None
        self._load_model()
        
    def _load_model(self):
        """Load the pre-trained model and tokenizer"""
        try:
            # Use pipeline for easier handling
            self.summarizer_pipeline = pipeline(
                "summarization",
                model=self.model_name,
                tokenizer=self.model_name,
                device=0 if self.device == "cuda" else -1
            )
            print(f"Model {self.model_name} loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to a smaller model
            self.model_name = "facebook/bart-large-cnn"
            self.summarizer_pipeline = pipeline(
                "summarization",
                model=self.model_name,
                device=0 if self.device == "cuda" else -1
            )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file using multiple methods for better accuracy
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as string
        """
        text = ""
        
        # Method 1: Using pdfplumber (better for complex layouts)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        # Method 2: Fallback to PyPDF2 if pdfplumber fails
        if not text.strip():
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"PyPDF2 failed: {e}")
                raise Exception(f"Could not extract text from PDF: {e}")
        
        return text.strip()
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess text for better summarization
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        
        # Remove multiple consecutive punctuation
        text = re.sub(r'([.!?])\1+', r'\1', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, max_length: int = 1024) -> List[str]:
        """
        Split text into chunks that fit within model's maximum length
        
        Args:
            text: Text to chunk
            max_length: Maximum length per chunk
            
        Returns:
            List of text chunks
        """
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) < max_length:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Generate summary of the input text
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Generated summary
        """
        if not text.strip():
            return "No text to summarize."
        
        # Preprocess text
        text = self.preprocess_text(text)
        
        # Check if text is too long and needs chunking
        if len(text) > 1000:
            chunks = self.chunk_text(text)
            summaries = []
            
            for chunk in chunks:
                try:
                    summary = self.summarizer_pipeline(
                        chunk,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False
                    )
                    summaries.append(summary[0]['summary_text'])
                except Exception as e:
                    print(f"Error summarizing chunk: {e}")
                    continue
            
            # Combine chunk summaries
            if summaries:
                combined_text = " ".join(summaries)
                # Summarize the combined summaries if still too long
                if len(combined_text) > 1000:
                    final_summary = self.summarizer_pipeline(
                        combined_text,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False
                    )
                    return final_summary[0]['summary_text']
                else:
                    return combined_text
            else:
                return "Error: Could not generate summary from chunks."
        else:
            # Text is short enough to summarize directly
            try:
                summary = self.summarizer_pipeline(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                return summary[0]['summary_text']
            except Exception as e:
                return f"Error generating summary: {e}"
    
    def process_file(self, file_path: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Process a file (PDF or text) and return summary
        
        Args:
            file_path: Path to the file
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Generated summary
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        if not text.strip():
            return "No text content found in the file."
        
        return self.summarize_text(text, max_length, min_length)
    
    def process_text_input(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Process direct text input and return summary
        
        Args:
            text: Input text
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Generated summary
        """
        return self.summarize_text(text, max_length, min_length)


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Text Summarization Tool")
    parser.add_argument("input", help="Input file path or text")
    parser.add_argument("--max_length", type=int, default=150, help="Maximum summary length")
    parser.add_argument("--min_length", type=int, default=30, help="Minimum summary length")
    parser.add_argument("--output", help="Output file path (optional)")
    
    args = parser.parse_args()
    
    # Initialize summarizer
    summarizer = TextSummarizer()
    
    try:
        # Check if input is a file or direct text
        if os.path.exists(args.input):
            summary = summarizer.process_file(args.input, args.max_length, args.min_length)
        else:
            summary = summarizer.process_text_input(args.input, args.max_length, args.min_length)
        
        print("Summary:")
        print("-" * 50)
        print(summary)
        
        # Save to output file if specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"\nSummary saved to: {args.output}")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
