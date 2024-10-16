import streamlit as st
from groq import Groq
import os

# Initialize Groq client
client = Groq(api_key=os.getenv('groq'))

# Set page configuration
st.set_page_config(page_title="Streamlit Code Generator with Groq Llama3", layout="wide")

# Title of the app
st.title("Streamlit Code Generator using Llama3")

# Input prompt from user
st.write("### Enter a prompt for the code generator")
user_prompt = st.text_area(
    "Enter your description (e.g., 'write Python code for swapping two numbers')",
    placeholder="Enter your prompt here..."
)

# Function to generate code using Groq Llama3 API
def generate_code_with_groq(prompt):
    # Call the Groq API to generate the code
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
    # Stream the chunks of code as they are generated
    for chunk in completion:
        generated_code += chunk.choices[0].delta.content or ""
        yield generated_code

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

# Display generated code interactively
if st.button("Generate Code"):
    if user_prompt:
        # Display spinner while the code is being generated
        with st.spinner("Generating code..."):
            try:
                # Stream the generated code to the app in real-time
                generated_code = ""
                code_display = st.empty()  # Create an empty placeholder for the code
                
                # Stream the generated code in chunks
                for code_chunk in generate_code_with_groq(user_prompt):
                    generated_code = code_chunk
                    code_display.code(generated_code, language="python")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a description before generating code!")

# Optional: Provide a download button once the code is generated
if 'generated_code' in locals() and generated_code:
    st.sidebar.download_button(
        label="Download Generated Code",
        data=generated_code,
        file_name="generated_code.py",
        mime="text/x-python"
    )
