import streamlit as st
import requests
from datetime import datetime

# ---------- STYLING ----------
st.set_page_config(page_title="Smart Inbox AI", layout="wide", page_icon="📨")

# Custom CSS for premium UI
st.markdown("""
<style>
    /* Global background */
    .stApp {
        background: #0e1117;
    }
    /* Card styling */
    .email-card {
        background: rgba(255,255,255,0.04);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: 0.2s ease;
    }
    .email-card:hover {
        border: 1px solid rgba(255,255,255,0.25);
        background: rgba(255,255,255,0.07);
    }
    .category-badge {
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: bold;
        float: right;
        margin-top: -10px;
    }
    .important { background: #ff4d4f22; color: #ff4d4f; }
    .todo { background: #1677ff22; color: #1677ff; }
    .newsletter { background: #13c2c222; color: #13c2c2; }
    .spam { background: #a0a0a022; color: #a0a0a0; }
    .reply-box {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- API ENDPOINTS ----------
API = "http://127.0.0.1:8000"

def fetch_json(route):
    try:
        return requests.get(f"{API}{route}").json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {route}: {e}")
        return []

def post_json(route, data=None):
    try:
        resp = requests.post(f"{API}{route}", json=data)
        if resp.text:
            return resp.json()
        return {"status": "success"}
    except requests.exceptions.RequestException as e:
        st.error(f"Error posting to {route}: {e}")
        return None

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### ✉️ Smart Inbox AI")
    st.write("A modern AI-powered email dashboard.")

    page = st.radio("Navigate", ["Inbox", "Processed Inbox", "Prompt Settings"])
    st.markdown("---")

    if st.button("⚙️ Process Inbox", use_container_width=True):
        post_json("/process_inbox")
        st.success("Processed successfully!")

# ---------- PAGE: INBOX ----------
if page == "Inbox":
    st.markdown("## 📥 Inbox")

    inbox = fetch_json("/emails")

    for email in inbox:
        with st.container():
            st.markdown('<div class="email-card">', unsafe_allow_html=True)

            st.markdown(f"""
            <span class="category-badge newsletter">RAW</span>
            <h3>{email['subject']}</h3>
            <p><b>From:</b> {email['sender']}</p>
            <p><b>Time:</b> {email['timestamp']}</p>
            <hr>
            <p>{email['body']}</p>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)


# ---------- PAGE: PROCESSED INBOX ----------
elif page == "Processed Inbox":
    st.markdown("## 🧠 AI Processed Inbox")

    processed = fetch_json("/process_inbox")

    for email in processed:
        category_class = {
            "Important": "important",
            "To-Do": "todo",
            "Newsletter": "newsletter",
            "Spam": "spam",
        }.get(email.get("category", "newsletter"), "newsletter")

        st.markdown('<div class="email-card">', unsafe_allow_html=True)

        st.markdown(f"""
            <span class="category-badge {category_class}">{email.get('category', 'Unknown')}</span>
            <h3>{email.get('subject', 'N/A')}</h3>
            <p><b>From:</b> {email.get('sender', 'Unknown')}</p>
            <p><b>Time:</b> {email.get('timestamp', 'N/A')}</p>
            <hr>
            <p>{email.get('body', 'No content')}</p>
        """, unsafe_allow_html=True)

        # Action Items
        st.subheader("📝 Action Items")

        action_items = email.get("action_items", [])
        if action_items:
            for idx, item in enumerate(action_items):
                if isinstance(item, dict):
                    st.markdown(f"**{idx+1}. {item.get('task', 'N/A')}**  \n⏳ Deadline: *{item.get('deadline', 'None')}*")
                else:
                    st.markdown(f"**{idx+1}. {item}**")
        else:
            st.write("No action items found.")

        # Auto Reply Button
        if st.button(f"Generate Auto-Reply for Email {email.get('id', 'Unknown')}"):
            reply = post_json(f"/auto_reply/{email.get('id')}")
            if reply:
                st.markdown(
                    f"<div class='reply-box'><b>Generated Reply:</b><br>{reply.get('reply', 'No reply generated')}</div>",
                    unsafe_allow_html=True
                )

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- PAGE: PROMPT SETTINGS ----------
elif page == "Prompt Settings":
    st.markdown("## 🛠 Prompt Settings")

    prompts = fetch_json("/prompts")

    if prompts:
        categorization_text = st.text_area("Categorization Prompt", prompts.get("categorization", ""))
        action_text = st.text_area("Action Item Prompt", prompts.get("action_item", ""))
        reply_text = st.text_area("Auto Reply Prompt", prompts.get("auto_reply", ""))

        if st.button("Save Changes"):
            result = post_json("/prompts", {
                "categorization": categorization_text,
                "action_item": action_text,
                "auto_reply": reply_text
            })
            if result:
                st.success("Prompts updated!")
    else:
        st.error("Failed to load prompts.")