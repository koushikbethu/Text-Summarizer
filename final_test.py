"""
Quick test script to verify text summarization is working
"""

from text_summarizer import TextSummarizer

def test_basic_functionality():
    print("🔍 Testing Text Summarizer...")
    
    # Initialize summarizer
    summarizer = TextSummarizer()
    
    # Test text
    test_text = """
    Climate change refers to long-term shifts in global or regional climate patterns. Since the mid-20th century, the pace of climate change has dramatically accelerated due to human activities, particularly the burning of fossil fuels, which increases heat-trapping greenhouse gas levels in Earth's atmosphere. The consequences include rising global temperatures, melting ice caps, rising sea levels, and more frequent extreme weather events. Scientists around the world agree that immediate action is required to reduce greenhouse gas emissions and transition to renewable energy sources to prevent catastrophic impacts on ecosystems and human societies.
    """
    
    print("📝 Input text length:", len(test_text.split()), "words")
    
    # Test summarization
    summary = summarizer.summarize_text(test_text, max_length=100, min_length=30)
    
    print("✅ Generated summary:", summary)
    print("📊 Summary length:", len(summary.split()), "words")
    
    # Test with direct file
    print("\n🔍 Testing file summarization...")
    
    # Create a sample text file
    with open("sample_test.txt", "w", encoding="utf-8") as f:
        f.write(test_text)
    
    file_summary = summarizer.summarize_file("sample_test.txt")
    print("✅ File summary:", file_summary)
    
    print("\n🎉 All tests completed successfully!")

if __name__ == "__main__":
    test_basic_functionality()