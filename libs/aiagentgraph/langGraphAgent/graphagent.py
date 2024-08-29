from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.sqlite import SqliteSaver

import os
import os.path as osp
import sys
import uuid

import pydantic
from pydantic import BaseModel
from typing import List, Any, Dict, Union

script_dir = osp.dirname(__file__)
sys.path.insert(0, osp.dirname(script_dir))
from llms.models import ChatOpenAIRateLimited
from tools import searchtool
from utils.agentutils import AgentState

# Sqllit connection for in-memory persistance
memory = SqliteSaver.from_conn_string(":memory:")


class Agent(BaseModel):
    """Agent based on LangGraph

    A class for creating instances of an Agent

    Attributes:
        graph: StateGraph instance
        description: System Message to the LLM
        tools_: List of tools to bind to the model
        tools: Attribute provides a dict of the tool name and method
        uncompiledgraph: graph state before compiling
        model: langchain model objects
        checkpointer: Any persistance memory to pass as a checkpoint to the graph

    """
    graph: Union[StateGraph, None] = None
    description: str = ""
    tools_: List[Any]
    tools: Dict[str, Any] = {}
    uncompiledgraph: StateGraph
    model: Any
    checkpointer: Any

    class Config:
            arbitrary_types_allowed = True
            
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uncompiledgraph.add_node("llm", self.call_openai)
        self.uncompiledgraph.add_node("action", self.take_action)
        self.uncompiledgraph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        self.uncompiledgraph.add_edge("action", "llm")
        self.uncompiledgraph.set_entry_point("llm")
        self.graph = self.uncompiledgraph.compile(checkpointer=self.checkpointer)
        self.tools = {t.name: t for t in self.tools_}
        self.model = self.model.bind_tools(self.tools_)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.description:
            messages = [SystemMessage(content=self.description)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                try:
                    result = self.tools[t['name']].invoke(t['args'])
                except pydantic.v1.error_wrappers.ValidationError:
                    print(f"\n Validation Error; Likely missing tool input arg {t.get('args')}")
                    result = "Tool argument not passed, retry"
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}


if __name__ == "__main__":
    import argparse

    prompt = """You are a smart research assistant. Use the search engine to look up information. \
            You are allowed to make multiple calls (either together or in sequence). \
            Only look up information when you are sure of what you want. \
            If you need to look up some information before asking a follow up question, you are allowed to do that!
            """

    def fileParser():
        parser = argparse.ArgumentParser(
            prog='LangChain Agent',
            description="Defines an agent using Langgraph"
        )

        savepoint = osp.join(script_dir, 'visual')
        os.makedirs(savepoint, exist_ok=True)
        
        parser.add_argument("--savepath", default=osp.join(savepoint, 'graphagent.png'), type=str, required=False)
        parser.add_argument("--savegraph", default=False, type=bool, required=False)
        parser.add_argument("--run", default=False, type=bool, required=False)

        return parser.parse_args()
    
    args_ = fileParser()

    model = ChatOpenAIRateLimited() 
    tool = searchtool.search_tool()
    abot = Agent(uncompiledgraph= StateGraph(AgentState), model=model, tools_=[tool], checkpointer=memory, description=prompt)
    
    if args_.run:
        # UUID will serve as the sessionid, we want to have a deterministic customerid so that we can return to the state
        # in subsequent conversations
        thread_id = uuid.uuid1().hex
        messages = [HumanMessage(content="What is the weather in sf?")]
        thread = {"configurable": {"thread_id": f"{thread_id}"}}
        for event in abot.graph.stream({"messages": messages}, thread, stream_mode="values"):
            event["messages"][-1].pretty_print()

        # Reinitiate bot 
        # Using the same thread, with in-memory checkpoint new bot can start where we left off
        second_bot = Agent(uncompiledgraph= StateGraph(AgentState), model=model, tools_=[tool], checkpointer=memory, description=prompt)
        messages = [HumanMessage(content="Are you sure?")]
        for event in second_bot.graph.stream({"messages": messages}, thread, stream_mode="values"):
            event["messages"][-1].pretty_print()

        # Memory
        print("================================ Sql Memory Chkpt =================================")
        print(list(memory.list(thread))[-1])

    if args_.savegraph:
        abot.graph.get_graph().draw_png(args_.savepath)
