#!/usr/bin/python    

# Repo AI-Agent-in-LangGraph
# env
DIRECTORY="agent_env"
if [ -d "$DIRECTORY" ]; then
    echo "agent venv exist, activating the env"
    source "$DIRECTORY"/bin/activate
else
    echo "Creating venv"
    /usr/local/bin/python3 -m venv "$DIRECTORY"
fi