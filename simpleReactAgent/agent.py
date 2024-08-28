import openai
import re
import httpx

import os
import os.path as osp
import sys
import json

from langchain_openai import OpenAI

from pydantic import BaseModel
from typing import Dict, List, Optional

file_dir = osp.dirname(__file__)
sys.path.insert(0, file_dir)


class ReActAgent(BaseModel):
    prompt: Dict[str, str]
    system: Optional[str] = None
    message: Optional[List[Dict]] = None

    @staticmethod
    def createclient():
        return OpenAI()
    
    def setup(self):
        self.system = self.prompt.get('system_prompt')
        if self.system:
            self.message.append({"role": "system", "content": self.system})


if __name__ == "__main__":
    import json

    prompt_dict = json.load(open(osp.join(file_dir, 'config/prompts.json'), 'r'))
    print(prompt_dict)
    agent = ReActAgent(
        prompt=prompt_dict
    )
    agent.createclient()
    agent.setup()