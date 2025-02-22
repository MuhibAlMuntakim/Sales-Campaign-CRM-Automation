from crewai import Agent, LLM
from tools import NotionTool, EmailVerificationTool, GmailSMTPTool, GmailInboxTool, GPTPersonalizationTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Define OpenAI LLM
openai_llm = LLM(model="gpt-4-turbo")

# ------------------- Supervisor Agent -------------------
supervisor = Agent(
    name="Supervisor Agent",
    role="Manages and oversees the entire lead generation process, including task delegation and reporting.",
    goal="Ensure that leads are processed efficiently and stakeholders receive timely updates.",
    backstory="An AI leader capable of monitoring emails, managing Notion records, and communicating via Gmail.",
    tools=[NotionTool(), GmailInboxTool(), GmailSMTPTool(), GPTPersonalizationTool()],
    allow_delegation=True,  # ✅ Allow delegation to Verifier and Outreach agents
    llm=openai_llm,
    verbose=True  # ✅ Enable detailed output for debugging
)

# ------------------- Verifier Agent -------------------
verifier = Agent(
    name="Lead Verifier Agent",
    role="Responsible for verifying the email addresses and details of all leads.",
    goal="Ensure that only valid leads are processed for outreach.",
    backstory="An AI expert in email verification using Hunter.io and updating lead status in Notion.",
    tools=[NotionTool(), EmailVerificationTool()],
    llm=openai_llm,
    verbose=True  # ✅ Enable detailed output for debugging
)

# ------------------- Outreach Agent -------------------
outreach = Agent(
    name="Outreach Agent",
    role="Handles personalized email outreach and tracks lead responses.",
    goal="Engage verified leads and record their responses in Notion.",
    backstory="An AI sales representative skilled in crafting personalized emails using OpenAI GPT-4.",
    tools=[GmailSMTPTool(), GPTPersonalizationTool(), NotionTool()],
    llm=openai_llm,
    verbose=True  # ✅ Enable detailed output for debugging
)
