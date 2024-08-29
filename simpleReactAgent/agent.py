import re

import os.path as osp
import sys
import json

from openai import OpenAI

from pydantic import BaseModel
from typing import Dict, List, Optional, Any

file_dir = osp.dirname(__file__)
sys.path.insert(0, file_dir)


class ReActAgent(BaseModel):
    prompt: Dict[str, str]
    system: Optional[str] = None
    messages: Optional[List[Dict]] = []
    model: str = 'gpt-4o'
    action_re: Any = None

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
    
    def parseaction(self):
        self.action_re = re.compile('^Action: (\\w+): (.*)$')   # python regular expression to selection action
    
    def query(self, question:str, max_turns:int =5, i: int = 0):
        self.parseaction()
        next_prompt = question
        while i < max_turns:
            i += 1
            result = self(next_prompt)
            print(result)
            actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
            if actions:
                # There is an action to run
                action, action_input = actions[0].groups()
                if action not in known_actions:
                    raise Exception("Unknown action: {}: {}".format(action, action_input))
                print(" -- running {} {}".format(action, action_input))
                observation = known_actions[action](action_input)
                print("Observation:", observation)
                next_prompt = "Observation: {}".format(observation)
            else:
                print('END \n')
                return
    

if __name__ == "__main__":
    import json

    from tools.agenttools import average_dog_weight, calculate
    known_actions = {
        "calculate": calculate,
        "average_dog_weight": average_dog_weight
    }

    prompt_dict = json.load(open(osp.join(file_dir, 'config/prompts.json'), 'r'))
    agent = ReActAgent(
        prompt=prompt_dict
    )
    agent.setup()
    agent.query("How much does a toy poodle weigh?")
    agent.query("I have 2 dogs, a border collie and a scottish terrier. What is their combined weight")