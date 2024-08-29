# Introduction
The `agent.py` script is based on the [Python React Pattern](https://til.simonwillison.net/llms/python-react-pattern) notebook from Simon Willison, with modifications on the formatting of the directory and structure of the codebase. We leverage the use of Pydantic throughout this codebase.

## Agent
ReAct from scratch. Develop an Agent class to invoke the OpenAI client, with a highly curated system prompt, and parsing logic to mirror the ReAct framework iterations.

## AgentOptimized
Native `langchain` modules to reach the same conclusion as [`agent.py`](#agent) with less custom code and fewer lines of code.

This section utilizes a generic system prompt with placeholders for {tools} that are supplied to the LLM and an {agent_scratchpad} for the LLM to return its thinking process. These placeholders are defined by the langchain modules, see [2](#references).

Noteworthy changes:
1. Must add a tool decorator to the functions defined in [agenttools](./tools/agenttools.py), and include a descrption to provide context to the LLM on intended usage. The more information the better the results.
2. The AgentExectutor [3](#references), is the native langchain version of the agent defined in the section above.

## Getting Started with OpenAI API
Set up openai API key as an env variable, otherwise packages will raise an error.
```bash
export OPENAI_API_KEY='your-api-key-here'
```
Review the official documentation at [Open AI Developer Quickstart](https://platform.openai.com/docs/quickstart).


## References:
1. [Langchain Hub](https://smith.langchain.com/hub): Central location for the community to explore and contribute prompts to the community hub.
2. [ReAct Module](https://api.python.langchain.com/en/latest/agents/langchain.agents.react.agent.create_react_agent.html): Create an agent that uses ReAct prompting. Based on paper “ReAct: Synergizing Reasoning and Acting in Language Models” 
