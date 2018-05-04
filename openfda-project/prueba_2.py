from flask import Flask
from flask import request
import json
import requests

app = Flask(__name__)

@app.route("/searchDrug")
def get_ingredient():
    algo = request.args.get('active_ingredient')
    url = "https://api.fda.gov/drug/label.json?search=active_ingredient:'"
    url += algo
    url += "'&limit=100"
    print(url)
    print(type(url))
    pet = requests.get(url).json()
    print(type(pet))
    return pet

if __name__ == "__main__":
    app.run()
