from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core._api.beta_decorator import suppress_langchain_beta_warning

from pydantic import BaseModel

#Suppress warning
suppress_langchain_beta_warning()

# Set Limits
rate_limiter = InMemoryRateLimiter(
    requests_per_second=1,  
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)

class ChatOpenAIRateLimited(BaseModel):
    __name__:str = "ChatOpenAIRateLimit"

    def __new__(self):
        return ChatOpenAI(model="gpt-4o", rate_limiter=rate_limiter)


if __name__ == '__main__':
    model = ChatOpenAIRateLimited()
    response = model.invoke('Hello')
    response.pretty_print()