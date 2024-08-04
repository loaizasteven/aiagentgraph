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

## Simple Reach Agent

## LangGraph Agent

Visual of the simple Langgraph Agent utilizing a search tool that leverages the TavillySearch API.

![image](langGraphAgent/visual/graphagent.png)

# Reference

[1]: Google Research. "React: Synergizing Reasoning and Acting in Language Models." Google AI Blog, 4 Aug. 2023, [link](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/).

[2]: Madaan, A. et.al. "Self-Refine: Iterative Reginement with Self-Feedback." 2023, [link](https://selfrefine.info)

[3]: Ridnik, T. et al. "Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering" 16 Jan. 2024, [link](https://arxiv.org/pdf/2401.08500)