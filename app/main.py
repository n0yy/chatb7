import streamlit as st
from dotenv import load_dotenv
from utils.file import save_uploaded_file
from models.llms import LanguageModel
from utils.word_stream import word_stream

load_dotenv()

# Load Model
st.set_page_config(page_title="ChatB7", page_icon=":robot_face:")
llm = LanguageModel(model="gemini-2.0-flash-thinking-exp-01-21")


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
            ### _Version 0.0.1_ (Maret 2025)
            
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

# uploaded_pdf = st.file_uploader(
#     "Upload Dokumen (.pdf, .pptx)",
#     type=["pdf", "pptx"],
#     help="Pilih dokumen",
#     accept_multiple_files=True,
# )

# all_docs = []

# if uploaded_pdf:
#     for uploaded_file in uploaded_pdf:
#         save_path = save_uploaded_file(uploaded_file)

#         if uploaded_file.name.endswith(".pdf"):
#             raw_docs = llm.load_pdf(save_path)

#         elif uploaded_file.name.endswith(".pptx"):
#             raw_docs = llm.load_pptx(save_path)

#         # elif uploaded_file.name.endswith(".docx"):
#         #     raw_docs = llm.load_csv(save_path)

#         else:
#             st.error(
#                 f"Format file belum didukung untuk saat ini.\n{uploaded_file.name}"
#             )
#             continue

#     processed_chunks = llm.chunk_docs(raw_docs)
#     all_docs.extend(processed_chunks)
#     if all_docs:
#         llm.index_docs(all_docs)
#         st.success("✅ Semua dokumen teks berhasil diindeks!")

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

    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("user"):
        st.write(user_query)

    with st.spinner("Mirasss (mikir keras)...", show_time=True):
        relevant_docs = llm.find_related_docs(user_query)
        response = llm.invoke(user_query, relevant_docs)

        response = word_stream(response)

        source_paths = [
            source.metadata.get("source", "Unknown") for source in relevant_docs
        ]
        source_set = set(source_paths)

    st.session_state.messages.append(
        {"role": "ai", "content": response, "source": source_set}
    )

    with st.chat_message("ai", avatar="🤖"):
        st.write_stream(response)
        st.write("---")

        st.markdown("[Source](%s)" % set(source_set))
