"""
Redirect requests to different urls over at firebase,
as determined by the event name.
See API reference at
    https://github.com/mitmproxy/mitmproxy/blob/master/libmproxy/protocol/http.py
"""
import json
import os
from netlib.odict import ODict

FIREBASE_APP = os.environ.get('FIREBASE_APP', 'YOUR APP HERE')
FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY', 'YOUR SECRET HERE')

# Change the map below to your unique event names
# and the firebase URL that each should PUT to.
# In this example, I am using my OneWire device ID as
# part of my event name to know what each value means.
EVENT_URL_MAP = {
    'sensor.28f8e6aa300dd': 'location/basement/underporch/temperature.json'
}


def request(context, flow):
    """
    Called when a client request has been received.
    """
    flow.request.host = "{}.firebaseio.com".format(FIREBASE_APP)
    flow.request.update_host_header()

    if flow.request.method == 'PUT':
        # Get the event name from the request.
        # We will use this to determine the firebase REST endpoint.
        data = json.loads(flow.request.content)
        event = data.pop('event', 'foo')

        # Look up the URL to use from the map, we will PUT the data there.
        url = EVENT_URL_MAP.get(event, 'unmapped.json')
        flow.request.url = 'https://{}.firebaseio.com/{}'.format(FIREBASE_APP, url)

        # Add in your API key for authentication with FireBase
        query = ODict()
        query['auth']=[FIREBASE_API_KEY]
        flow.request.set_query(query)
