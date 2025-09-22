import streamlit as st

st.title("🤖 AI Text Summarizer - Test")
st.write("If you can see this, Streamlit is working!")

# Simple test
text = st.text_area("Enter some text to test:")
if st.button("Test"):
    st.write(f"You entered: {text}")
    st.success("✅ Streamlit is working correctly!")
