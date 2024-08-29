from uuid import uuid4
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage

from typing import Annotated, TypedDict
import operator

def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    """
    Supports replacement of existing messages with the same `id` and appends otherwise.

    Args:
        left: list = Current list of messages in the state
        right: list = Modified/New list of messages
    """
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    return merged

# class AgentState(TypedDict):
#     "Class updates agent states with appended messages, not overwriting the previous state"
#     messages: Annotated[list[AnyMessage], operator.add]

class AgentState(TypedDict):
    "Class updates agent states with appended messages, will overwrite state messages with human breakpoints"
    messages: Annotated[list[AnyMessage], reduce_messages]