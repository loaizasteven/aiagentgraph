from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages.tool import ToolCall

from typing import Dict, Union, List
from langchain_community.tools import BaseTool


class search_tool(BaseTool):
    """Uses Tavily Search API, assumes TAVILY_API_KEY is set in env variables

    Attributes:
        max_results: Limit returned search results. Defaults to 4.
        name: string name representation
        search: Instance of Tavily Search API
    """
    max_results: int = 4
    name: str = 'search_tool'
    description: str = 'This tool search information from the Tavily Search API to provide context to LLMs for user queries'
    search: TavilySearchResults = TavilySearchResults(max_results=max_results)

    def _run(self):
        pass

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
