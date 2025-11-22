import streamlit as st
import requests

st.title("Inbox Viewer")

emails = requests.get("http://localhost:8000/emails").json()

for email in emails:
    if st.button(f"{email['subject']} — {email['sender']}", key=email['id']):
        st.session_state['selected_email'] = email['id']
        # print(st.session_state['selected_email'])

        
if 'selected_email' in st.session_state:
    email = requests.get(
        f"http://localhost:8000/emails/{st.session_state['selected_email']}"
    ).json()

    st.subheader(email["subject"])
    st.write(email["body"])
