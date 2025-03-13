import streamlit as st
from dotenv import load_dotenv
from utils.file import save_uploaded_file
from models.llms import LanguageModel

load_dotenv()

# Load Model
st.set_page_config(page_title="ChatB7", page_icon=":robot_face:")
llm = LanguageModel(model="gemini-2.0-flash-thinking-exp-01-21")

# UI Config
st.title("ChatB7 :robot_face:")
st.write(
    "Asisten virtual yang siap membantu Anda dengan informasi seputar, Profil perusahaan PT Bintang Toedjoe dan produk-produknya"
)
with st.expander("Knowledge Base :"):
    st.write("ChatB7 baru belajar tentang Company Profile dan Kua Lima saja")
    st.write(
        "[Source](https://drive.google.com/drive/folders/1WUx_0ztyjDt-e08SDoqqDePJnnxZXpIV?usp=sharing)"
    )
    st.write(
        "Jika ingin menambahkan Knowledge silahkan upload file berupa pdf atau pptx ke Google Drive diatas"
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

user_query = st.chat_input("Kamu nanyuwaakkkkkk..???")

if user_query:
    with st.chat_message("user"):
        st.write(user_query)

    with st.spinner("Mirasss (mikir keras)...", show_time=True):
        relevant_docs = llm.find_related_docs(user_query)
        response = llm.invoke(user_query, relevant_docs)

    with st.chat_message("ai", avatar="🤖"):
        st.write(response)
        st.write("---")

        source_path = [
            source.metadata.get("source", "Unknown") for source in relevant_docs
        ]
        st.markdown("[Source](%s)" % set(source_path))
