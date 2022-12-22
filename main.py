import os
from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from utils import fetch_reply


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
whatsapp_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)


@app.get("/")
def read_root():
    message = client.messages.create(
        body='Como vai?',
        from_='whatsapp:'+whatsapp_number,
        to='whatsapp:+553584496453'
    )   
    return {"Hello": "World"}


@app.post("/sms")
async def sms_reply(request: Request):    
    data = await request.form()
    msg = data.get('Body')
    phone_number = data.get('From')
    reply = fetch_reply(msg, phone_number)

    resp = MessagingResponse()
    resp.message(reply)
    
    return Response(content=str(resp), media_type='application/xml')
