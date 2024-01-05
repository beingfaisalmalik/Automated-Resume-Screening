import streamlit as st
import PyPDF2
import docx2txt
import io

import google.generativeai as genai

genai.configure(api_key="API-KEY")

## Function to load OpenAI model and get responses
def get_gemini_response(input_prompt, input, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_prompt, input, prompt])
    return response.text

# Function to extract text from PDF file
def extract_text_from_pdf(pdf_file):
    with pdf_file as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num] 
            text += page.extract_text()
        return text

# Function to extract text from DOCX file
def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

text_inputs = []

# Main function to create the Streamlit app
def main():
    # Set page title and favicon
    st.set_page_config(
        page_title="Text Extraction App",
        page_icon="✒️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Add a custom background color and padding
    st.markdown(
        """
        <style>
            body {
                background-color: #f4f4f4;
                padding: 20px;
                font-family: 'Arial', sans-serif;
            }
            h1 {
                color: #3498DB;
            }
            .text-area {
                margin-top: 20px;
                background-color: #FFFFFF;
                color: #333333;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }
            #submitButton {
                background-color: #3498DB;
                color: #ECF0F1;
                font-weight: bold;
                padding: 10px 20px;
                cursor: pointer;
                margin-top: 20px;
            }
            #submitButton:hover {
                background-color: #2980B9;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header with a title
    st.title("Automated Resume Screening")
    st.markdown("Upload multiple PDF and DOCX files for Automated Screening.")

    # Input prompt
    

    # File uploader widget
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx"], accept_multiple_files=True)

    # Process uploaded files
    if uploaded_files:
        for i, file in enumerate(uploaded_files):
            file_extension = file.name.split(".")[-1].lower()

            # Extract text based on file type
            if file_extension == "pdf":
                text = extract_text_from_pdf(file)
            elif file_extension == "docx":
                text = extract_text_from_docx(io.BytesIO(file.read()))
                text_inputs.append(text)                
            else:
                text = "Unsupported file format."
                text_inputs.append(text)   

            # Display extracted text with a colorful box
            st.subheader(f"Text extracted from {file.name}:")
            st.markdown(f'<div class="text-area">{text}</div>', unsafe_allow_html=True)

    # Submit button
    input = st.text_input("Input Prompt:", key="input")
    submit = st.button("Tell me about the resumes", key="submitButton")

    input_prompt = """
                You are an expert in understanding resumes.
                You will receive a single string where ||| is the separator. Each line after this separator represents a resume detail.
                You will have to answer questions based on the input data.
                """

    ## If ask button is clicked
    separator = "|||"
    inputs = separator.join(text_inputs)
    if submit:
        response = get_gemini_response(input_prompt, inputs, input)
        st.subheader("The Response is")
        st.markdown(f'<div class="text-area">{response}</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
