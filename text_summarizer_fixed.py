"""
Simplified Text Summarization for Python 3.13 compatibility
A working version that handles the import issues gracefully
"""

import os
import re
from typing import List, Optional, Union
import PyPDF2
import pdfplumber
import nltk
from nltk.tokenize import sent_tokenize

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
    """Simplified Text Summarizer with better Python 3.13 compatibility"""
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """Initialize the summarizer"""
        self.model_name = model_name
        self.summarizer_pipeline = None
        self._load_model()
        
    def _load_model(self):
        """Load the model with better error handling"""
        try:
            # Import here to avoid immediate import issues
            from transformers import pipeline
            
            self.summarizer_pipeline = pipeline(
                "summarization",
                model=self.model_name,
                device=-1  # Force CPU to avoid CUDA issues
            )
            print(f"✅ Model {self.model_name} loaded successfully")
            
        except Exception as e:
            print(f"⚠️ Failed to load transformers model: {e}")
            print("📝 Using fallback extractive summarization")
            self.summarizer_pipeline = None
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        
        # Method 1: Using pdfplumber
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        # Method 2: Fallback to PyPDF2
        if not text.strip():
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"PyPDF2 also failed: {e}")
        
        return text.strip()
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:]', ' ', text)
        
        # Remove multiple dots
        text = re.sub(r'\.{2,}', '.', text)
        
        return text.strip()
    
    def extractive_summarization(self, text: str, num_sentences: int = 3) -> str:
        """Simple extractive summarization as fallback"""
        sentences = sent_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text
        
        # Simple scoring: prefer sentences with more words (basic heuristic)
        sentence_scores = []
        for sentence in sentences:
            words = len(sentence.split())
            # Avoid very short or very long sentences
            if 10 <= words <= 50:
                score = words
            else:
                score = words * 0.5
            sentence_scores.append((sentence, score))
        
        # Sort by score and take top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [sent[0] for sent in sentence_scores[:num_sentences]]
        
        # Reorder sentences by their original position
        summary_sentences = []
        for sentence in sentences:
            if sentence in top_sentences:
                summary_sentences.append(sentence)
        
        return ' '.join(summary_sentences)
    
    def chunk_text(self, text: str, max_chunk_size: int = 512) -> List[str]:
        """Split text into smaller chunks for processing"""
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Rough word count estimation
            if len((current_chunk + sentence).split()) <= max_chunk_size:
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
        Summarize text using either transformers or extractive method
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Summary text
        """
        if not text.strip():
            return "No text provided for summarization."
        
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        if len(cleaned_text.split()) < 50:
            return "Text too short to summarize meaningfully."
        
        try:
            if self.summarizer_pipeline:
                # Use transformers model
                chunks = self.chunk_text(cleaned_text, 400)  # Smaller chunks for stability
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
                        print(f"⚠️ Error summarizing chunk: {e}")
                        # Fallback to extractive for this chunk
                        summaries.append(self.extractive_summarization(chunk, 2))
                
                return ' '.join(summaries)
            
            else:
                # Use extractive summarization
                num_sentences = max(3, len(sent_tokenize(cleaned_text)) // 10)
                return self.extractive_summarization(cleaned_text, num_sentences)
                
        except Exception as e:
            print(f"❌ Summarization failed: {e}")
            # Ultimate fallback
            return self.extractive_summarization(cleaned_text, 3)
    
    def summarize_file(self, file_path: str, **kwargs) -> str:
        """
        Summarize content from a file
        
        Args:
            file_path: Path to the file (.pdf, .txt, .md)
            **kwargs: Additional arguments for summarization
            
        Returns:
            Summary text
        """
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                text = self.extract_text_from_pdf(file_path)
            elif file_extension in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            else:
                return f"Unsupported file format: {file_extension}"
            
            if not text.strip():
                return "No text could be extracted from the file."
            
            return self.summarize_text(text, **kwargs)
            
        except Exception as e:
            return f"Error processing file: {str(e)}"


# Simple test function
def test_summarizer():
    """Test the summarizer with sample text"""
    summarizer = TextSummarizer()
    
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".

    The scope of AI is disputed: as machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology. Modern machine capabilities generally classified as AI include successfully understanding human speech, competing at the highest level in strategic game systems, autonomously operating cars, intelligent routing in content delivery networks, and military simulations.
    """
    
    summary = summarizer.summarize_text(sample_text)
    print(f"📝 Summary: {summary}")
    return summary


if __name__ == "__main__":
    test_summarizer()