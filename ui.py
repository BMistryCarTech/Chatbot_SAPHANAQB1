import streamlit as st
import uuid
import csv
from io import StringIO
from langchain.memory import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain.callbacks import StreamlitCallbackHandler

def init_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "message_history" not in st.session_state:
        st.session_state.message_history = ChatMessageHistory()

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.message_history = ChatMessageHistory()
    st.success("Chat cleared.")

def chat_ui(agent_executor):
    user_input = st.chat_input("Ask anything...")
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.message_history.add_user_message(user_input)

        # Build context
        context_string = ""
        for msg in st.session_state.message_history.messages[:-1]:
            if isinstance(msg, HumanMessage):
                context_string += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                context_string += f"Bot: {msg.content}\n"
        context_string += f"User: {user_input}"

        with st.spinner("Thinking..."):
            callback = StreamlitCallbackHandler(st.container())
            try:
                response = agent_executor.invoke({"input": context_string}, callbacks=[callback])
                final_output = response.get("output", str(response))
            except Exception as e:
                final_output = f"Error: {str(e)}"

            st.session_state.message_history.add_ai_message(final_output)
            st.session_state.chat_history.append(("Bot", final_output))

    # Display history
    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {msg}")

def export_history():
    if st.sidebar.button("Export Chat History to CSV"):
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Sender", "Message"])
        for sender, message in st.session_state.chat_history:
            writer.writerow([sender, message])

        st.download_button(
            label="Download Chat History (CSV)",
            data=csv_buffer.getvalue(),
            file_name="chat_history.csv",
            mime="text/csv"
        )
