from flask import Flask
from flask import request
import json
import http.client

app = Flask(__name__)

@app.route("/searchDrug")
def get_ingredient():
    nombre = request.args.get('active_ingredient').replace(" ", "%20")
    #act_ing = nombre
    #act_ing = act_ing.replace(" ", "%20")
    datos =  """
              <!doctype html>
              <html>
              <head>
              <title>Título<title>
              </head>
              <body>
              <h1>Nombres de medicamentos:</h1>
              <p>
            """

    temp = '/drug/label.json?search=active_ingredient:"' + nombre + '"&limit=10'
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

    datos += """
            </p>
            </body>
            </html>
            """

    print(datos)
    return "<ul>{}</ul>".format(datos)

@app.route("/searchCompany")
def get_company():
    empresa = request.args.get('company')
    emp = empresa
    emp = emp.replace(" ", "%20")
    datos = ""
    temp = '/drug/label.json?search=manufacturer_name:"' + emp + '"&limit=10'
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
    num = request.args.get('limite')
    print(num)
    datos = ""
    temp = '/drug/label.json?&limit=' + num
    print(temp)
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
    num = request.args.get('limite')
    print(num)
    datos = ""
    temp = '/drug/label.json?&limit=' + num
    print(temp)
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
                datos += (str(elem["openfda"]["manufacturer_name"]).lower()[2:-2])
                datos += "<br>"
            else:
                datos += "No hay resultados"
                datos += "<br>"

    else:
        datos = "nada"

    return "<ul>{}</ul>".format(datos)

@app.route("/")
def do_get():
    message = """<!DOCTYPE html>
                <html>
                <body>

                <h2>DRUG</h2>

                <form action="/searchDrug">
                  Medicamento:<br>
                  <input type="text" name="active_ingredient" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>If you click the "Submit" button, the form-data will be sent to a page called "/searchDrug".</p>

                </body>
                </html>"""
    message +=  """<!DOCTYPE html>
                <html>
                <body>

                <h2>COMPANY</h2>

                <form action="/searchCompany">
                  Empresa:<br>
                  <input type="text" name="company" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>If you click the "Submit" button, the form-data will be sent to a page called "/searchCompany".</p>

                </body>
                </html>"""
    message +=  """<!DOCTYPE html>
                <html>
                <body>

                <h2>LIST DRUGS</h2>

                <form action="/listDrugs">
                  Límite:<br>
                  <input type="text" name="limite" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>If you click the "Submit" button, the form-data will be sent to a page called "/listDrugs".</p>

                </body>
                </html>"""
    message +=  """<!DOCTYPE html>
                <html>
                <body>

                <h2>LIST COMPANIES</h2>

                <form action="/listCompanies">
                  Límite:<br>
                  <input type="text" name="limite" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>If you click the "Submit" button, the form-data will be sent to a page called "/listCompanies".</p>

                </body>
                </html>"""
    return message

if __name__ == "__main__":
    app.run(port=8000)