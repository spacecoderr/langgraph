from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState) -> ChatState:
    messages=state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

#Checkpointer

checkpointer = InMemorySaver()

graph=StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(checkpointer=checkpointer)
stream=chatbot.stream(
    {"messages":[HumanMessage(content="How to make maggie")]},
     config={"configurable": {"thread_id": "thread-1"}},
     stream_mode= 'messages'
)#This returns 2 things message_chunk and metadata
print(type(stream)) #This returns a generator and to get the values we need to use loop
#because it is an iterator and we need to iterate over it to get the values

for message_chunk, metadata in stream:
    if message_chunk.content:
        print(message_chunk.content,end=" ",flush=True)
        