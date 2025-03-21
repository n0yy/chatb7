import streamlit as st
import time

from uuid import uuid4
from lib.google_cloud import collection

# Set page config
st.set_page_config(
    page_title="Feedback", page_icon=":incoming_envelope:", layout="centered"
)

feedback, feedback_response = st.tabs(["Feedback", "Feedback AI's Response"])

with feedback:
    st.title("Feedback :incoming_envelope:")
    st.write("Silahkan isi feedback Anda di bawah ini")

    user_id = str(uuid4())
    name = st.text_input("Nama", key="name", placeholder="John Doe")
    message = st.text_area("Feedback", key="message", placeholder="Thats cool app")
    datetime = time.strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Kirim Feedback", key="send_feedback"):
        feedback = collection("feedback")
        doc_ref = feedback.document(user_id)
        doc_ref.set({"name": name, "message": message, "datetime": datetime})
        st.success("Feedback Anda telah dikirim")

with feedback_response:
    st.title("Feedback AI's Response")
    st.write("Silahkan isi form dibawah ini jika respon yang AI berikan tidak sesuai")

    user_id = str(uuid4())
    name = st.text_input("Masukan Nama Anda", key="name_ai  ", placeholder="John Doe")
    prompt = st.text_area(
        "Masukan Prompt", key="prompt", placeholder="-- PLACEHOLDER YANG COCOK --"
    )
    response = st.text_area(
        "Response yang diharapkan",
        key="response",
        placeholder="-- PLACEHOLDER YANG COCOK --",
    )
    datetime = time.strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Kirim Feedback", key="send_feedback_ai_response"):
        feedback = collection("feedbacks_ai_response")
        doc_ref = feedback.document(user_id)
        doc_ref.set({"name": name, "prompt": prompt, "response": response})
        st.success("Feedback Anda telah dikirim")
