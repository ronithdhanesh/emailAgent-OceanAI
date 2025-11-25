from fastapi import FastAPI, HTTPException
import json 
import requests
from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent

def load_inbox():
    with open(BACKEND_DIR / "emails.json",'r') as f: 
        inbox = json.load(f)
        return inbox
    
def load_email(email_id:int):
    with open(BACKEND_DIR / "emails.json",'r') as f:
        inbox = json.load(f)
    for e in inbox:
        if e["id"] == email_id:
            email = e
            break
    return email

def load_prompts():
    with open(BACKEND_DIR / "prompts.json","r") as f:
        prompts = json.load(f)
        return prompts
    

def save_processed_emails(processed):
    with open(BACKEND_DIR / "saved_processed_emails.json", "w") as f:
        json.dump(processed,f,indent=2)

def load_processed_inbox():
    with open(BACKEND_DIR / "saved_processed_emails.json", "r") as f:
        processed_inbox = json.load(f)
        return processed_inbox