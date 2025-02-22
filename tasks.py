from crewai import Task
from agents import supervisor, verifier, outreach
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
STAKEHOLDER_EMAIL = os.getenv("STAKEHOLDER_EMAIL", "default@example.com")  # ✅ Use a default for safety

# ------------------- Task 1: Monitor and Assign Leads -------------------
assign_task = Task(
    name="Monitor and Assign Leads",
    agent=supervisor,
    description="""
    The Supervisor Agent monitors Gmail inbox for new campaign notifications and Notion for new leads with 'Pending' status.
    Tasks:
    1. Check Gmail inbox for emails with subject 'New Campaign Task'.
    2. Fetch leads from Notion where 'Email Verified'is no or 'Response Status' is 'Pending'.
    3. Assign leads with unverified emails to the Verifier Agent.
    4. Assign leads with verified emails to the Outreach Agent.
    """,
    expected_output="Successfully assigned leads to Verifier and Outreach agents."
)

# ------------------- Task 2: Verify Email Addresses -------------------
verify_task = Task(
    name="Verify Lead Emails",
    agent=verifier,
    description="""
    The Verifier Agent verifies lead email addresses using Hunter.io and updates Notion.
    Tasks:
    1. Fetch leads from Notion where 'Email Verified' is 'No'.
    2. Use Hunter.io to check email validity.
    3. Update Notion with 'Yes' or 'No' in 'Email Verified' and add notes if needed.
    """,
    expected_output="Updated Notion with verified email statuses."
)

# ------------------- Task 3: Perform Email Outreach -------------------
outreach_task = Task(
    name="Perform Email Outreach",
    agent=outreach,
    description="""
    The Outreach Agent sends personalized emails using OpenAI GPT-4 and Gmail SMTP, and records lead responses.
    Tasks:
    1. Fetch leads from Notion where 'Email Verified' is 'Yes' and 'Response Status' is 'Pending'.
    2. Generate personalized emails using GPT-4.
    3. Send emails via Gmail SMTP.
    4. Monitor responses: 'Interested', 'Not Interested', or 'No Response'.
    5. Update Notion with the response and add notes if applicable.
    """,
    expected_output="Successfully sent personalized emails and recorded responses in Notion."
)

# ------------------- Task 4: Generate Summary Report -------------------
report_task = Task(
    name="Generate and Email Summary Report",
    agent=supervisor,
    description=f"""
    The Supervisor Agent consolidates lead processing results and emails a summary to stakeholders.
    Tasks:
    1. Fetch all lead statuses from Notion.
    2. Generate a summary including total leads, verified emails, and response outcomes.
    3. Use GPT-4 to create a well-structured email report.
    4. Send the report to the stakeholder's email: {STAKEHOLDER_EMAIL}
    """,
    expected_output="Summary report emailed to stakeholders."
)
