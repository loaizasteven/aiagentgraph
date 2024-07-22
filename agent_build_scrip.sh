#!/usr/bin/python    

# Repo AI-Agent-in-LangGraph
# env
DIRECTORY="agent_env"

function activate () {
  source $HOME/git/AI-Agents-in-LangGraph/agent_env/bin/activate
}

if [ -d "$DIRECTORY" ]; then
    activate
else
    echo "Creating venv"
    /usr/local/bin/python3 -m venv "$DIRECTORY"
fi