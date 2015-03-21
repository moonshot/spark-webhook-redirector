"""
Redirect requests to different urls over at firebase,
as determined by the url parameter that was passed in the json payload.
See API reference at
    https://github.com/mitmproxy/mitmproxy/blob/master/libmproxy/protocol/http.py
"""
import json
import os
from netlib.odict import ODict

FIREBASE_APP = os.environ.get('FIREBASE_APP', 'YOUR APP HERE')
FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY', 'YOUR SECRET HERE')

def request(context, flow):
    """
    Called when a client request has been received.
    """
    flow.request.host = "{}.firebaseio.com".format(FIREBASE_APP)
    flow.request.update_host_header()

    if flow.request.method == 'PUT':

        # Get the url from the json that was sent in the request
        data = json.loads(flow.request.content)
        url = data.pop('url', 'foo')
        flow.request.content = json.dumps(data)

        # Change the URL to that specified
        flow.request.url = 'https://{}.firebaseio.com/{}'.format(FIREBASE_APP, url)

        # Add in your API key for authentication
        query = ODict()
        query['auth']=[FIREBASE_API_KEY]
        flow.request.set_query(query)
