#!/usr/bin/env -S python -u
from email.mime.text import MIMEText
from http.client import INTERNAL_SERVER_ERROR
from fastapi import FastAPI
import pydantic
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
import smtplib
from email.mime.multipart import MIMEMultipart
from fastapi import Depends, FastAPI, HTTPException

from starlette.middleware.sessions import SessionMiddleware


"""
SMTP_SERVER: smtp.sendgrid.net
SMTP_PORT: '587'
SOURCE_EMAIL: sales@aramse.io
DEST_EMAIL: sales@aramse.io,ssakhuja@aramse.io
AUTH_USER: apikey
"""

import os

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware(SessionMiddleware, secret_key = "foo") 

session : smtplib.SMTP = smtplib.SMTP(os.environ.get('SMTP_SERVER', 'localhost'), int(os.environ.get('SMTP_PORT', 25)))

class MailSendParams(pydantic.BaseModel):
    subject: str
    body: str
    receipient: str

@app.get("/ready")
async def ready():
    return {"ready": True}

@app.get("/health")
async def health():
    return {'healthy': True}


@app.post('/mail/send')
def mail_send(params : MailSendParams):
    message = MIMEMultipart()
    sender =  os.environ.get('SOURCE_EMAIL', '')
    message['From'] = sender
    message['To'] = params.receipient
    message['Subject'] = params.subject
    message.attach(MIMEText(params.body, 'plain'))
    try:
        session.sendmail(sender,params.receipient, message.as_string())
    except Exception as err:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {'sent': True}


if __name__ == "__main__":
    session.starttls()
    session.login(os.environ.get('AUTH_USER', ''), os.environ.get('AUTH_PASSWD', ''))
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["MAIL_PORT"]), log_level="info")