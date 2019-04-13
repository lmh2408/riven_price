import os
import requests
from flask import Flask, flash, jsonify, render_template, request


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """ Take API data into search suggestion list """
    try:
        response = requests.get(f"http://n9e5v4d8.ssl.hwcdn.net/repos/weeklyRivensPC.json")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # get data then add name to list
    riven_data = response.json()
    query_list = set()
    for each in riven_data:
        item = str(each["compatibility"]).casefold()
        item = item.title()
        query_list.add(item)

    return render_template("index.html", query_list = query_list)


@app.route("/price", methods=["GET"])
def lookup():
    # get input
    query = request.args.get("query")

    try:
        response = requests.get(f"http://n9e5v4d8.ssl.hwcdn.net/repos/weeklyRivensPC.json")
        response.raise_for_status()
    except requests.RequestException:
        return jsonify(False)

    riven_data = response.json()

    counter = 0
    result = list()

    for item in riven_data:
        if str(item["compatibility"]).lower() == str(query).lower():
            counter = counter + 1
            result.append(item)
            if counter == 2:
                return jsonify(result)

    return jsonify(False)