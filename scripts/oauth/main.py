import http.server
import urllib.parse
import webbrowser

SCOPES="users.profile:write,users.profile:read"    
CLIENT_ID=""
OAUTH_URL=f"https://slack.com/oauth/v2_user/authorize?client_id={CLIENT_ID}&scope={SCOPES}"
PORT=6768

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        ...
    
    def exchange_for_access_code(self):
        ...

    def send_error_response(self):
        ...

webbrowser.open_new_tab(OAUTH_URL) # open the tab, awit for auth to complete

