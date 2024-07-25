from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages.tool import ToolCall

from typing import Dict, Union, List
from pydantic import BaseModel


class search_tool(BaseModel):
    """Uses Tavily Search API, assumes TAVILY_API_KEY is set in env variables

    Attributes:
        max_results: Limit returned search results. Defaults to 4.
        name: string name representation
        search: Instance of Tavily Search API
    """
    max_results: int = 4
    name: str = 'search_tool'
    search: TavilySearchResults = TavilySearchResults(max_results=max_results)

    def invoke(self, input:Union[str, Dict, ToolCall])-> List:
        """Wrapper for native invoke, reducting the output content.

        Args:
            input: The input to the Runable.

        Returns:
            A List of the search results content.
        """
        results = self.search.invoke(input)
        getContent = lambda x:x.get('content')

        return list(map(getContent, results))
