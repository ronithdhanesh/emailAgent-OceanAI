import streamlit as st
import requests

st.title("Prompts system test")

emails = requests.get("")
prompts = requests.get("http://127.0.0.1:8000/prompts").json()

st.write(f"Categorization Prompt: {prompts["categorization"]}")
st.write(f"Action Prompt: {prompts["action_item"]}")
st.write(f"Auto Reply Prompt: {prompts["auto_reply"]}")

cat_prompt = st.sidebar.text_area("Categorization Prompt", prompts["categorization"])
action_prompt = st.sidebar.text_area("Action Prompt", prompts["action_item"])
auto_reply_prompt = st.sidebar.text_area("Auto Reply Prompt", prompts["auto_reply"])

if st.sidebar.button("Save"):
    data = {
        "categorization": cat_prompt,
        "action_item": action_prompt,
        "auto_reply": auto_reply_prompt
    }

    requests.post("http://127.0.0.1:8000/prompts", json=data)
    st.write("Saved successfully, Refresh to see new Prompts")
    st.rerun()


