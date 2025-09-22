import streamlit as st
import tempfile
import os
from text_summarizer import TextSummarizer

# Page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

st.title("🤖 AI Text Summarizer")
st.write("Upload a PDF/text file or paste text to get an AI-generated summary")

# Initialize summarizer
@st.cache_resource
def load_summarizer():
    with st.spinner("Loading AI model... This may take a moment on first run."):
        return TextSummarizer()

summarizer = load_summarizer()

# Sidebar for settings
st.sidebar.header("⚙️ Settings")
max_length = st.sidebar.slider("Maximum Summary Length", 50, 300, 150)
min_length = st.sidebar.slider("Minimum Summary Length", 10, 100, 30)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Input")
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["Upload File", "Paste Text"])
    
    input_text = ""
    file_uploaded = None
    
    if input_method == "Upload File":
        file_uploaded = st.file_uploader("Choose a file", type=['pdf', 'txt', 'md'])
        if file_uploaded is not None:
            st.success(f"✅ File uploaded: {file_uploaded.name}")
    else:
        input_text = st.text_area("Paste your text here:", height=200)

with col2:
    st.subheader("📋 Summary Output")
    
    if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
        if input_method == "Upload File" and file_uploaded is not None:
            try:
                with st.spinner("Processing file and generating summary..."):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_uploaded.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(file_uploaded.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Generate summary
                    summary = summarizer.process_file(tmp_file_path, max_length, min_length)
                    
                    # Clean up
                    os.unlink(tmp_file_path)
                    
                    st.success("✅ Summary generated successfully!")
                    st.write("**Generated Summary:**")
                    st.write(summary)
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                
        elif input_method == "Paste Text" and input_text.strip():
            try:
                with st.spinner("Generating summary..."):
                    summary = summarizer.process_text_input(input_text, max_length, min_length)
                    
                    st.success("✅ Summary generated successfully!")
                    st.write("**Generated Summary:**")
                    st.write(summary)
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please upload a file or paste some text to summarize.")

# Information
st.markdown("---")
st.info("💡 **Tip:** The AI model will be downloaded automatically on first use. This may take a few minutes.")
