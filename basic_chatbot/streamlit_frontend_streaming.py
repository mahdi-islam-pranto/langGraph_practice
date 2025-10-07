import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, SystemMessage

st.title("Ask me anything")

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# sample message history
# st.session_state["message_history"] = [
#     {"role": "user", "content": "Hello"},
#     {"role": "assistant", "content": "Hello, how can I help you?"},
# ]

# get user input
user_input = st.chat_input("Type here: ")

# show message history in the chat interface
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

# show user input in the chat interface
if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message('user'):
        st.text(user_input)


    thread_id = "1"

    config = {'configurable': {"thread_id": thread_id}}

    # get chatbot response
    # response = chatbot.invoke({"messages": [SystemMessage(content="You are a helpful chatbot."),
    #                               HumanMessage(content=user_input)]}, config=config )
    # ai_response = response['messages'][-1].content


    
    # show chatbot response in the chat interface
    with st.chat_message('assistant'):
        ai_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream({"messages": [SystemMessage(content="You are a helpful chatbot."),
                              HumanMessage(content=user_input)]}, config=config, stream_mode='messages' )
        )

        # put ai response in the message history
    st.session_state["message_history"].append({"role": "assistant", "content": ai_response})
        