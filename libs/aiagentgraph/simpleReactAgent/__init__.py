import openai
import os

def check_client_api():
		if bool(os.getenv('OPENAI_API_KEY')):
			pass
		else:
			raise openai.OpenAIError('The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable')

check_client_api()
