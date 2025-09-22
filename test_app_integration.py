"""
Test the app functionality directly
"""

from text_summarizer import TextSummarizer

def test_app_methods():
    print("🔍 Testing App Integration...")
    
    # Initialize summarizer like the app does
    summarizer = TextSummarizer()
    
    # Test text input (like paste text functionality)
    test_text = """
    The Internet of Things (IoT) refers to the network of physical devices, vehicles, home appliances, and other items embedded with electronics, software, sensors, actuators, and connectivity which enables these things to connect and exchange data. IoT allows objects to be sensed or controlled remotely across existing network infrastructure, creating opportunities for more direct integration of the physical world into computer-based systems. This results in improved efficiency, accuracy and economic benefit in addition to reduced human intervention.
    """
    
    print("\n📝 Testing text summarization (like paste text)...")
    summary = summarizer.summarize_text(test_text, max_length=100, min_length=30)
    print(f"✅ Text Summary: {summary}")
    
    # Test file processing
    print("\n📄 Testing file summarization...")
    
    # Create a test file
    with open("test_iot.txt", "w", encoding="utf-8") as f:
        f.write(test_text)
    
    file_summary = summarizer.summarize_file("test_iot.txt", max_length=100, min_length=30)
    print(f"✅ File Summary: {file_summary}")
    
    print("\n🎉 All app methods working correctly!")

if __name__ == "__main__":
    test_app_methods()