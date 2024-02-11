import os

from dotenv import load_dotenv

# Import the OpenAIChat model and the Agent struct
from swarms.models import OpenAIChat
from swarms.structs import Agent

# Load the environment variables
load_dotenv()

# Get the API key from the environment
api_key = os.environ.get("OPENAI_API_KEY")

# Initialize the language model
llm = OpenAIChat(
    temperature=0.5,
    model_name="gpt-4",
    openai_api_key=api_key,
    max_tokens=1000,
)

## Initialize the workflow
agent = Agent(
    llm=llm,
    max_loops=1,
    autosave=True,
    dashboard=False,
    streaming_on=True,
    verbose=True,
)

# Run the workflow on a task
agent.run("Generate a 10,000 word blog on health and wellness.")
..............................................................