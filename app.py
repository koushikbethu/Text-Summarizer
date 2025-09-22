"""
Streamlit Web Interface for Text Summarization
A user-friendly web app for summarizing PDF and text files
"""

import streamlit as st
import tempfile
import os
from text_summarizer import TextSummarizer
import time

# Page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_summarizer():
    """Initialize the summarizer model"""
    if 'summarizer' not in st.session_state:
        with st.spinner("Loading AI model... This may take a moment on first run."):
            st.session_state.summarizer = TextSummarizer()
    return st.session_state.summarizer

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Text Summarizer</h1>', unsafe_allow_html=True)
    st.markdown("### Transform your documents into concise summaries using advanced AI")
    
    # Sidebar for settings
    st.sidebar.header("⚙️ Settings")
    
    # Summary length settings
    st.sidebar.subheader("Summary Length")
    max_length = st.sidebar.slider("Maximum Length", 50, 300, 150, 10)
    min_length = st.sidebar.slider("Minimum Length", 10, 100, 30, 5)
    
    # Model selection
    st.sidebar.subheader("Model Selection")
    model_choice = st.sidebar.selectbox(
        "Choose Model",
        ["facebook/bart-large-cnn", "facebook/bart-large-xsum", "google/pegasus-xsum"],
        help="BART-CNN is best for general text, BART-XSum for news, Pegasus for abstractive summaries"
    )
    
    # Initialize summarizer
    summarizer = initialize_summarizer()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h3 class="sub-header">📄 Input Options</h3>', unsafe_allow_html=True)
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["Upload File", "Paste Text"],
            horizontal=True
        )
        
        input_text = ""
        file_uploaded = None
        
        if input_method == "Upload File":
            st.markdown("**Upload a PDF or Text file:**")
            file_uploaded = st.file_uploader(
                "Choose a file",
                type=['pdf', 'txt', 'md'],
                help="Supported formats: PDF, TXT, Markdown"
            )
            
            if file_uploaded is not None:
                # Display file info
                st.success(f"✅ File uploaded: {file_uploaded.name}")
                st.info(f"📊 File size: {file_uploaded.size:,} bytes")
                
        else:
            st.markdown("**Paste your text here:**")
            input_text = st.text_area(
                "Enter text to summarize",
                height=200,
                placeholder="Paste your text here...",
                help="You can paste any text content for summarization"
            )
    
    with col2:
        st.markdown('<h3 class="sub-header">📋 Summary Output</h3>', unsafe_allow_html=True)
        
        # Summarize button
        if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
            
            if input_method == "Upload File" and file_uploaded is not None:
                # Process uploaded file
                try:
                    with st.spinner("Processing file and generating summary..."):
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_uploaded.name.split('.')[-1]}") as tmp_file:
                            tmp_file.write(file_uploaded.getvalue())
                            tmp_file_path = tmp_file.name
                        
                        # Generate summary
                        summary = summarizer.summarize_file(
                            tmp_file_path, 
                            max_length=max_length, 
                            min_length=min_length
                        )
                        
                        # Clean up temporary file
                        os.unlink(tmp_file_path)
                        
                        # Display results
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("✅ Summary generated successfully!")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown("**📝 Generated Summary:**")
                        st.write(summary)
                        
                        # Download button
                        st.download_button(
                            label="💾 Download Summary",
                            data=summary,
                            file_name=f"summary_{int(time.time())}.txt",
                            mime="text/plain"
                        )
                        
                except Exception as e:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.error(f"❌ Error processing file: {str(e)}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            elif input_method == "Paste Text" and input_text.strip():
                # Process pasted text
                try:
                    with st.spinner("Generating summary..."):
                        summary = summarizer.summarize_text(
                            input_text, 
                            max_length=max_length, 
                            min_length=min_length
                        )
                        
                        # Display results
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("✅ Summary generated successfully!")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown("**📝 Generated Summary:**")
                        st.write(summary)
                        
                        # Download button
                        st.download_button(
                            label="💾 Download Summary",
                            data=summary,
                            file_name=f"summary_{int(time.time())}.txt",
                            mime="text/plain"
                        )
                        
                except Exception as e:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    st.error(f"❌ Error generating summary: {str(e)}")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please upload a file or paste some text to summarize.")
    
    # Information section
    st.markdown("---")
    st.markdown('<h3 class="sub-header">ℹ️ About This Tool</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔧 Features:**
        - PDF text extraction
        - Multiple file formats
        - Adjustable summary length
        - High-quality AI models
        - Download summaries
        """)
    
    with col2:
        st.markdown("""
        **📚 Supported Formats:**
        - PDF documents
        - Text files (.txt)
        - Markdown files (.md)
        - Direct text input
        """)
    
    with col3:
        st.markdown("""
        **🤖 AI Models:**
        - BART-Large-CNN (default)
        - BART-Large-XSum
        - Google Pegasus
        - State-of-the-art accuracy
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-top: 2rem;'>
            <p>Built with ❤️ using Streamlit and Hugging Face Transformers</p>
            <p>Powered by advanced AI models for accurate text summarization</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
