import streamlit as st
import requests
from helper import validate_files
import re
import io
import base64
from PIL import Image
st.set_page_config(page_title="GENIE", page_icon="🤖")
# Remove padding and margin from all possible elements
st.markdown(
        """
        <style>
            /* Remove padding and margin from the entire page */
            .css-18e3th9, .css-1d391kg, .stApp {
                padding: 0;
                margin: 0;
            }
            /* Remove space from the header if it exists */
            header, .block-container {
                padding-top: 0;
                margin-top: 0;
            }
            /* Ensures the body has no extra space */
            body {
                margin: 0;
                padding: 0;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# # Define the path of the logo file
logo_path = "logo.png"  # Ensure this path is correct    
# # Display the logo
# st.image(logo_path,width=300,use_column_width=False, output_format="SVG")

# Open and resize the image
img = Image.open(logo_path)

# Convert the image to bytes
img_bytes = io.BytesIO()
img.save(img_bytes, format='png')
img_bytes.seek(0)

# Encode the image bytes to base64
img_base64 = base64.b64encode(img_bytes.getvalue()).decode()

# Display the image with HTML/CSS centering and margin
st.markdown(
    f'''
    <div style="text-align: center; margin-top: 50px; margin-bottom: 50px;">
        <img src="data:image/png;base64,{img_base64}" style="width: 250px;" />
    </div>
    ''',
    unsafe_allow_html=True
)

# Custom CSS for blinking cursor
st.markdown("""
    <style>
        .blinking-cursor {
            animation: blink 1s step-end infinite;
        }
        @keyframes blink {
            50% { opacity: 0; }
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": """
         Hello! I'm **GENIE**  
         **I can help you with your resume. Here's how you can use me:**
            - step 1: Upload your resume in PDF or DOCX format.
            - step 2: Ask any questions about your resume.
            - step 3: I will provide feedback and suggestions.
         
         enjoy!💖

         """}
    ]

# Sidebar for file upload
with st.sidebar:
    st.sidebar.title("PDF File Uploader")
    uploaded_files = st.sidebar.file_uploader(
        "Choose PDF files", accept_multiple_files=True, type=["pdf"]
    )

    if uploaded_files:
        invalid_files = validate_files(uploaded_files)

        if invalid_files:
            # Display validation errors
            error_message = "The following files are invalid:\n"
            for file, reason in invalid_files:
                error_message += f"- {file}: {reason}\n"
            st.sidebar.error(error_message)
        else:
            files_to_upload = [("files", (file.name, file, file.type))
                               for file in uploaded_files]

            with st.spinner('Retrieving context... Please wait.'):
                try:
                    response = requests.post("http://localhost:8000/upload", files=files_to_upload)
                    response.raise_for_status()

                    result = response.json()
                    if result["status"] == "success":
                        st.sidebar.success("Files uploaded successfully!")
                    else:
                        st.sidebar.error(f"Error: {result['message']}")
                except requests.RequestException as e:
                    st.sidebar.error(f"Error communicating with the server: {e}")


# Main chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response_parts = []

        with st.spinner("Thinking..."):
            try:
                # Use a streaming request from the server
                response = requests.post(
                    "http://localhost:8000/chat", json={"query": prompt}, stream=True
                )

                if response.status_code == 200:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            decoded_chunk = chunk.decode("utf-8").strip()

                            # Remove "data:" prefix if present
                            if decoded_chunk.startswith("data:"):
                                decoded_chunk = decoded_chunk[5:].strip()

                            # Replace escaped newlines with actual newlines
                            decoded_chunk = decoded_chunk.replace("\\n", "\n")

                            # Remove excessive spaces around punctuation
                            decoded_chunk = re.sub(r'\s+([.,!])', r'\1', decoded_chunk)  # Remove spaces before punctuation
                            decoded_chunk = re.sub(r'([.,!])\s+', r'\1 ', decoded_chunk)  # Ensure single space after punctuation

                            # Append a space between chunks if the last part does not end with punctuation
                            if response_parts and not response_parts[-1].endswith(('.', '!', '?')):
                                response_parts[-1] += " "  # Add a space to the last part


                            # Append the decoded chunk
                            response_parts.append(decoded_chunk)

                            # Render progressively with Markdown
                            formatted_response = "".join(response_parts)
                            message_placeholder.markdown(formatted_response, unsafe_allow_html=True)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error communicating with the server: {e}")

        response = "".join(response_parts)
        message_placeholder.markdown(response)

    # Add the assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
