from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
# for add all messages to state
from langgraph.graph.message import add_messages
# for memory saver (sqlite)
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3
# load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key="AIzaSyC8k0BJEofzDvH9pXmUCEsilPlSBSZmf5s")

# define state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# define functions
def chat_node(state: ChatState):
    all_messages = state['messages']
    llm_response = llm.invoke(all_messages)
    return {'messages': [llm_response]}

# connect to database
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# define memory
check_pointer = SqliteSaver(conn=conn)

# define state
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


chatbot = graph.compile(checkpointer=check_pointer)

thread_id = "thread_id_1"

config = {'configurable': {"thread_id": thread_id}}


# check chatbot memory working
# response = chatbot.invoke({"messages": [HumanMessage(content="What is the capital of Bangladesh?")]}, config=config)

# get all the thread_ids from the database checkpointer
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in check_pointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)
# print(retrieve_all_threads())