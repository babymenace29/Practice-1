import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

# create your API token, and set it up in Postman collection as part of the Body section
API_TOKEN = "123"
# you can get API keys for free here - https://api-ninjas.com/api/jokes
RSA_KEY = "9PXV38WJBEPDY24PTVUD6VJVJ"

app = Flask(__name__)
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def get_weather_api(location, date):
    url =f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key={RSA_KEY} "

    response = requests.get(url)

    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        raise InvalidUsage(response.text, status_code=response.status_code)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>KMA L2: python Saas.</h2></p>"


@app.route("/start", methods=["POST"])
def joke_endpoint():
    datetime = dt.datetime.now()
    json = request.get_json()
    token = json.get("token")
    date = json.get("date")
    location = json.get("location")
    requester_name = json.get("requester_name")

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    # exclude = ""
    # if json_data.get("exclude"):
    #     exclude = json_data.get("exclude")

    data = get_weather_api(location, date)

    result = {
        "datetime": datetime,
        "name": requester_name,
    }

    return result


if __name__ == "__main__":
    app.run(debug=True)