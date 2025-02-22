# Sales Campaign CRM Automation

## 📝 Project Overview
This project is an AI-powered Sales Campaign CRM Automation system designed to streamline lead management and outreach processes. It utilizes CrewAI to coordinate agents responsible for verifying leads, conducting personalized outreach, and summarizing campaign progress. The system integrates with Notion for lead storage, Gmail SMTP for email communication, and OpenAI GPT for email personalization.

## 💡 Key Features
- **Supervisor Agent**: Monitors Gmail inbox for campaign tasks, assigns leads, and sends summary reports.
- **Verifier Agent**: Validates lead emails using Hunter.io and updates Notion.
- **Outreach Agent**: Sends personalized emails using OpenAI GPT and tracks lead responses.
- **Scheduler**: Automates the workflow using APScheduler for periodic checks.

## 🚀 Workflow
1. **Monitoring**: The Supervisor Agent checks Gmail for new campaign task emails.
2. **Lead Processing**:
    - Fetches up to 3 pending leads from Notion.
    - Assigns unverified leads to the Verifier Agent and verified leads to the Outreach Agent.
3. **Verification**: The Verifier Agent verifies emails and updates Notion.
4. **Outreach**: The Outreach Agent sends personalized emails and updates response statuses in Notion.
5. **Reporting**: The Supervisor Agent consolidates results and emails a summary to stakeholders.

## 🛠️ Technologies Used
- **Python**: Core programming language
- **CrewAI**: Agent coordination
- **OpenAI GPT**: Personalized email generation and powering Agents 
- **Notion API**: Lead management
- **Hunter.io API**: Email verification
- **Gmail SMTP**: Sending emails
- **APScheduler**: Workflow automation

## 📂 Project Structure
```
├── agents.py
├── main.py
├── scheduler.py
├── tasks.py
├── tools.py
├── .env
└── README.md
```

## ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/MuhibAlMuntakim/Sales-Campaign-CRM-Automation.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Sales-Campaign-CRM-Automation
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🗝️ Environment Variables
Create a `.env` file and configure the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_notion_database_id
HUNTER_API_KEY=your_hunter_api_key
SMTP_EMAIL=your_email@example.com
SMTP_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
STAKEHOLDER_EMAIL=stakeholder@example.com
```

## 🏃‍♂️ Running the Application
1. **Start the Scheduler:**
   ```bash
   python scheduler.py
   ```
## Manually Trigger the Workflow
2. **Run Main.py:**
```bash
python main.py
```

## 🧩 Use Cases
- Automates lead verification and outreach
- Personalizes email communication
- Reduces manual effort in sales campaigns


---

