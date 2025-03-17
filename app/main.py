import streamlit as st
from dotenv import load_dotenv
from models.llms import LanguageModel
from utils.word_stream import word_stream

load_dotenv()

# Load Model
st.set_page_config(page_title="ChatB7", page_icon=":robot_face:")
llm = LanguageModel(model="gemini-2.0-pro-exp-02-05")


# Initial State
if "messages" not in st.session_state:
    st.session_state.messages = []

# UI Config
st.title("ChatB7 :robot_face:")
st.write(
    "Asisten virtual yang siap membantu Anda dengan informasi seputar, Profil perusahaan PT Bintang Toedjoe dan produk-produknya"
)

# Menggunakan expander sebagai alternatif dialog
with st.sidebar:
    with st.expander("Changelog"):
        st.markdown(
            """            
            ### _Version 0.1.2-beta_  
            #### Features:
            - ChatB7 Released
            - Knowledge base:
                - Company Profile
                - Kua Lima
            - Tampilan dasar
            ### Limitation
            - Batas Pengetahuan: hanya Profil Perusahaan dan Kua Lima)
            - Hanya fitur dasar yang tersedia

            Untuk menambahkan pengetahuan ChatB7, silakan unggah file PDF atau PPTX ke Google Drive kami:
            """
        )
        st.link_button(
            "Akses File Sumber",
            "https://drive.google.com/drive/folders/1WUx_0ztyjDt-e08SDoqqDePJnnxZXpIV?usp=sharing",
        )

for message in st.session_state.messages:
    with st.chat_message(
        message["role"], avatar="🤖" if message["role"] == "ai" else None
    ):
        st.write(message["content"])
        if message["role"] == "ai" and "source" in message:
            st.write("---")
            st.markdown("[Source](%s)" % message["source"])

user_query = st.chat_input("Kamu nanyuwaakkkkkk..???")

if user_query is not None:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Display user message
    with st.chat_message("user"):
        st.write(user_query)

    # Get AI response
    with st.spinner("Mirasss (mikir keras)...", show_time=True):
        response = llm.run(user_query)
        response_text = ""

        # Create a placeholder for streaming response
        with st.chat_message("ai", avatar="🤖"):
            message_placeholder = st.empty()

            # Stream the response
            for chunk in word_stream(response):
                response_text += chunk
                message_placeholder.write(response_text)

            # Add source reference if available
            if hasattr(response, "source"):
                st.write("---")
                st.markdown("[Source](%s)" % response.source)
                # Add the completed AI message with source to history
                st.session_state.messages.append(
                    {"role": "ai", "content": response_text, "source": response.source}
                )
            else:
                # Add the completed AI message to history without source
                st.session_state.messages.append(
                    {"role": "ai", "content": response_text}
                )
