import requests
import streamlit as st



emails = requests.get("http://127.0.0.1:8000/emails/").json()


st.title("email inbox")



print(emails)