import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Home", page_icon=":robot_face:", layout="centered")

# Initialize session state for the language model
if "llm" not in st.session_state:
    from models.llms import LanguageModel

    st.session_state.llm = LanguageModel(model="gemini-2.0-pro-exp-02-05")

# Initialize messages if not already in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define the homepage content
st.title("Welcome to ChatB7 :robot_face:")
st.write(
    "ChatB7 adalah asisten virtual yang dirancang untuk membantu Anda dengan informasi seputar PT Bintang Toedjoe dan produk-produknya. Proyek ini bertujuan untuk menyediakan akses cepat dan mudah ke pengetahuan tentang perusahaan, termasuk profil perusahaan, produk, dan informasi terkini."
)

# Changelog section
st.markdown("#### Version")
with st.expander("v0.1.4-beta"):
    st.markdown(
        """
        March 20, 2025
        #### Knowledge base:
            - Company Profile

        Untuk menambahkan pengetahuan ChatB7, silakan unggah file PDF, DOCX, atau PPTX ke Google Drive kami:
        """
    )
    st.link_button(
        "Akses File Sumber",
        "https://drive.google.com/drive/folders/1WUx_0ztyjDt-e08SDoqqDePJnnxZXpIV?usp=sharing",
    )
