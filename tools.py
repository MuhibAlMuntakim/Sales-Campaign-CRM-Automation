import smtplib
import requests
import os
import imaplib
import email
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import openai

# Load environment variables
load_dotenv()

# Load API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_NAME = os.getenv("SENDER_NAME", "Sampada Gadi")



# ------------------- Notion Lead Management Tool -------------------
class NotionToolInput(BaseModel):
    action: str = Field(..., description="Action to perform: 'fetch' or 'update'.")
    lead_email: str = Field(None, description="Email of the lead to update (required for updates).")
    update_data: dict = Field(None, description="Data to update in Notion (required for updates).")


class NotionTool(BaseTool):
    name: str = "notion_tool"  # ✅ Type annotation added
    description: str = "Interact with Notion database for lead management."  # ✅ Type annotation added
    args_schema = NotionToolInput

    def _run(self, action, lead_email=None, update_data=None):
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        if action == "fetch":
            url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
            response = requests.post(url, headers=headers)
            return response.json()
        elif action == "update" and lead_email:
            url = f"https://api.notion.com/v1/pages/{lead_email}"
            response = requests.patch(url, headers=headers, json={"properties": update_data})
            return response.json()


# ------------------- Email Verification Tool (Hunter.io) -------------------
class EmailVerificationToolInput(BaseModel):
    email: str = Field(..., description="Email address to verify.")


class EmailVerificationTool(BaseTool):
    name: str = "email_verification_tool"  # ✅ Type annotation added
    description: str = "Verify email addresses using Hunter.io API."  # ✅ Type annotation added
    args_schema = EmailVerificationToolInput

    def _run(self, email):
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}"
        response = requests.get(url)
        return response.json().get('data', {}).get('status', 'unknown')


# ------------------- Gmail SMTP Email Tool -------------------
class GmailSMTPToolInput(BaseModel):
    to_email: str = Field(..., description="Recipient email address.")
    subject: str = Field(..., description="Email subject.")
    content: str = Field(..., description="Email body content.")


class GmailSMTPTool(BaseTool):
    name: str = "gmail_smtp_tool"  # ✅ Type annotation added
    description: str = "Send emails using Gmail SMTP."  # ✅ Type annotation added
    args_schema = GmailSMTPToolInput

    def _run(self, to_email, subject, content):
        try:
            msg = MIMEMultipart()
            msg["From"] = SMTP_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(content, "plain"))

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()

            return {"status": "Email sent successfully!"}

        except Exception as e:
            return {"error": str(e)}


# ------------------- Gmail Inbox Monitoring Tool -------------------
class GmailInboxToolInput(BaseModel):
    search_criteria: str = Field(..., description="Search criteria to filter emails (e.g., 'UNSEEN SUBJECT \"New Campaign Task\"').")


class GmailInboxTool(BaseTool):
    name: str = "gmail_inbox_tool"  # ✅ Type annotation added
    description: str = "Monitor Gmail inbox for new campaign task notifications."  # ✅ Type annotation added
    args_schema = GmailInboxToolInput

    def _run(self, search_criteria):
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(SMTP_EMAIL, SMTP_PASSWORD)
            mail.select('inbox')

            result, data = mail.search(None, search_criteria)
            email_ids = data[0].split()

            emails = []
            for num in email_ids[-5:]:
                result, msg_data = mail.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        emails.append({
                            "subject": msg["subject"],
                            "from": msg["from"],
                            "date": msg["date"]
                        })

            mail.logout()
            return emails

        except Exception as e:
            return {"error": str(e)}


# ------------------- OpenAI GPT-4 Email Personalization Tool -------------------
class GPTPersonalizationToolInput(BaseModel):
    lead_name: str = Field(..., description="Lead's name for personalization.")
    company: str = Field(..., description="Lead's company name.")
    industry: str = Field(..., description="Industry of the lead.")

class GPTPersonalizationTool(BaseTool):
    name: str = "gpt_personalization_tool"
    description: str = "Generate personalized outreach messages using OpenAI GPT-4."
    args_schema = GPTPersonalizationToolInput

    def _run(self, lead_name, company, industry):
        # ✅ Load API Key and Sender's Name
        client = openai.Client(api_key=OPENAI_API_KEY)
        SENDER_NAME = os.getenv("SENDER_NAME", "[Your Name]")  # Default if not provided

        # ✅ Create the Email Prompt
        prompt = (
            f"Write a highly personalized email introduction for {lead_name}, "
            f"who works at {company} in the {industry} industry. "
            "The email should be professional, engaging, and under 100 words. "
            "Use the recipient's name at the beginning. End the email with: "
            f"Best regards,\n{SENDER_NAME}"
        )

        # ✅ Use OpenAI Client to Generate Email
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

