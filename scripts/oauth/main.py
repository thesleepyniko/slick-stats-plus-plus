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
CLIENT_ID = "9991336848048.11245198089317"
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
            html = "<html><body><h1>400</h1><h2>Slack returned URL with invalid state</h2></body></html>"
            self.wfile.write(html.encode("utf-8"))
            sys.exit(0)
        
        else:
            # send code to server with state, await server to return it
            body_bytes = urlencode({"code": code}).encode('utf-8')

            req = urllib.request.Request(
                url="https://slick.greenphosphor.dev", # needs to be URL that bot is hosted on
                data=body_bytes,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )

            try:
                with urllib.request.urlopen(req) as response:
                    resp_status = response.getcode()
                    data = json.loads(response.read().decode('utf-8'))
                    resp_body = None
            except urllib.request.HTTPError as e:
                resp_status = e.code
                resp_body = e.read().decode('utf-8') if hasattr(e, 'read') else 'Nothing returned'
                data = None

            # show a little page, not too pretty to conserve space
            if resp_status != 200:
                print(f"ERROR: Server returned {resp_status}", file=sys.stderr)
                self.send_response(resp_status)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                html = f"<html><body><h1>{resp_status}</h1><h2>Server returned with {resp_status}<br>Body returned: {resp_body}</h2></body></html>"
                self.wfile.write(html.encode("utf-8"))
                sys.exit(1)

            # parse JSON response from server

            if not data:
                print("ERROR: Server did not return any content", file=sys.stderr)
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                html = "<html><body><h1>500</h1><h2>Server did not return any content.</h2></body></html>"
                self.wfile.write(html.encode("utf-8"))
                sys.exit(1)
                
            if not data.get("access_token") or not data.get("ok"):
                print("ERROR: Access token not included or result errored", file=sys.stderr)
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                html = "<html><body><h1>500</h1><h2>Slack either did not include an access token or errored</h2></body></html>"
                self.wfile.write(html.encode("utf-8"))
                sys.exit(1)

            if not data.get("enterprise", {}).get("id") or data.get("enterprise").get("id") != "E09V59WQY1E":
                print("ERROR: User did not auth with Hack Club", file=sys.stderr)
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                html = "<html><body><h1>400</h1><h2>Did not authenticate with Hack Club workspace<br>Please try again.</h2></body></html>"
                self.wfile.write(html.encode("utf-8"))
                sys.exit(1)
            
            
            else:
                access_token = data.get("access_token")
                # write access token into a file
                ...

        print("Successful", file=sys.stderr)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html = "<html><body><h1>400</h1><h2>Did not authenticate with Hack Club workspace<br>Please try again.</h2></body></html>"
        self.wfile.write(html.encode("utf-8"))
        sys.exit(0)

webbrowser.open_new_tab(OAUTH_URL) # open the tab, awit for auth to complete

# goodbye america hello new york