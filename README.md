# spark-webhook-redirector
Use a single spark.io webhook and redirect traffic based on the PUT/POST data.

To test out locally:

Start up the server with something like (the www.google.com piece will be overwritten):
```
mitmdump -s redirect-to-firebase.py -p 8888 -R http://www.google.com
```

Make a request:
```
curl -X PUT -d '{ "name": "temperature", "value": "57.10", "url": "foobar.json" }' http://localhost:8888
```
