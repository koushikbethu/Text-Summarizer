import streamlit as st
import tempfile
import os
from text_summarizer import TextSummarizer

# Page configuration
st.set_page_config(
    page_title="AI Text Summarizer - Fast",
    page_icon="📝",
    layout="wide"
)

st.title("🤖 AI Text Summarizer - Fast Version")
st.write("Using a smaller, faster model for quick summaries")

# Initialize summarizer with a smaller model
@st.cache_resource
def load_summarizer():
    with st.spinner("Loading fast AI model..."):
        # Use a smaller model for faster loading
        return TextSummarizer(model_name="facebook/bart-large-cnn")

summarizer = load_summarizer()

# Settings
st.sidebar.header("⚙️ Settings")
max_length = st.sidebar.slider("Maximum Summary Length", 50, 200, 100)
min_length = st.sidebar.slider("Minimum Summary Length", 10, 50, 20)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Input")
    
    # Simple text input for now
    input_text = st.text_area("Paste your text here:", height=300, 
                             placeholder="Paste any text you want to summarize...")

with col2:
    st.subheader("📋 Summary Output")
    
    if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
        if input_text.strip():
            try:
                with st.spinner("Generating summary..."):
                    summary = summarizer.process_text_input(input_text, max_length, min_length)
                    
                    st.success("✅ Summary generated successfully!")
                    st.write("**Generated Summary:**")
                    st.write(summary)
                    
                    # Show stats
                    st.info(f"📊 Original: {len(input_text)} chars → Summary: {len(summary)} chars")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.write("The model might still be loading. Please wait a moment and try again.")
        else:
            st.warning("⚠️ Please paste some text to summarize.")

# Sample text for testing
st.markdown("---")
st.subheader("🧪 Try with Sample Text")
sample_text = """
Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. 

The scope of AI is disputed: as machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. Modern machine learning techniques, particularly deep learning, have dramatically improved the performance of AI systems across many domains.

These techniques have enabled AI to achieve superhuman performance in many specific tasks, such as image recognition, natural language processing, and game playing. The future of AI looks promising with advances in areas such as explainable AI, federated learning, and quantum machine learning.
"""

if st.button("📝 Use Sample Text"):
    st.session_state.sample_text = sample_text
    st.rerun()

if 'sample_text' in st.session_state:
    st.text_area("Sample text loaded:", value=st.session_state.sample_text, height=200)

st.info("💡 **Note:** The AI model is downloading in the background. If you see errors, wait a few minutes for the download to complete.")
