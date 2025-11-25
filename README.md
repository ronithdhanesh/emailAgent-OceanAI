📬 Smart Inbox AI

A Prompt-Driven Email Productivity Agent
Streamlit + FastAPI + Gemini LLM

🚀 Overview

Smart Inbox AI is an intelligent, prompt-driven email productivity agent designed to:

Categorize emails

Extract action items

Auto-draft intelligent replies

Provide a chat-based inbox assistant

Allow users to fully customize the agent’s “brain” using editable prompts

The entire system is built with:

Backend: FastAPI

Frontend: Streamlit

LLM: Gemini Flash (via Google Generative AI API)

Storage: JSON-based mock inbox + prompt store

This project satisfies all requirements of the assignment.

📁 Project Structure
.
├── backend
│ ├── backend.py # FastAPI app
│ ├── emails.json # Mock inbox (10–20 emails)
│ ├── prompts.json # Editable prompt brain
│ ├── saved_processed.json # Processed results store
│ └── llm_utils
│ └── utils.py # LLM logic (categorize, action items, reply agent)
│
├── frontend
│ └── app.py # Streamlit UI (Inbox, Agent Chat, Prompts UI)
│
├── main.py # Dev launcher
├── README.md # Project documentation
├── pyproject.toml / uv.lock # Dependencies
└── .env # API keys

🛠️ Setup Instructions
1️⃣ Clone the repository
git clone <your-repo-url>
cd <project-folder>

2️⃣ Install dependencies

Using uv (recommended):

uv sync

Or pip:

pip install -r requirements.txt

3️⃣ Add your API key

Create a .env file:

GOOGLE_API_KEY=your_key_here

▶️ Running the Application
Start Backend (FastAPI)
uvicorn backend.backend:app --reload

Runs on: http://localhost:8000

Start Frontend (Streamlit)
streamlit run frontend/app.py

Runs on: http://localhost:8501

📥 Loading the Mock Inbox

The mock inbox lives at:

backend/emails.json

You can modify or extend this file with additional mock emails.

The UI includes a Process Inbox button that:

Loads all emails

Categorizes them using the categorization prompt

Extracts action items (only if category = To-Do)

Stores processed results in saved_processed.json

Updates the UI automatically

🧠 Prompt Configuration (The Agent Brain)

Prompts are stored in:

backend/prompts.json

Contains:

{
"categorization": "...",
"action_item": "...",
"auto_reply": "...",
"agent_chat": "..."
}

The Prompt Settings panel in the UI allows users to:

Edit prompts

Save changes

Immediately re-process inbox using new logic

All LLM behavior is 100% prompt-driven.

💬 Email Agent (Chat)

The "Email Agent" screen lets users:

Summarize an email

Ask “What tasks do I need to do?”

Generate replies with custom tone

Ask questions about inbox

Use custom prompt brain logic

This is achieved by the agent_chat prompt template.

✉️ Auto-Reply Draft Generation

In the Inbox or Processed Inbox view, users can:

Click Generate Auto-Reply

LLM constructs a reply using:

The auto-reply prompt

The email content

User style constraints

Draft is saved, never sent

🔧 Backend Architecture

The backend provides endpoints for:

✔️ /process-inbox

Loads emails → runs LLM pipelines → stores results.

✔️ /get-emails

Fetches raw inbox.

✔️ /get-processed

Fetches processed (categorized/action-item-extracted) results.

✔️ /generate-reply/{email_id}

Creates a draft reply using the auto-reply prompt.

✔️ /agent-chat

Chat endpoint for summarization, reply suggestions, etc.

🎨 Frontend (Streamlit UI)

The frontend contains:

1️⃣ Sidebar Navigation

Inbox

Processed Inbox

Prompt Settings

Process Inbox button

2️⃣ Inbox Viewer

Each email shows:

Sender

Subject

Timestamp

Body

Category

Action items

Auto-reply button

3️⃣ Processed Inbox

Shows categorized/parsed results.

4️⃣ Prompt Settings Panel

Edit & Save prompts

Immediate effect on processing

5️⃣ Agent Chat

Chatbot that understands inbox via prompts.

🧪 Sample Assets Included
✔️ Mock Inbox

backend/emails.json includes:

Meeting requests

Manager requests

Newsletter

Spam-like promo

Project updates

Follow-ups

To-do request emails

✔️ Default Prompts

backend/prompts.json includes:

Categorization

Action item extraction

Auto-reply drafting

Agent chat behavior
