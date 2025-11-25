from fastapi import FastAPI, HTTPException
from utils.categorize import load_inbox, load_email, load_prompts, save_processed_emails, load_processed_inbox
from llm_utils.utils import categorize_email, extract_action_items, generate_auto_reply
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).parent


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
    with open(BACKEND_DIR / "prompts.json", "w") as f:
        json.dump(prompts, f, indent=2)
        return {"status" : "ok"}

@app.post("/process_inbox")
def process_inbox():
    inbox = load_inbox()
    prompts = load_prompts()

    processed = []

    for email in inbox:
        category = categorize_email(email, prompts)
        action_items = extract_action_items(email, prompts, category)

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

@app.get("/process_inbox")
def get_processed_inbox():
    processed_inbox = load_processed_inbox()
    return processed_inbox

@app.post("/auto_reply/{email_id}")
def auto_reply(email_id: int):
    inbox = load_inbox()

    email = next((e for e in inbox if e["id"] == email_id), None)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    prompts = load_prompts()

    try:
        reply = generate_auto_reply(email, prompts)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate auto reply: {str(e)}"
        )

    return {
        "id": email_id,
        "reply": reply
    }


