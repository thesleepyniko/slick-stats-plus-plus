import os
import logging

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, field_validator
import requests

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners

logging.basicConfig(level=logging.DEBUG)

fastApiApp = FastAPI()

class exchangeTokenRequest(BaseModel):
    code: str

# Initialization
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Register Listeners
register_listeners(app)

@fastApiApp.post("/exchange")
def exchange_token(exchangeReq: exchangeTokenRequest):
    code = exchangeReq.code
    req = requests.post(
        "https://slack.com/api/oauth.v2.access",
        data={
            "code": code,
            "client_id": ...,
            "client_secret": ...
        }
    )

    if req.status_code != 200:
        raise HTTPException(status_code=500, detail="Slack did not return 200 on request")
    
    return req.json() # return it directly

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
