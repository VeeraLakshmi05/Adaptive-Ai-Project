from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END 
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
import os
import getpass

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

MODEL_NAME = "gemini-2.5-flash"

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME, 
    temperature=0
)

class MessageClassifier (BaseModel):
    message_type: Literal["emotional", "logical"] = Field(
        ...,
        description="classify if the user's message requires 'emotional'/'therapist' or 'logical' response"
    )

class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str | None

graph_builder = StateGraph(State)

def classify_message(state: State):
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)
    result = classifier_llm.invoke([
        {
            "role": "system",
            "content": """Classify the user message as either:
            - 'emotional': if it asks for emotional support, therapy, deals with feelings, or personal problems
            - 'logical': if it asks for facts, information, logical analysis, or practical solutions
            """
        },
        {"role": "user", "content": last_message.content}
    ])
    return {
        "message_type": result.message_type
    }

def therapist_agent(state: State):
    last_message = state["messages"][-1]

    messages = [
        {"role": "system",
         "content": """You are a compassionate therapist. Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked."""
         },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}

def logical_agent(state: State):
    last_message = state["messages"][-1]

    messages = [
        {"role": "system",
         "content": """You are a purely logical assistant. Focus only on facts and information.
            Provide clear, concise answers based on logic and evidence.
            Do not address emotions or provide emotional support.
            Be direct and straightforward in your responses."""
         },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    reply = llm.invoke(messages)
    return {"messages": [{"role": "assistant", "content": reply.content}]}

def router(state: State):
    message_type = state.get("message_type", "logical")
    if message_type == "emotional":
        return {
            "next": "therapist"
        }
    else:
        return {
            "next": "logical"
        }


graph_builder.add_node("classify", classify_message)
graph_builder.add_node("therapist", therapist_agent)
graph_builder.add_node("logical", logical_agent)
graph_builder.add_node("router", router)

graph_builder.add_edge(START, "classify")
graph_builder.add_edge("classify", "router")

graph_builder.add_conditional_edges(
    "router",
    lambda state: state["next"],
    {"therapist": "therapist", "logical": "logical"}
)

graph_builder.add_edge("therapist", END)
graph_builder.add_edge("logical", END)

graph = graph_builder.compile()

def run_chat():
    state: State = {
        "messages": [],
        "message_type": None
    }

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        state["messages"].append({"role": "user", "content": user_input})

        state = graph.invoke(state)

        if state.get("messages") and len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            print("Assistant:", last_message.content)


if __name__ == "__main__":
    run_chat()