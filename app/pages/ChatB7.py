import streamlit as st
from utils.word_stream import word_stream

# Set page config
st.set_page_config(page_title="ChatB7", page_icon=":robot_face:")

# Get the language model from session state
llm = st.session_state.llm

if len(st.session_state.messages) == 0:
    st.title("ChatB7 :robot_face:")
    st.write(
        "Asisten virtual yang siap membantu Anda dengan informasi seputar PT Bintang Toedjoe dan produk-produknya"
    )

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(
        message["role"], avatar="🤖" if message["role"] == "ai" else None
    ):
        st.write(message["content"])
        if message["role"] == "ai" and "source" in message:
            st.write("---")
            st.markdown("[Source](%s)" % message["source"])

# Input Pengguna
user_query = st.chat_input("Pertanyaan Anda...")

if user_query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Display user message
    with st.chat_message("user"):
        st.write(user_query)

    # Get AI response
    with st.spinner("Loadingg...", show_time=True):
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
                    {
                        "role": "ai",
                        "content": response_text,
                        "source": response.source,
                    }
                )
            else:
                # Add the completed AI message to history without source
                st.session_state.messages.append(
                    {"role": "ai", "content": response_text}
                )
