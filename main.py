import streamlit as st
import requests

st.title("Email Inbox")

# Load inbox
inbox = requests.get("http://localhost:8000/emails").json()

# Load processed emails (if any)
processed = requests.get("http://localhost:8000/process_inbox").json()
print("inbox: ",inbox)
print("processed: ", processed)
# Button to process inbox
if st.button("Process Emails"):
    processed = requests.post("http://localhost:8000/process_inbox").json()
    st.session_state["processed"] = processed
    st.success("Emails processed successfully!")

# Use session_state if available
if "processed" in st.session_state:
    processed = st.session_state["processed"]

# Utility: find processed details for an email id
def find_processed(email_id):
    for p in processed:
        if p["id"] == email_id:
            return p
    return None

# Display inbox
for email in inbox:
    with st.expander(f"{email['subject']} — {email['sender']}"):
        st.write(f"**Sender:** {email['sender']}")
        st.write(f"**Time:** {email['timestamp']}")
        st.write("---")
        st.write(email["body"])

        # show processed data if exists
        p = find_processed(email["id"])
        
        if p:
            st.write("---")
            st.subheader("AI Processing Results")

            # Category
            st.markdown(f"**Category:** `{p['category']}`")

            # Action Items
            if p["action_items"]:
                st.write("**Action Items:**")
                for item in p["action_items"]:
                    st.write(f"- {item['task']} (deadline: {item['deadline']})")
            else:
                st.write("No action items found.")
