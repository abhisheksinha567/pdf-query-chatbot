import streamlit as st
from PyPDF2 import PdfReader
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to extract text from uploaded PDFs
def extract_text_from_pdfs(pdfs):
    text = ""
    for pdf in pdfs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to get the response from the language model
def get_response_from_llm(context, question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Context: {context}\n\nQuestion: {question}\n\nAnswer:",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit app layout
def main():
    st.title("PDF Query Chatbot")

    # File uploader for PDFs
    uploaded_pdfs = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

    # Text input for the user's question
    user_question = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        if uploaded_pdfs and user_question:
            with st.spinner("Extracting text from PDFs..."):
                context = extract_text_from_pdfs(uploaded_pdfs)
            with st.spinner("Getting response from the model..."):
                answer = get_response_from_llm(context, user_question)
            st.write("Answer:", answer)
        else:
            st.error("Please upload PDF files and enter a question.")

if __name__ == "__main__":
    main()
