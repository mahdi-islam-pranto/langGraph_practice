from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
# for add all messages to state
from langgraph.graph.message import add_messages
# for memory saver (local ram)
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
# load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", api_key="")

# define state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# define functions
def chat_node(state: ChatState):
    all_messages = state['messages']
    llm_response = llm.invoke(all_messages)
    return {'messages': [llm_response]}


# define memory
check_pointer = MemorySaver()

# define state
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


chatbot = graph.compile(checkpointer=check_pointer)

thread_id = "1"

config = {'configurable': {"thread_id": thread_id}}

# make the loop for the chatbot


   

# initial_state = {'messages': [SystemMessage(content="You are a helpful chatbot."),
#                                   HumanMessage(content=user_input)]}
# response = chatbot.invoke(initial_state, config=config)
# print("Chatbot: " + response['messages'][-1].content)