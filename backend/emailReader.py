import json
from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/emails")
def get_emails():
    with open(r"backend\emails.json","r") as f:
        inbox = json.load(f)
    return inbox

@app.get("/emails/{email_id}")
def get_email(email_id: int):
    with open(r"backend\emails.json", "r") as f:
        inbox = json.load(f)
    email = next((e for e in inbox if e["id"] == email_id), None)
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return email
    