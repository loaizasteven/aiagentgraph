import openai
import os
from dotenv import load_dotenv

from pydantic import BaseModel 
_ = load_dotenv()
from openai import OpenAI

client = OpenAI(api_key='')

class Agent(BaseModel):
	system: str = ""
	messages: list = []

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if self.system:
			self.messages.append({"role": "system", "content": self.system})
	
	def __call__(self, message):
		self.messages.append({"role": "user", "content": message})
		result = self.execute()
		self.messages.append({"role": "assistant", "content": result})
		return result

	def execute(self):
		completion = client.chat.completions.create(
                        model="gpt-4o", 
                        temperature=0,
                        messages=self.messages)
		return completion.choices[0].message.content		
