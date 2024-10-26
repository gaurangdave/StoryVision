import streamlit as st
import requests
from io import BytesIO

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000/process-image"

st.title("Accessible Storybook Narrator")
st.write("Upload an image, and the app will generate an engaging audio description!")

# File uploader widget
uploaded_file = st.file_uploader(
    "Choose an image file", type=["jpg", "jpeg", "png"])

# Display button to trigger processing
if uploaded_file is not None:
    if st.button("Generate Audio Description"):
        # Send the uploaded file to the FastAPI endpoint
        files = {"file": (uploaded_file.name, uploaded_file,
                          "multipart/form-data")}
        try:
            response = requests.post(FASTAPI_URL, files=files)
            response.raise_for_status()  # Raises error if response status code is not 200

            # Load the audio content
            audio_data = BytesIO(response.content)
            # Play the audio in Streamlit
            st.audio(audio_data, format="audio/mp3")
            st.success("Audio description generated successfully!")

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503:
                st.error(
                    "Service is currently unavailable. Please ensure all modules are installed and accessible.")
            elif response.status_code == 500:
                st.error(
                    "There was an error generating the audio. Please try again.")
            else:
                st.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            st.error(f"Error connecting to the backend: {err}")