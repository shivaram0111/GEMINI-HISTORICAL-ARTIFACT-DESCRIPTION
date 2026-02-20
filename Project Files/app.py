from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
#load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
# Function to get Gemini response
def get_gemini_response(input_text, image, prompt):
  model = genai.GenerativeModel("gemini-2.5-flash")
  response = model.generate_content([input_text, image[0], prompt])
  return response.text
#Function to setup input image
def input_image_setup(uploaded_file):
  if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    image_parts= [
      {
        "mime_type": uploaded_file.type,
        "data": bytes_data
      }
    ]
    return image_parts
  else:
    raise FileNotFoundError("No file uploaded")
#Initialize Streamlit app
st.set_page_config(page_title="Gemini Historical Artifact Description App", page_icon="🏺")
st.header("🏺 Gemini Historical Artifact Description App")
input_text = st.text_input("📝 Input Prompt:", key="input")
uploaded_file = st.file_uploader("🖼️ Choose an image of an artifact...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
  image = Image.open(uploaded_file)
  st.image(image, caption="📷 Uploaded Image.", use_container_width=True)
submit = st.button("🚀 Generate Artifact Description")
input_prompt = """
You are a historian. Please describe the historical artifact in the image and provide detailed information, including its name, origin, time period, materials used, purpose, and cultural significance, and any interesting historical facts.
----
----

"""
# If submit button is clicked
if submit:
  try:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt + input_text, image_data, input_prompt)
    st.subheader("📜 Generated Artifact Description:")
    st.write(response)
  except Exception as e:
    st.error(f"⚠️ Error: {str(e)}")