import json
from fastapi import FastAPI, HTTPException


app = FastAPI()

@app.get("/emails")
def get_emails():
    with open("emails.json","r") as f:
        inbox = json.load(f)
    return inbox

@app.get("/emails/{email_id}")
def get_email(email_id: int):
    with open("emails.json", "r") as f:
        inbox = json.load(f)
    email = next((e for e in inbox if e["id"] == email_id), None)
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


#PROMPTS -----------------------------------------------------------------

@app.get("/prompts")
def get_prompts():
    with open("prompts.json","r") as f:
        prompts = json.load(f)
        return prompts
    

@app.post("/prompts")
def update_prompts(prompts: dict):
    with open("prompts.json", "w") as f:
        json.dump(prompts,f,indent=2)

    return {"status" : "ok"}