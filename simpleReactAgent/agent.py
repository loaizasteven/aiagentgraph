import openai
import re
import httpx

import os
import os.path as osp
import sys
import json

from openai import OpenAI

from pydantic import BaseModel
from typing import Dict, List, Optional

file_dir = osp.dirname(__file__)
sys.path.insert(0, file_dir)


class ReActAgent(BaseModel):
    prompt: Dict[str, str]
    system: Optional[str] = None
    messages: Optional[List[Dict]] = []
    model: str = 'gpt-4o'

    @staticmethod
    def createclient():
        return OpenAI()
    
    def setup(self):
        self.system = self.prompt.get('system_prompt')
        if self.system:
            self.messages.append({"role": "system", "content": self.system})

    def execute(self):
        client = self.createclient()
        completion = client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=self.messages
        )

        return completion.choices[0].message.content
    
    def __call__(self, message:str):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        
        return result
    
if __name__ == "__main__":
    import json

    prompt_dict = json.load(open(osp.join(file_dir, 'config/prompts.json'), 'r'))
    agent = ReActAgent(
        prompt=prompt_dict
    )
    agent.setup()
    response = agent('hi')
    print(response)
