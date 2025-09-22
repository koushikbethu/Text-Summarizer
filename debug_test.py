"""
Debug script to test TextSummarizer functionality
"""
import sys
import traceback
from text_summarizer import TextSummarizer

def test_summarizer():
    print("🔧 Testing TextSummarizer...")
    
    try:
        # Initialize the summarizer
        print("1. Initializing TextSummarizer...")
        summarizer = TextSummarizer()
        print("✅ TextSummarizer initialized successfully")
        
        # Test with simple text
        test_text = """
        Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
        """
        
        print("2. Testing text summarization...")
        summary = summarizer.summarize_text(test_text)
        print(f"✅ Summary generated: {summary[:100]}..." if summary else "❌ No summary generated")
        
        return summary is not None and len(summary) > 0
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print(f"📝 Full traceback:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_summarizer()
    print(f"\n🎯 Test result: {'PASSED' if success else 'FAILED'}")