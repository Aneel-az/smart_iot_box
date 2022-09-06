import os
import smtplib, ssl

import uvicorn
from fastapi import FastAPI
import requests

from consts import (
    SYSTEM_MAIL,
    SYSTEM_MAIL_PASSWORD,
    SYSTEM_MAIL_PORT,
    SYSTEM_MAIL_HOST,
    DEFAULT_PORT,
    OWNER_MAIL
)

app = FastAPI()
port = int(os.environ.get('PORT', DEFAULT_PORT))

context = ssl.create_default_context()
message = """\
Subject: delivery

you're delivery is waiting on the door.

To open the box enter:": "https://aneel-smart-box.herokuapp.com/open
To close the box enter:": "https://aneel-smart-box.herokuapp.com/close
"""


@app.get("/scan")
async def root():
    with smtplib.SMTP_SSL(SYSTEM_MAIL_HOST, SYSTEM_MAIL_PORT, context=context) as server:
        server.login(SYSTEM_MAIL, SYSTEM_MAIL_PASSWORD)
        server.sendmail(SYSTEM_MAIL, OWNER_MAIL, message)
    return "A notification was sent to the house's owner."


@app.get("/open")
async def root():
    try:
        result = requests.get("MYHOST:80/open")
        return result.text
    except:
        return "Open mock box"


@app.get("/close")
async def root():
    try:
        result = requests.get("MYHOST:80/close")
        return result.text
    except:
        return "Close mock box"


uvicorn.run(app, host="0.0.0.0", port=port)
