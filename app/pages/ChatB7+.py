import streamlit as st
from langchain_community.utilities import SQLDatabase
from utils.word_stream import word_stream

# Set page config
st.set_page_config(page_title="ChatB7+", page_icon=":robot_face:")

# Get the language model from session state
llm = st.session_state.llm

# UI Header
st.title("ChatB7+ :robot_face:")
st.write("Interaksi dengan database")

# Initialize database connection state if not present
if "db_connected" not in st.session_state:
    st.session_state.db_connected = False

# Only show the connection form if not already connected
if not st.session_state.db_connected:
    # Database Connection UI
    st.markdown("## Connect to Database")
    username = st.text_input("Username", key="username", placeholder="root")
    password = st.text_input(
        "Password", key="password", placeholder="root", type="password"
    )
    host = st.text_input("Host", key="host", placeholder="localhost")
    port = st.text_input("Port", key="port", placeholder="3306")
    dbname = st.text_input("Database Name", key="dbname", placeholder="User")

    submit_connect = st.button("Connect")

    if submit_connect:
        uri = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{dbname}"
        try:
            with st.spinner("Connecting..."):
                db = SQLDatabase.from_uri(uri)
                st.session_state.db = db
                st.session_state.db_connected = True
            st.success("MySQL Connected!")
            # Force a rerun to refresh the UI and hide the form
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
else:
    # Show connected status and option to disconnect
    st.success("Connected to database")
    if st.button("Disconnect"):
        st.session_state.db_connected = False
        if "db" in st.session_state:
            del st.session_state.db
        st.rerun()

# Database interaction UI - only show if connected
if st.session_state.db_connected:

    # Create a separate message history for database interactions
    if "db_messages" not in st.session_state:
        st.session_state.db_messages = []

    # Display chat history
    for message in st.session_state.db_messages:
        with st.chat_message(
            message["role"], avatar="🤖" if message["role"] == "ai" else None
        ):
            st.write(message["content"])

    # Input for database query
    db_query = st.chat_input("Ask a question about your database...")

    if db_query:
        # Add user message to history
        st.session_state.db_messages.append({"role": "user", "content": db_query})

        # Display user message
        with st.chat_message("user"):
            st.write(db_query)

        # Get AI response
        with st.spinner("Querying database...", show_time=True):
            # TODO: Interect with LLM. Below is Example:
            response = llm.run(f"Database query: {db_query}")
            response_text = ""

            # Create a placeholder for streaming response
            with st.chat_message("ai", avatar="🤖"):
                message_placeholder = st.empty()

                # Stream the response
                for chunk in word_stream(response):
                    response_text += chunk
                    message_placeholder.write(response_text)

                # Add the completed AI message to history
                st.session_state.db_messages.append(
                    {"role": "ai", "content": response_text}
                )
