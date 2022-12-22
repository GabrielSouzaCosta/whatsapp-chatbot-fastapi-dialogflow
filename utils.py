import os
from dotenv import load_dotenv
from google.cloud import dialogflow

load_dotenv()

DIALOGFLOW_PROJECT_ID = 'c007-nbxa'
dialogflow_session_client = dialogflow.SessionsClient()

def detect_intent_from_text(text, session_id, language_code='pt-BR'):
    session = dialogflow_session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(query, session_id):
    response = detect_intent_from_text(query, session_id)
    return response.fulfillment_text