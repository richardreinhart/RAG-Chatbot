import streamlit as st
import random
import time
import backend_llm

def response_generator(prompt):
    history = []
    pairs = []
    messages = st.session_state.messages
    for i in range(len(messages) - 2, -1, -2):
        if len(pairs) >= 2:
            break
        assistant_msg = messages[i]
        user_msg = messages[i + 1] if i + 1 < len(messages) else {"content": ""}
        if user_msg["role"] == "user" and assistant_msg["role"] == "assistant":
            pairs.insert(0, {"user": user_msg["content"], "assistant": assistant_msg["content"]})

    response = backend_llm.GenerateResponse(prompt, pairs)

    if response is None or not isinstance(response, str):
        st.error("Failed to generate response or response is not a valid string.")
        return ""

    response_container = st.empty()
    full_response = ""
    for char in response:
        full_response += char
        response_container.markdown(f"{full_response}▌") 
        time.sleep(0.001)

    response_container.markdown(full_response)
    return full_response

def run_plain_chatbot():
    st.title("Plain Chatbot")
    st.markdown("This chatbot using LLM to answer your questions")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What can I help you?"):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            full_response = response_generator(prompt)

        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    run_plain_chatbot()