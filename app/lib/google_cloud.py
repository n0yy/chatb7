import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

SECRETS = st.secrets["firebase"]
CREDENTIALS = service_account.Credentials.from_service_account_info(SECRETS)
firestore = firestore.Client(credentials=CREDENTIALS, project=SECRETS["project_id"])


def collection(name: str):
    return firestore.collection(name)
