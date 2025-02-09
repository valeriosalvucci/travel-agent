import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
import serpapi


from smolagents import LiteLLMModel, HfApiModel, CodeAgent, ToolCallingAgent
from smolagents import DuckDuckGoSearchTool, PythonInterpreterTool, tool, Tool
from typing import Optional
import os

from dotenv import load_dotenv
load_dotenv()

# print(os.environ['ANTHROPIC_API_KEY'])

# model = LiteLLMModel(model_id="gpt-3.5-turbo-0125", api_key=os.environ['OPENAI_API_KEY'])
# model = LiteLLMModel(model_id="gpt-4o", api_key=os.environ['OPENAI_API_KEY'])
# print(os.environ.get('USE_GOOGLE_API',"YOOO"))

# if os.environ.get('USE_GOOGLE_API',True):
#     model = LiteLLMModel(model_id="gemini/gemini-2.0-pro-exp" , api_key=os.environ['GOOGLE_API_KEY'])
# else:
# model = LiteLLMModel(model_id="claude-3-haiku-20240307", api_key=os.environ['ANTHROPIC_API_KEY'])

# if os.environ.get('USE_GOOGLE_API',True):
model = LiteLLMModel(model_id="gemini/gemini-2.0-pro-exp" , api_key=os.environ['GOOGLE_API_KEY'])
# else:
#model = LiteLLMModel(model_id="claude-3-haiku-20240307", api_key=os.environ['ANTHROPIC_API_KEY'])

agent = ToolCallingAgent(tools=[DuckDuckGoSearchTool()], model=model)
# agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

def make_activities(location, daterange, comments):
    agent.run(f"""
Find activities to do in {location} on {daterange}, considering user comments {comments}
""")
    return agent.memory


def make_restaurants(location, daterange, comments):
    api_key= "96eca78c229bbf08125eb97742e57715c02f2aaf0754ea0be60e6b7d8385fb2d"
    # from serpapi import GoogleSearch
    params = {
    "engine": "google",
    "q": "find 10 restaurants in {location}",
    "api_key": api_key
    }
    results = serpapi.search(params)

    r =  agent.run(f"extract restaurants from {results} considering {comments}")

    return r

def make_events(location, daterange, comments):
    r = agent.run(f"""
Find events to in {location} on {daterange}, considering preferences, 
if any, in user comments {comments}
""")
    return r


def summarize_itinerary(location, daterange, comments, activities, restaurants, events):
    r = agent.run(f"""
Create an itinerary in location {location} on {daterange}, 
for a user that expressed a desire for {comments if comments else 'no preferences'},
given these possible activities {activities}, and events {events}
""")
    return r

def make_fe(location, daterange, comments, activities, restaurants, events):
    r = agent.run(f"""
Plan a travel itinerary trip for me that includes two types of things to do in the itinerary: 
Activities to do on that given day, and events to attend on that given day. 
You will be provided with the following information to help tune my trip: 
My destination:  {location}
When I am planning to travel: {daterange},
List of possible activities {activities}
List of possible events {events}
Format the output as a web page that uses vanilla html and css .
{comments if comments else 'no preferences'},
""")
    return r

# @app.post("/upload")
# async def upload(
#     destination: str, daterange: str, comments: str
# ):
#     places = []
#     restaurants = []
#     activities = []
    
#     activities = make_activities(destination, daterange, comments)
#     result = f"""
#     here are my suggestions for {daterange} in {destination}, considering your comments: {comments}
#     places {places}
#     restaurants {restaurants}
#     activities {activities}
#     """
    # return result


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



# from typing import Optional
# from smolagents import CodeAgent, HfApiModel, tool

# @tool
# def get_travel_duration(start_location: str, destination_location: str, departure_time: Optional[int] = None) -> str:
#     """Gets the travel time in car between two places.
    
#     Args:
#         start_location: the place from which you start your ride
#         destination_location: the place of arrival
#         departure_time: the departure time, provide only a datetime.datetime if you want to specify this
#     """
#     import googlemaps
#     import os
#     from datetime import datetime

#     gmaps = googlemaps.Client(os.getenv("GMAPS_API_KEY"))

#     if departure_time is None:
#         departure_time = datetime.now()

#     directions_result = gmaps.directions(
#         start_location,
#         destination_location,
#         mode="transit",
#         departure_time=departure_time
#     )
#     return directions_result[0]["legs"][0]["duration"]["text"]

# # Initialize the agent with the custom tool
# agent = CodeAgent(tools=[get_travel_duration], model=HfApiModel(), additional_authorized_imports=["datetime"])

# # Run the agent with a travel planning request
# agent.run("Can you give me a nice one-day trip around Paris with a few locations and the times? Co
          
# from smolagents import CodeAgent, HfApiModel, GoogleSearchTool

# # Initialize the agent with the search tool and the Hugging Face model
# google_search = GoogleSearchTool() # Requires SerpAPI key in environment variables

# agent = CodeAgent(
#     tools=[google_search], 
#     model=HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct",token="<your_hf_token>")
#     )
