def categorize_email(email, prompts):
    subject = email["subject"].lower()
    body = email["body"].lower()
    if "meeting" in subject or "meeting" in body:
        return "To-Do"
    elif "newsletter" in subject:
        return "Newsletter"
    elif "promotion" in subject or "offer" in subject:
        return "Spam"
    else:
        return "Important"
    

def extract_action_items(email, category, prompts):
    if category != "To-Do":
        return []
    return [{
        "task": "Follow up on this meeting request",
        "deadline": "N/A"
    }]
