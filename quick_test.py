"""
Quick command-line test of the text summarizer
"""

from text_summarizer import TextSummarizer

def main():
    print("🤖 AI Text Summarizer - Quick Test")
    print("=" * 50)
    
    # Sample text for testing
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. 
    
    The scope of AI is disputed: as machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. Modern machine learning techniques, particularly deep learning, have dramatically improved the performance of AI systems across many domains.
    
    These techniques have enabled AI to achieve superhuman performance in many specific tasks, such as image recognition, natural language processing, and game playing. The future of AI looks promising with advances in areas such as explainable AI, federated learning, and quantum machine learning.
    """
    
    print("Loading AI model...")
    try:
        summarizer = TextSummarizer()
        print("✅ Model loaded successfully!")
        
        print("\n📝 Original Text:")
        print("-" * 30)
        print(sample_text[:200] + "..." if len(sample_text) > 200 else sample_text)
        
        print(f"\n📊 Original length: {len(sample_text)} characters")
        
        print("\n🔄 Generating summary...")
        summary = summarizer.process_text_input(sample_text, max_length=100, min_length=30)
        
        print("\n📋 Generated Summary:")
        print("-" * 30)
        print(summary)
        print(f"\n📊 Summary length: {len(summary)} characters")
        
        print("\n🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("The model might still be downloading. Please wait and try again.")

if __name__ == "__main__":
    main()
