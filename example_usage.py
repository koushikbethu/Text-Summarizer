"""
Example usage of the Text Summarizer
Demonstrates how to use the summarizer programmatically
"""

from text_summarizer import TextSummarizer
import os

def example_usage():
    """Demonstrate various ways to use the text summarizer"""
    
    print("🤖 Text Summarizer Example Usage")
    print("=" * 50)
    
    # Initialize the summarizer
    print("Loading AI model...")
    summarizer = TextSummarizer()
    print("✅ Model loaded successfully!")
    print()
    
    # Example 1: Summarize direct text
    print("📝 Example 1: Direct Text Summarization")
    print("-" * 40)
    
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
    
    The scope of AI is disputed: as machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    
    Modern machine learning techniques, particularly deep learning, have dramatically improved the performance of AI systems across many domains. These techniques have enabled AI to achieve superhuman performance in many specific tasks, such as image recognition, natural language processing, and game playing.
    """
    
    summary = summarizer.process_text_input(sample_text, max_length=100, min_length=30)
    print(f"Original text length: {len(sample_text)} characters")
    print(f"Summary length: {len(summary)} characters")
    print(f"Summary: {summary}")
    print()
    
    # Example 2: Create a sample text file and summarize it
    print("📄 Example 2: File-based Summarization")
    print("-" * 40)
    
    sample_content = """
    Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from and make predictions or decisions based on data. It has revolutionized many industries including healthcare, finance, transportation, and entertainment.
    
    There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning. Supervised learning uses labeled training data to learn a mapping from inputs to outputs. Unsupervised learning finds hidden patterns in data without labeled examples. Reinforcement learning learns through interaction with an environment and receiving rewards or penalties.
    
    Deep learning, a subset of machine learning, uses neural networks with multiple layers to model and understand complex patterns in data. It has been particularly successful in areas such as computer vision, natural language processing, and speech recognition.
    
    The future of machine learning looks promising with advances in areas such as explainable AI, federated learning, and quantum machine learning. These developments will make AI systems more transparent, privacy-preserving, and powerful.
    """
    
    # Create a temporary text file
    with open("sample_document.txt", "w", encoding="utf-8") as f:
        f.write(sample_content)
    
    try:
        summary = summarizer.process_file("sample_document.txt", max_length=120, min_length=40)
        print(f"File processed successfully!")
        print(f"Summary: {summary}")
    except Exception as e:
        print(f"Error processing file: {e}")
    finally:
        # Clean up
        if os.path.exists("sample_document.txt"):
            os.remove("sample_document.txt")
    
    print()
    
    # Example 3: Different summary lengths
    print("📏 Example 3: Different Summary Lengths")
    print("-" * 40)
    
    short_summary = summarizer.process_text_input(sample_text, max_length=50, min_length=20)
    long_summary = summarizer.process_text_input(sample_text, max_length=200, min_length=50)
    
    print(f"Short summary ({len(short_summary)} chars): {short_summary}")
    print()
    print(f"Long summary ({len(long_summary)} chars): {long_summary}")
    print()
    
    print("🎉 Examples completed successfully!")
    print("\nTo run the web interface, use: streamlit run app.py")
    print("To use from command line, use: python text_summarizer.py <input>")

if __name__ == "__main__":
    example_usage()
