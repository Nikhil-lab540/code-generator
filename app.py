import streamlit as st
import logging
from groq import Groq
import os

# Set up logging configuration to log prompts
logging.basicConfig(
    filename="prompts.log",  # Log file to store user prompts
    level=logging.INFO,  # Log info level to capture user inputs
    format="%(asctime)s - %(message)s",  # Log format to capture the time and prompt
)

# Initialize Groq client (placeholder)
client = Groq(os.getenv('groq'))

# Set page configuration
st.set_page_config(page_title="Code Generator with llama-3.1-70b-versatile", layout="wide")

# Title of the app
st.title("Streamlit Code Generator with Prompt Logging")

# Input prompt from user
st.write("### Enter a prompt for the code generator")
user_prompt = st.text_area(
    "Enter your description (e.g., 'write Python code for swapping two numbers')",
    placeholder="Enter your prompt here..."
)
def hide_streamlit_style():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

hide_streamlit_style()


# Function to generate code using Groq Llama3 API (simplified placeholder)
def generate_code_with_groq(prompt):
    # Placeholder for calling Groq's API
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    generated_code = ""
    for chunk in completion:
        generated_code += chunk.choices[0].delta.content or ""
    return generated_code

# Display generated code and log the prompt
if st.button("Generate Code"):
    if user_prompt:
        # Log the user prompt
        logging.info(f"User Prompt: {user_prompt}")
        
        with st.spinner("Generating code..."):
            try:
                # Generate code using the Groq API
                generated_code = generate_code_with_groq(user_prompt)
                st.code(generated_code, language="python")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a description before generating code!")

