import json 
from fastapi import FastAPI, HTTPException

app = FastAPI()

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