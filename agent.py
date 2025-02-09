import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from smolagents import LiteLLMModel, HfApiModel, CodeAgent, ToolCallingAgent
from smolagents import DuckDuckGoSearchTool, PythonInterpreterTool, tool, Tool
from typing import Optional
import os

from dotenv import load_dotenv
load_dotenv()

# model = LiteLLMModel(model_id="gpt-3.5-turbo-0125", api_key=os.environ['OPENAI_API_KEY'])
# model = LiteLLMModel(model_id="gpt-4o", api_key=os.environ['OPENAI_API_KEY'])
model = LiteLLMModel(model_id="gemini/gemini-2.0-pro-exp" , api_key=os.environ['GOOGLE_API_KEY'])
# model = HfApiModel(model_id="claude-3-opus-20240229", api_key=os.environ['ANTHROPIC_API_KEY'])

agent = ToolCallingAgent(tools=[DuckDuckGoSearchTool()], model=model)
# agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)
agent.run("Find activities to do in Tokyo on 16/02/2025")

print(agent.memory)



# class DuckDuckGoSearchTool(Tool):
#     name = "web_search"
#     description = """Performs a duckduckgo web search based on your query (think a Google search) then returns the top search results."""
#     inputs = {
#         "query": {"type": "string", "description": "The search query to perform."}
#     }
#     output_type = "string"

#     def __init__(self, *args, max_results=10, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.max_results = max_results
#         try:
#             from duckduckgo_search import DDGS
#         except ImportError:
#             raise ImportError(
#                 "You must install package `duckduckgo_search` to run this tool: for instance run `pip install duckduckgo-search`."
#             )
#         self.ddgs = DDGS()

#     def forward(self, query: str) -> str:
#         results = self.ddgs.text(query, max_results=self.max_results)
#         postprocessed_results = [
#             f"[{result['title']}]({result['href']})\n{result['body']}"
#             for result in results
#         ]
#         return "## Search Results\n\n" + "\n\n".join(postprocessed_results)
    




@tool
def get_weather(location: str, celsius: Optional[bool] = True) -> str:
    """
    Get current weather at a given location.
    Args:
        location: the location
        celsius: whether to use Celsius for temperature
    """
    return f"The weather in {location} is sunny with temperatures around {'10 Celsius' if celsius else '3 Fahrenheit'}."

# class GetWeather(Tool):
#     name = "get_weather"
#     description = """
#         Get current weather at a given location.
#         """
#     inputs = {
#         "location": {
#             "type": "string",
#             "description": "the location (city, area, country)",
#         },
#         "celsius": {
#             "type": "boolean",
#             "description": "if true returns temperature in Celsius, else in Fahrenheit",
#             "nullable": True,
#         }
#     }
#     output_type = "string"

#     def forward(self, location: str, celsius:  Optional[bool] = True):
#         print(f"FROM FUNCTION: location = {location} {type(location)},  celsius = {celsius} {type(celsius)}")
#         return f"The weather in {location} is sunny with temperatures around {'10 Celsius' if celsius else '50 Fahrenheit'}."

# agent = ToolCallingAgent(tools=[DuckDuckGoSearchTool(),GetWeather()], model=model) #, can't manage to pass function arguments properly