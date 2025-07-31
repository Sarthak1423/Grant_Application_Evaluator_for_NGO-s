# phi_app.py
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# You can change "gemini-2.0-flash-exp" to "gemini-1.5-pro-latest" if needed
gemini_model = Gemini(id="gemini-2.0-flash-exp")

tools = [DuckDuckGo()]  # If needed for impact/justification sourcing

eligibility_agent = Agent(
    name="EligibilityCheckerAgent",
    model=gemini_model,
    tools=tools,
    markdown=True,
    instructions=(
        "You are an eligibility checker for government grants. "
        "Check if the NGO proposal meets basic criteria such as:\n"
        "- Registered status\n- Budget range\n- Thematic fit\n- Geographic relevance\n\n"
        "Respond with YES/NO for each and explain briefly."
    ),
)

impact_agent = Agent(
    name="ImpactEvaluatorAgent",
    model=gemini_model,
    tools=tools,
    markdown=True,
    instructions=(
        "You are a grant evaluator tasked with assessing project impact. "
        "Analyze:\n1. Target beneficiaries\n2. Scalability\n3. Innovation\n4. Expected outcomes\n\n"
        "Return a clear, paragraph-based assessment."
    ),
)

scoring_agent = Agent(
    name="ScoringAgent",
    model=gemini_model,
    tools=tools,
    markdown=True,
    instructions=(
        "Based on a grant proposal, assign a score out of 10 and justify it clearly. "
        "Criteria include clarity, alignment, impact, and feasibility."
    ),
)
