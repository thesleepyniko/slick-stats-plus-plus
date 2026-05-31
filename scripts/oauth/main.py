# /// script
# requires-python = ">=3.0"
# dependencies = []
# ///

import http.server
from urllib.parse import urlparse, parse_qs, urlencode
import json
import urllib.request
import webbrowser
import secrets
import sys
import requests

# thats right. it's the AI variable formatting.
# it actually looks good tbf...
STATE     = secrets.token_hex(16)
SCOPES    = "users.profile:write,users.profile:read"    
CLIENT_ID = ""
OAUTH_URL = f"https://slack.com/oauth/v2_user/authorize?client_id={CLIENT_ID}&scope={SCOPES}?state={STATE}"
PORT      = 6768 # :sixseven:

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        
        parsed_url    = urlparse(self.path)
        parsed_params = parse_qs(parsed_url.query) # note to self: returns dict in form of: {"param": ["thing"]}
        code          = parsed_params["code"][0]
        state         = parsed_params["state"][0]

        if state != STATE:
            print("ERROR: State returned did not match initial state", file=sys.stderr)
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = "<html><body><h1>400</h1><h2>Slack returned URL with invalid state </h2></body></html>"
            self.wfile.write(html.encode("utf-8"))
            sys.exit(0)
        
        else:
            # send code to server with state, await server to return it
            body_bytes = urlencode({"code": code}).encode('utf-8')

            req = urllib.request.Request(
                url="https://example.com",
                data=body_bytes,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )

            try:
                with urllib.request.urlopen(req) as response:
                    resp_status = response.getcode()
                    resp_body = response.read().decode('utf-8')
            except urllib.request.HTTPError as e:
                resp_status = e.code
                resp_body = e.read().decode('utf-8') if hasattr(e, 'read') else ''

            if resp_status != 200:
                print(f"ERROR: Server returned {resp_status}", file=sys.stderr)
                self.send_response(resp_status)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                html = f"<html><body><h1>{resp_status}</h1><h2>Server returned with {resp_status}</h2></body></html>"
                self.wfile.write(html.encode("utf-8"))
                sys.exit(0)

            # parse JSON response from server
            data: dict = json.loads(resp_body)

        ... # should probably write out a simple page telling the user to return to terminal?
    
    def exchange_for_access_code(self):
        ...

    def send_error_response(self):
        ...

webbrowser.open_new_tab(OAUTH_URL) # open the tab, awit for auth to complete

# goodbye america hello new york