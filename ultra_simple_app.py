import streamlit as st
import re

# Page configuration
st.set_page_config(
    page_title="Ultra Simple Summarizer",
    page_icon="📝",
    layout="wide"
)

st.title("⚡ Ultra Simple Text Summarizer")
st.write("No downloads required - works instantly!")

def simple_summarize(text, num_sentences=3):
    """
    Ultra simple summarization using basic sentence splitting
    """
    # Split into sentences using basic punctuation
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= num_sentences:
        return text
    
    # Simple scoring based on word count and position
    sentence_scores = []
    for i, sentence in enumerate(sentences):
        # Score based on length and position (first sentences are more important)
        score = len(sentence.split()) + (len(sentences) - i) * 0.1
        sentence_scores.append((sentence, score))
    
    # Sort by score and take top sentences
    sentence_scores.sort(key=lambda x: x[1], reverse=True)
    top_sentences = [sent[0] for sent in sentence_scores[:num_sentences]]
    
    # Maintain original order
    summary = []
    for sentence in sentences:
        if sentence in top_sentences:
            summary.append(sentence)
    
    return '. '.join(summary) + '.'

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Input Text")
    
    # Sample text
    sample_text = """Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of intelligent agents: any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. The scope of AI is disputed: as machines become increasingly capable, tasks considered to require intelligence are often removed from the definition of AI, a phenomenon known as the AI effect. Modern machine learning techniques, particularly deep learning, have dramatically improved the performance of AI systems across many domains. These techniques have enabled AI to achieve superhuman performance in many specific tasks, such as image recognition, natural language processing, and game playing. The future of AI looks promising with advances in areas such as explainable AI, federated learning, and quantum machine learning."""
    
    input_text = st.text_area("Paste your text here:", height=300, value=sample_text)

with col2:
    st.subheader("📋 Summary Output")
    
    # Settings
    num_sentences = st.slider("Number of sentences in summary:", 1, 10, 3)
    
    if st.button("⚡ Generate Summary", type="primary", use_container_width=True):
        if input_text.strip():
            try:
                summary = simple_summarize(input_text, num_sentences)
                
                st.success("✅ Summary generated successfully!")
                st.write("**Generated Summary:**")
                st.write(summary)
                
                # Show stats
                original_sentences = len(re.split(r'[.!?]+', input_text))
                summary_sentences = len(re.split(r'[.!?]+', summary))
                compression_ratio = (1 - len(summary) / len(input_text)) * 100
                
                st.info(f"📊 Original: {original_sentences} sentences, {len(input_text)} chars")
                st.info(f"📊 Summary: {summary_sentences} sentences, {len(summary)} chars")
                st.info(f"📊 Compression: {compression_ratio:.1f}% reduction")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please paste some text to summarize.")

# Information
st.markdown("---")
st.success("🎉 **This version works instantly with no downloads!**")
st.info("💡 **Tip:** This is a basic extractive summarizer. For AI-powered summaries, wait for the model downloads on other ports to complete.")

# Show available apps
st.markdown("### 🌐 Available Applications:")
st.markdown("""
- **Port 8504**: Full AI Summarizer (downloading 1.63GB model... 14% complete)
- **Port 8505**: Fast AI Summarizer (downloading model...)
- **Port 8506**: Instant Summarizer (downloading NLTK data...)
- **Current**: Ultra Simple Summarizer ✅ **WORKING NOW**
""")
