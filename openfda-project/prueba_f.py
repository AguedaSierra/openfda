from flask import Flask
from flask import request
import json
import http.client

app = Flask(__name__)

@app.route("/searchDrug")
def get_ingredient():
    algo = request.args.get('active_ingredient')
    datos = ""
    temp = '/drug/label.json?search=active_ingredient:"' + algo + '"&limit=100'
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request('GET', temp, None, headers)
    r1 = conn.getresponse()
    r2 = r1.read().decode("utf-8")
    conn.close()
    data = json.loads(r2)

    if "results" in data:
        for elem in data["results"]:
            datos += elem["id"] + "////"

    else:
        datos = "nada"

    return algo + '------' + datos

@app.route("/searchCompany")
def get_company():
    empresa = request.args.get('company')
    datos = ""
    temp = '/drug/label.json?search=manufacturer_name:"' + empresa + '"&limit=100'
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request('GET', temp, None, headers)
    r1 = conn.getresponse()
    r2 = r1.read().decode("utf-8")
    conn.close()
    data = json.loads(r2)

    if "results" in data:
        for elem in data["results"]:
            datos += elem["id"] + "////"

    else:
        datos = "nada"

    return empresa + '------' + datos

@app.route("/listDrugs")
def get_drugs():
    datos = ""
    temp = '/drug/label.json?&limit=100'
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request('GET', temp, None, headers)
    r1 = conn.getresponse()
    r2 = r1.read().decode("utf-8")
    conn.close()
    data = json.loads(r2)

    if "results" in data:
        for elem in data["results"]:
            datos += elem["id"] + "////"

    else:
        datos = "nada"

    return datos

@app.route("/listCompanies")
def get_listcomp():
    datos = ""
    temp = '/drug/label.json?&limit=100'
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request('GET', temp, None, headers)
    r1 = conn.getresponse()
    r2 = r1.read().decode("utf-8")
    conn.close()
    data = json.loads(r2)

    if "results" in data:
        for elem in data["results"]:
            if "manufacturer_name" in elem["openfda"]:
                datos += (str(elem["openfda"]["manufacturer_name"])[2:-2])
                datos += "/////"
            else:
                datos += "No disponible"
                datos += "/////"

    else:
        datos = "nada"

    return datos


if __name__ == "__main__":
    app.run()