from flask import Flask
from flask import request
import json
import http.client

app = Flask(__name__)

@app.route("/searchDrug")
def get_ingredient():
    nombre = request.args.get('active_ingredient')
    act_ing = nombre
    act_ing = act_ing.replace(" ", "%20")
    datos = ""
    temp = '/drug/label.json?search=active_ingredient:"' + act_ing + '"&limit=100'
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request('GET', temp, None, headers)
    r1 = conn.getresponse()
    r2 = r1.read().decode("utf-8")
    conn.close()
    data = json.loads(r2)

    if "results" in data:
        for elem in data["results"]:
            if "brand_name" in elem["openfda"]:
                datos += (str(elem["openfda"]["brand_name"]).lower()[2:-2])
                datos += "<br>"
            else:
                datos += "No hay resultados"
                datos += "<br>"

    else:
        datos = "nada"
    return "<ul>{}</ul>".format(datos)

@app.route("/searchCompany")
def get_company():
    empresa = request.args.get('company')
    emp = empresa
    emp = emp.replace(" ", "%20")
    datos = ""
    temp = '/drug/label.json?search=manufacturer_name:"' + emp + '"&limit=100'
    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request('GET', temp, None, headers)
    r1 = conn.getresponse()
    r2 = r1.read().decode("utf-8")
    conn.close()
    data = json.loads(r2)

    if "results" in data:
        for elem in data["results"]:
            if "brand_name" in elem["openfda"]:
                datos += (str(elem["openfda"]["brand_name"]).lower()[2:-2])
                datos += "<br>"
            else:
                datos += "No hay resultados"
                datos += "<br>"

    else:
        datos = "nada"

    return "<ul>{}</ul>".format(datos)

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
            if "brand_name" in elem["openfda"]:
                datos += (str(elem["openfda"]["brand_name"]).lower()[2:-2])
                datos += "<br>"
            else:
                datos += "No hay resultados"
                datos += "<br>"

    else:
        datos = "nada"

    return "<ul>{}</ul>".format(datos)

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
                datos += "<br>"
            else:
                datos += "Desconocida"
                datos += "<br>"

    else:
        datos = "nada"

        return "<ul>{}</ul>".format(datos)

@app.route("/")
def do_get():
    message = """<!DOCTYPE html>
                <html>
                <body>

                <h2>OPEN FDA</h2>

                <form action="/action_page.php">
                  Punto de entrada:<br>
                  <input type="text" name="nombre" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>If you click the "Submit" button, the form-data will be sent to a page called "/action_page.php".</p>

                </body>
                </html>"""

    return message

if __name__ == "__main__":
    app.run()