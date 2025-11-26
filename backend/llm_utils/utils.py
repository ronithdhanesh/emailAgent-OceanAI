from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

def categorize_email(email, prompts):
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

    categorization_prompt = prompts["categorization"]

    email_text = f"""
      Subject: {email['subject']}
      From: {email['sender']}
      Body: {email['body']}
      """

    prompt = ChatPromptTemplate.from_template("""
You are an email categorization model.

Follow these rules:
{categorization_prompt}

Email:
{email_text}

Return ONLY one word:
Important, To-Do, Newsletter, or Spam.
Do NOT return explanations.
""")

    chain = prompt | llm | StrOutputParser()

    category = chain.invoke({
        "categorization_prompt": categorization_prompt,
        "email_text": email_text
    })

    return category.strip()


def extract_action_items(email, prompts, category):
    if category != "To-Do":
        return []
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

    action_prompt = prompts["action_item"]

    email_text = f"""
                  Subject: {email['subject']}
                  From: {email['sender']}
                  Body: {email['body']}
                  """

    prompt = ChatPromptTemplate.from_template("""
        You extract action items from emails.

        Follow these instructions strictly:
        {action_prompt}

        Email:
        {email_text}

        Return ONLY valid JSON. No explanation. No markdown. No text before or after.
        """)
    chain = prompt | llm | StrOutputParser()

    raw_output = chain.invoke({
        "action_prompt": action_prompt,
        "email_text": email_text
    }).strip()
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    if raw_output == "[]":
        return []
    try:
        data = json.loads(raw_output)
        return data
    except json.JSONDecodeError:
        print("⚠️ Warning: Model returned malformed JSON. Raw output:", raw_output)
        repaired = raw_output
        repaired = repaired.replace(",}", "}").replace(",]", "]")

        try:
            return json.loads(repaired)
        except:
            
            return []


def generate_auto_reply(email, prompts):
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

    auto_reply_prompt = prompts["auto_reply"]

    email_text = f"""
        Subject: {email['subject']}
        From: {email['sender']}
        Body: {email['body']}
    """

    prompt = ChatPromptTemplate.from_template("""
You generate short, professional email replies.

Follow these rules strictly:
{auto_reply_prompt}

Email you are replying to:
{email_text}

Return ONLY the reply body. 
Do NOT include greetings like "Hi," unless needed.
Do NOT include the sender name.
Do NOT include markdown.
    """)

    chain = prompt | llm | StrOutputParser()

    reply_text = chain.invoke({
        "auto_reply_prompt": auto_reply_prompt,
        "email_text": email_text
    }).strip()

    return reply_text

prompts = {
  "categorization": "You are an email categorization model. You must choose exactly ONE of these categories:\n- Important\n- Newsletter\n- Spam\n- To-Do\n\nRules:\n- Only mark an email as To-Do if it VERY CLEARLY says something like: \"Please do this immediately\" or explicitly assigns a task.\n- If the email only mentions general information, reminders, or casual requests, do NOT consider it To-Do.\n- Emails from coworkers, bosses, or clients that do not contain explicit instructions should be marked Important.\n- Company announcements or updates should be Newsletter.\n- Suspicious, promotional, or unwanted content is Spam.\n\nReturn only one category name as a single word.",

  "action_item": "Extract action items ONLY IF the email contains a very explicit task such as: \"You must do this\", \"I need you to\", \"Please complete this task by...\", or \"Your responsibility is...\".\n\nIf the email does NOT contain a very explicit instruction, return an empty JSON array: []\n\nIf there is an explicit task, respond in strict JSON only with the format:\n{\n  \"task\": \"...\",\n  \"deadline\": \"...\"\n}",

  "auto_reply": "Write a polite and short reply. Keep the tone friendly and non-committal.\nIf the email does not contain a direct request, simply acknowledge the message.\nReturn only the email body, no metadata."
}


# email =  {
#     "id": 1,
#     "sender": "boss@example.com",
#     "subject": "Project Update",
#     "timestamp": "2025-01-03 10:20",
#     "body": "Hey, can you send the weekly update by tomorrow?"
# }
email = {
  "subject": "Quick Question",
  "sender": "colleague@example.com",
  "body": "Hey, when you get time, could you take a quick look at the latest report?"
}




category = categorize_email(email, prompts)
action_item = extract_action_items(email,prompts, category)
auto_reply = generate_auto_reply(email, prompts)
print("CATEGORY:", category)
print('Action-item:', action_item)
print('Auto-Reply:', auto_reply)
