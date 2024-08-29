> AI Agents with LangGraph
> [![LangGraph Version](https://img.shields.io/badge/langgraph-0.0.53-green)](https://pypi.org/project/langgraph/0.0.53/)

# Introduction
Developed a cutting-edge Research Assistant Agent that utilizes a search tool to fetch up-to-date information, generating informed responses to user queries. Built on top of LangGraph AgentState, our agent leverages the powerful GPT-4O LLM model and integrates seamlessly with the TavillySearch API for external search capabilities.

Key Features:
- Contextual Understanding: The agent comprehends user queries and decides when to initiate search actions, ensuring optimal responses.
- Parallel Search Calls: Equipped to handle multiple searches simultaneously, enhancing efficiency.
- Rate Limiting: Implemented rate limiting wrappers to prevent excessive resource calls.
- Human-in-the-Loop: Incorporated breakpoints for human intervention, ensuring accuracy and control.

## Installation for Mac
The following steps are required to save graph rendering localing on the repository.

 Step 1. Follow instructions to install [brew](https://brew.sh) to install packages/tools that are not pre-installed on your laptop.
 Step 2. Run 
 ```brew 
 brew install graphviz
 ```
 Step 3. Per [PyGraphviz](https://pygraphviz.github.io/documentation/stable/install.html) run
 ```bash 
    pip install --config-settings="--global-option=build_ext" \
                    --config-settings="--global-option=-I$(brew --prefix graphviz)/include/" \
                    --config-settings="--global-option=-L$(brew --prefix graphviz)/lib/" \
                    pygraphviz
```

# LLM-Agents

## Simple ReAct Agent
A ReAct model is a an Agent that performs both Reasoning and Actions task, based on [[1]](#reference). This project implements as simplified ReAct pattern from scratch using python. The main essense of this framework is as follows:
1. LLM thinks on what to do
2. Decides on what action to take 
3. Execute that actions (or calls an external tool to take the action) 
4. An observations is returned 
5. Repeat from (2)

The [Simple ReAct Agent](./simpleReactAgent/) directory showcases two approches.
1. `agent.py`: The ReAct framework from scratch utilizing prompting and output parsing.
2. `agentoptimized.py`: Use native langchain modules with AgentExecutor. 

## LangGraph Agent

Visual of the simple Langgraph Agent utilizing a search tool that leverages the TavillySearch API. 
* code: [`/langGraphAgent/graphagent.py`](./langGraphAgent/graphagent.py)

### Known Issues
The `take_action()` method/node has a failsafe to invoke the LLM and have it pass the required arguments for the tool call. In `langchain-openai>=0.1.21rc1` there is a new kwarg [`struct=True`](https://python.langchain.com/v0.2/docs/integrations/chat/openai/#stricttrue) to enforce the tools argument schema.

### Persistance ("memory") To Graph
Some Applications need memory to share context across multiple interactions/sessions. In LangGraph, memory is provided for any StateGraph through Checkpointers such as `SqliteSaver`. This checkpointer is used as an in-memory database, if your machine memory is a concern LangGraph we can use *Redis* as our cache application

This is an important feature, for example, when building a customer facing chatbot and the requirements are to have the chatbot recall previous states of the conversation and have the user resume from that state.

### State Memory
With state memory the Agent can be invoked from any section of its graph with the use of its history and checkpoints.

## Mid-Execution Failures
Programs fail, it happens. Fortunately, with the use of our memory/checkpoint we can make necessary updates to our code, re-initiate our class, and start from a saved checkpoint. 

Suppose you are working with the [`Agent`](/langGraphAgent/graphagent.py) and you have some "bad code" in the `take_action` method:

```python
Class Agent:
...
   def take_action(self, state: AgentState):
      raise()
      ...
   ...
```

Depending on the size of the graph and/or costs it does not make sense to start the execution from the beginning. Instead, we would like to resume from the faulty state after making the neccessary fixes. This is made possible with the thread config and memory/checkpoint.

```python
# Fix method
Class Agent:
...
   def take_action(self, state: AgentState):
      #raise()
      ...
   ...

# Initiate Agent class
abot = Agent(model, [tool], system=prompt, checkpointer=memory)

# Current/Next stage
print(f"Graph will start from current configuration and run the following stage in the graph: {abot.graph.get_state(thread).next}")

# Run from latest checkpoint
for event in abot.graph.stream(input=None, config=thread):
   for v in event.values():
      print(v)
```
## Agent Updates (Time-Travel)
Additionally, Agent states allow us to time-travel to a particular point on the graph with the use of the `thread_ts`. This key identifies a place in the state within the current thread.

We can use the iterator `graph.get_state_history(thread)` to obtain the `thread_ts` and use it to invoke/stream our agent from that state on the graph.

```python
for event in abot.graph.stream(input=None, config={"configurable": {"thread_id": "1", "thread_ts": {value}}):
   for v in event.values():
      print(v)
```

This is useful for a few reasons updates to future nodes in the graph and modification of intermediate stages within the graph. For the latter you can get the state, with the use of the `thread_ts`, modify it, and then update the history using:

```python
current_values = abot.graph.get_state(thread)

# ... modify current_values

graph.update_state(thread, current_values.values)
```

### Breakpoints (Human-In-The-Loop)
Human in the Loop are essential interations between person(s) and LLM-Agents. Adding breakpoints in the graph, allow it to stop at specific nodes, seek human intervention/approval before proceeding. This can be used when there is a sensitive step that will happen next, and we require final approval/modification from a live person.

[Interactive Python Example](/langGraphAgent/humanloopagent.py)

### Graph Visualization
Run python script with flag `--savegraph`.
![image](langGraphAgent/visual/graphagent.png)

# Reference

[1]: Google Research. "React: Synergizing Reasoning and Acting in Language Models." Google AI Blog, 4 Aug. 2023, [link](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/).

[2]: Madaan, A. et.al. "Self-Refine: Iterative Reginement with Self-Feedback." 2023, [link](https://selfrefine.info)

[3]: Ridnik, T. et al. "Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering" 16 Jan. 2024, [link](https://arxiv.org/pdf/2401.08500)

# Contributions
This repo follows the `deeplearning.ai` course "AI Agents in LangGraph", with some modifications.
