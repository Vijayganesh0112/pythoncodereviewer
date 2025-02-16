import streamlit as st
import google.generativeai as genai
import os

# Load the API key from Streamlit's environment variable set in the secrets management
api_key = os.getenv('GENAI_API_KEY')
genai.configure(api_key=api_key)

# Configure the Gemini AI model
code_review_model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-exp")

st.set_page_config(page_title="AI Code Reviewer", layout="wide")

# Custom CSS for Matrix background, title margin, and styling adjustments
st.markdown(
    """
    <style>
    /* Targeting the main body of the app for the background and central alignment */
    html, body, .block-container {
        height: 100%;
        margin: 0 auto;  /* Centering the block container */
        padding: 0;
        background-image: url('https://link_to_your_image.jpg');  /* Ensure this URL is correct and accessible */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #00ff41; /* Matrix green text for visibility */
        max-width: 80%;  /* Reducing the maximum width by 20% */
    }

    /* Custom margin for the title to prevent cutting off */
    .st-bf {
        margin-top: 20px;  /* Add more space above the title */
    }

    /* Ensuring text and input fields are visibly styled against the background */
    .stTextInput, .stTextArea, .stFileUploader, .stButton {
        background-color: rgba(0,0,0,0.8); /* Semi-transparent black for input fields and buttons */
        color: #00ff41; /* Matrix green text */
        border: 1px solid #00ff41;
        font-size: 30px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Adding a LinkedIn link at the top
st.markdown("""
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/vijay-ganesh-071756249/)
    ## Welcome!
    Submit your Python code for an AI-driven review. You can either paste your code directly 
    in the input area below or upload a Python file to get started.
""", unsafe_allow_html=True)

st.title("AI-Powered Python Code Reviewer")

# Single column layout for inputs
code_input = st.text_area("Paste your Python code here:", height=250)

uploaded_file = st.file_uploader("Or upload a Python file (.py):", type=['py'])
if uploaded_file is not None:
    # Reading the contents of the uploaded Python file
    code_from_file = uploaded_file.read().decode("utf-8")
    code_input = code_from_file  # Set the file content as input for review

if st.button('Review Code'):
    if code_input.strip():
        try:
            user_prompt = f"Review the above code and provide feedback: {code_input}"
            review_results = code_review_model.generate_content(prompt=user_prompt)
            st.markdown("## Review Results")
            st.markdown(review_results.text)

        except Exception as error_detail:
            st.error(f"An error occurred during the code review: {error_detail}")

    else:
        st.warning("Please provide some Python code to review, either by pasting it or uploading a file.")
