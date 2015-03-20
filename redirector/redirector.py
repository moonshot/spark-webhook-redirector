"""
Redirect HTTP requests to an external service, namely FireBase
"""

import re
import urlparse
from .http import StubHttpRequestHandler, StubHttpService, require_params

class FirebaseRedirectServiceHandler(StubHttpRequestHandler):

    @require_params('POST', 'fb_path')
    def do_POST(self):
        self.send_response(200)

class FirebaseRedirectService(StubHttpService):
    HANDLER_CLASS = FirebaseRedirectServiceHandler
