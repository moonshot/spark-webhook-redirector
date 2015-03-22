# spark-webhook-redirector
Use a single spark.io webhook and redirect traffic based on the PUT data.

* Set up your spark-powered device to publish events.
Here is an example of a sensor that publishes a temperature on a specified interval:
https://github.com/moonshot/spark-tiny-house-sensor.git.
* Create a (free) app on firebase.io to store your data.
* Change the logic in the redirect-to-firebase script to parse your event name and forward the
data to the correct URL for whatever API schema you have architected.

To test out locally:

Set up a python virtualenv and pip install into it, or install the python requirements globally with:
```
sudo pip install -r requirements.txt
```
Start up the server with something like below.
Note: the www.google.com value is a placeholder and your actual firebase URL will be used instead
when the forward proxy script kicks in.
```
mitmdump -s redirect-to-firebase.py -p 8888 -R http://www.google.com
```

Make a request. Substitue "sensor.28f8e6aa300dd" below with your event name that will trigger the logic
that you had coded by modifying the redirect script:
```
curl -X PUT -d '{ "value": "42.12", "event": "sensor.28f8e6aa300dd" }' http://localhost:8888
```

To deploy on heroku:

* On heroku, follow the instructions for deploying a python app on the cedar stack (free).
* In the heroku app dashboard, under Settings, add Config var values for FIREBASE_API_KEY and FIREBASE_APP.
* You can now test out the forward proxy with the above curl statement, using the URL of your heroku app instead
of localhost. Either http or https will work, heroku handles the routing for you.
* Now register a webhook with the spark cli. For example:
```
spark webhook create webhook.json
```
where the contents of webhook.json are something like this:
```
{
    "eventName": "sensor.",
    "url": "https://my-app-name-at-heroku.herokuapp.com/",
    "requestType": "PUT",
    "mydevices": true
}
```
