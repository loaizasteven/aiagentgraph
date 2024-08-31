#!/usr/bin/python    

REPO="aiagentgraph"
# env
DIRECTORY="agent_env"

function activate () {
  source $HOME/git/$REPO/$DIRECTORY/bin/activate
  # logging info
  echo "Currently activated $VIRTUAL_ENV"
  python --version
  # pip installation
  pip install --upgrade pip
  echo "pip installation in quiet mode..."
  pip install -q -r libs/requirements.txt --upgrade-strategy only-if-needed
}

if [ -d "$DIRECTORY" ]; then
    activate
else
    echo "Creating venv"
    /usr/local/bin/python3 -m venv "$DIRECTORY"

    activate
fi