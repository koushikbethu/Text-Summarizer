import streamlit as st
import re
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Page configuration
st.set_page_config(
    page_title="Instant Text Summarizer",
    page_icon="📝",
    layout="wide"
)

st.title("⚡ Instant Text Summarizer")
st.write("Quick extractive summarization - no AI model download required!")

def extractive_summarize(text, num_sentences=3):
    """
    Simple extractive summarization using sentence scoring
    """
    # Clean and tokenize
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
    
    # Remove stopwords and get word frequencies
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(words)
    
    # Score sentences
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        sentence_words = [word for word in sentence_words if word.isalnum() and word not in stop_words]
        score = sum(word_freq[word] for word in sentence_words)
        sentence_scores[sentence] = score
    
    # Get top sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    summary_sentences = [sent[0] for sent in top_sentences]
    
    # Maintain original order
    summary = []
    for sentence in sentences:
        if sentence in summary_sentences:
            summary.append(sentence)
    
    return ' '.join(summary)

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Input Text")
    
    # Sample text
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. 
    
    The scope of AI is disputed: as machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. Modern machine learning techniques, particularly deep learning, have dramatically improved the performance of AI systems across many domains.
    
    These techniques have enabled AI to achieve superhuman performance in many specific tasks, such as image recognition, natural language processing, and game playing. The future of AI looks promising with advances in areas such as explainable AI, federated learning, and quantum machine learning.
    """
    
    input_text = st.text_area("Paste your text here:", height=300, value=sample_text)
    
    if st.button("📝 Use Sample Text"):
        st.rerun()

with col2:
    st.subheader("📋 Summary Output")
    
    # Settings
    num_sentences = st.slider("Number of sentences in summary:", 1, 10, 3)
    
    if st.button("⚡ Generate Summary", type="primary", use_container_width=True):
        if input_text.strip():
            try:
                with st.spinner("Generating summary..."):
                    summary = extractive_summarize(input_text, num_sentences)
                    
                    st.success("✅ Summary generated successfully!")
                    st.write("**Generated Summary:**")
                    st.write(summary)
                    
                    # Show stats
                    original_sentences = len(sent_tokenize(input_text))
                    summary_sentences = len(sent_tokenize(summary))
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
st.info("💡 **This is an extractive summarizer that works instantly!** It selects the most important sentences based on word frequency. For AI-powered abstractive summaries, wait for the model download to complete on the other ports.")

# Show available apps
st.markdown("### 🌐 Available Applications:")
st.markdown("""
- **Port 8504**: Full AI Summarizer (downloading model...)
- **Port 8505**: Fast AI Summarizer (downloading model...)
- **Current**: Instant Extractive Summarizer ✅
""")
