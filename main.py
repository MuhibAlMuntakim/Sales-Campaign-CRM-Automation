from crewai import Crew
from agents import supervisor, verifier, outreach  # ✅ Import Agents
from tasks import assign_task, verify_task, outreach_task, report_task  # ✅ Import Tasks

# ------------------- Create the CrewAI Workflow -------------------
lead_management_crew = Crew(
    agents=[supervisor, verifier, outreach],  # ✅ Assigning all agents
    tasks=[assign_task, verify_task, outreach_task, report_task]  # ✅ Assigning all tasks
)

# ------------------- Start the Workflow -------------------
if __name__ == "__main__":
    print("\n🚀 Starting AI-Powered Lead Management Workflow...\n")
    lead_management_crew.kickoff()
    print("\n✅ Workflow completed successfully!\n")
