from graphagent import Agent

from typing import List
import uuid


class HumanInterrupt(BaseException):
    def __str__(self):
        return "Interrupted by User"


class AgentHIL(Agent):
    """ Agent Class with Human in the Loop breakpoints
    
    Attributes:
        interrputed_nodes: List of nodes to add breakpoints before traversing forward to the graph state.
    """
    interrupted_nodes: List[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # recompile graph
        self.graph = self.uncompiledgraph.compile(checkpointer=self.checkpointer, interrupt_before=self.interrupted_nodes)
    
    def breakpoint_invoke(self, userinput="What is the weather in sf?", thread={"configurable": {"thread_id": f"{uuid.uuid1().hex}"}}):
        """ Invoke AgentHIL with human breakpoint and resume after intervention
        TODO: Allow User to update the state of the graph, this should also allow for promptguards to mitigate external injection

        Args:
            userinput: Initial user query to start
            thread: dictionary configuration for streaming the graph
        """
        messages = [HumanMessage(content=userinput)]
        for event in self.graph.stream({"messages": messages}, thread, stream_mode="values"):
            event["messages"][-1].pretty_print()

        nextstage = abot.graph.get_state(thread).next

        while nextstage:
            userapproval = input(f"Do you want to go to {nextstage[0]}? (yes/no): ")
            if userapproval == 'yes':
                for event in self.graph.stream(None, thread, stream_mode="values"):
                    event["messages"][-1].pretty_print()
                
                nextstage = abot.graph.get_state(thread).next
            else:
                raise HumanInterrupt()
            

if __name__ == "__main__":
    from langgraph.graph import StateGraph
    from langgraph.checkpoint.sqlite import SqliteSaver

    import os.path as osp
    import sys

    script_dir = osp.dirname(__file__)
    sys.path.insert(0, osp.dirname(script_dir))
    from llms.models import ChatOpenAIRateLimited
    from tools import searchtool
    from utils.agentutils import AgentState
    import uuid
    from langchain_core.messages import HumanMessage

    prompt = """You are a smart research assistant. Use the search engine to look up information. \
            You are allowed to make multiple calls (either together or in sequence). \
            Only look up information when you are sure of what you want. \
            If you need to look up some information before asking a follow up question, you are allowed to do that!
            """
    
    # Sqllit connection for in-memory persistance
    memory = SqliteSaver.from_conn_string(":memory:")

    model = ChatOpenAIRateLimited() 
    tool = searchtool.search_tool()
    abot = AgentHIL(uncompiledgraph= StateGraph(AgentState), model=model, tools_=[tool], checkpointer=memory, description=prompt, interrupted_nodes=['llm'])
    abot.breakpoint_invoke()
