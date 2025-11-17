import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent, Dispatcher
from google.adk.models.lite_llm import LiteLlm
from production_agent.google_maps_tool import google_maps_tool
import google.auth

# Load environment variables
root_dir = Path(__file__).parent.parent
dotenv_path = root_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Configure Google Cloud
try:
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
except Exception:
    pass

os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "europe-west1")

# Configure model connection
gemma_model_name = os.getenv("GEMMA_MODEL_NAME", "gemma3:270m")
api_base = os.getenv("OLLAMA_API_BASE", "localhost:10010")  # Location of Ollama server

# Production Gemma Agent - GPU-accelerated conversational assistant
# Set as root agent
root_agent = production_agent# Agent to handle Google Maps
google_maps_agent = Agent(
    model=LiteLlm(model=f"ollama_chat/{gemma_model_name}", api_base=api_base),
    name="google_maps_agent",
    description="An agent that can provide directions and information about locations using Google Maps.",
    instruction="""You are a helpful assistant that can provide directions and information about locations using Google Maps.
    You can answer questions about:
    - How to get from one place to another.
    - The distance between two locations.
    - The estimated travel time.
    - Information about specific places (e.g., restaurants, landmarks).

    You have access to a Google Maps tool to retrieve this information.
    """,
    tools=[google_maps_tool],
)

# Create a dispatcher to route requests to the appropriate agent
root_agent = Dispatcher(
    model=LiteLlm(model=f"ollama_chat/{gemma_model_name}", api_base=api_base),
    agents=[production_agent, google_maps_agent],
)
