from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages.tool import ToolCall

from typing import Dict, Union, List
from langchain_core.tools import tool

@tool
def search_tool(max_results: int, input:Union[str,Dict, ToolCall]) -> List:
    """Tool search for information from Tavillly search api
    Args:
        max_results: "Number of returned articles, default to 3 if unsure"
        input:"The query for the search tool"
    Return
        List of results
    """
    search =TavilySearchResults(max_results=max_results)
    try:
        results = search.invoke(input)
        getContent = lambda x:x.get('content')

        return list(map(getContent, results))
    except (AttributeError):
        return [results]
