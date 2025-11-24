from fastapi import FastAPI, HTTPException
from backend.utils.categorize import load_inbox, load_email, load_prompts, save_processed_emails
from backend.utils.processor import categorize_email, extract_action_items
import json


app = FastAPI()

@app.get("/emails")
def get_emails():
    inbox =  load_inbox()
    return inbox

@app.get("/emails/{email_id}")
def get_email(email_id:int):
    email = load_email(email_id)
    return email

@app.get("/prompts")
def get_prompts():
    prompts = load_prompts()
    return prompts


@app.post("/prompts")
def update_prompts(prompts: dict):
    with open("backend/prompts.json", "w") as f:
        json.dump(prompts, f, indent=2)
        return {"status" : "ok"}

@app.post("/process_inbox")
def process_inbox():
    inbox = load_inbox()
    prompts = load_prompts()

    processed = []

    for email in inbox:
        category = categorize_email(email, prompts)
        action_items = extract_action_items(email, category, prompts)

        email_result = {
            "id": email["id"],
            "sender": email["sender"],
            "subject": email["subject"],
            "body": email["body"],
            "timestamp": email["timestamp"],
            "category": category,
            "action_items": action_items
        }

        processed.append(email_result)

    save_processed_emails(processed)

    return processed




