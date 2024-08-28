import openai
import re
import httpx

import os
import os.path as osp
import sys
import json

from langchain_openai import OpenAI

from pydantic import BaseModel
from typing import Dict

file_dir = osp.dirname(__file__)
sys.path.insert(0, file_dir)


class ReActAgent(BaseModel):
    prompt: Dict[str, str]

    @staticmethod
    def createclient():
        return OpenAI()

if __name__ == "__main__":
    import json

    prompt_dict = json.load(open(osp.join(file_dir, 'config/prompts.json'), 'r'))

    agent = ReActAgent(
        prompt=prompt_dict
    )
    agent.createclient