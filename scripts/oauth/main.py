import http.server
from urllib.parse import urlparse, parse_qs
import webbrowser
import secrets
import sys

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
            sys.exit(0)
        
        else:
            # send code to server with state, await server to return it
            ...

        ... # should probably write out a simple page telling the user to return to terminal?
    
    def exchange_for_access_code(self):
        ...

    def send_error_response(self):
        ...

webbrowser.open_new_tab(OAUTH_URL) # open the tab, awit for auth to complete

# goodbye america hello new york