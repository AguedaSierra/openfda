from flask import Flask, redirect
from flask import request
from flask_api import status
import json
import http.client

app = Flask(__name__)

conn = http.client.HTTPSConnection("api.fda.gov")

class OpenFDAClient(): # Clase que incluye la lógica para comunicarse con la API de OpenFDA
    def __init__(self, enlace=""):
        self.enlace = enlace
    def fda_connection(self, enlace):
        headers = {'User-Agent': 'http-client'}
        conn.request('GET', enlace, None, headers)
        r1 = conn.getresponse()
        return r1

class OpenFDAParser(): #Clase que incluye la lógica para obtener los datos de los medicamentos
    def __init__(self, r1=""):
        self.r1 = r1
    def get_data(self):
        r2 = self.r1.read().decode("utf-8")
        conn.close()
        data = json.loads(r2)
        return data

class OpenFDAHTML(): # Clase que genera el HTML para la visualización de la información
    def __init__(self, datos=""" """): # Se inicializan los datos
        self.datos = datos
    def convert_into_html(self, clave, subclave):
        if clave == "warnings":
            encabezado = "Warnings de los medicamentos:"
        else:
            if subclave == "brand_name":
                encabezado = "Nombres de los medicamentos:"
            else:
                encabezado = "Nombres de las empresas:"

        info = """
                <!DOCTYPE html>
                    <html>
                        <body>
                        <h1>""" + encabezado + """</h1>
                        <ul>
                        """

        if "results" in self.datos:
            for elem in self.datos["results"]:
                if subclave != "":
                    if subclave in elem[clave]:
                        info += "<li>"
                        info += (str(elem[clave][subclave]).lower()[2:-2])
                        info += "</li>"
                    else:
                        info += "<li>"
                        info += "No hay resultados"
                        info += "</li>"
                else:
                    if clave in elem:
                        info += "<li>"
                        info += (str(elem[clave]).lower()[2:-2])
                        info += "</li>"
                    else:
                        info += "<li>"
                        info += "No hay resultados"
                        info += "</li>"

        else:
            info += "<li>Error</li>"

        info += """
                        </ul>
                        </body>
                    </html>
                    """
        return info

@app.route("/searchDrug")
def get_ingredient():
   nombre = request.args.get('active_ingredient')
   act_ing = nombre
   act_ing = act_ing.replace(" ", "%20")

   direccion = OpenFDAClient()
   respuesta = direccion.fda_connection('/drug/label.json?search=active_ingredient:"' + act_ing + '"&limit=10')

   data1 = OpenFDAParser(respuesta)
   data = data1.get_data()

   datos_html = OpenFDAHTML(data)
   datos = datos_html.convert_into_html("openfda", "brand_name")

   return datos

@app.route("/searchCompany")
def get_company():
    empresa = request.args.get('company')
    emp = empresa
    emp = emp.replace(" ", "%20")

    direccion = OpenFDAClient()
    respuesta = direccion.fda_connection('/drug/label.json?search=manufacturer_name:"' + emp + '"&limit=10')

    data1 = OpenFDAParser(respuesta)
    data = data1.get_data()

    datos_html = OpenFDAHTML(data)
    datos = datos_html.convert_into_html("openfda", "brand_name")

    return datos

@app.route("/listDrugs")
def get_drugs():
    num = request.args.get('limit')

    direccion = OpenFDAClient()
    respuesta = direccion.fda_connection('/drug/label.json?&limit=' + num)

    data1 = OpenFDAParser(respuesta)
    data = data1.get_data()

    datos_html = OpenFDAHTML(data)
    datos = datos_html.convert_into_html("openfda", "brand_name")

    return datos

@app.route("/listCompanies")
def get_listcomp():
    num = request.args.get('limit')

    direccion = OpenFDAClient()
    respuesta = direccion.fda_connection('/drug/label.json?&limit=' + num)

    data1 = OpenFDAParser(respuesta)
    data = data1.get_data()

    datos_html = OpenFDAHTML(data)
    datos = datos_html.convert_into_html("openfda", "manufacturer_name")

    return datos

@app.route("/listWarnings")
def get_warnings():
    num = request.args.get('limit')

    direccion = OpenFDAClient()
    respuesta = direccion.fda_connection('/drug/label.json?&limit=' + num)

    data1 = OpenFDAParser(respuesta)
    data = data1.get_data()

    datos_html = OpenFDAHTML(data)
    datos = datos_html.convert_into_html("warnings", "")

    return datos

@app.route("/")
def do_get():
    message = """<!DOCTYPE html>
                <html>
                <body>

                <h2>DRUG</h2>

                <form action="searchDrug">
                  Medicamento:<br>
                  <input type="text" name="active_ingredient" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>Si clica en el botón "Submit", irá a la página "/searchDrug".</p>

                </body>
                </html>"""
    message +=  """<!DOCTYPE html>
                <html>
                <body>

                <h2>COMPANY</h2>

                <form action="searchCompany">
                  Empresa:<br>
                  <input type="text" name="company" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>Si clica en el botón "Submit", irá a la página "/searchCompany".</p>

                </body>
                </html>"""
    message +=  """<!DOCTYPE html>
                <html>
                <body>

                <h2>LIST DRUGS</h2>

                <form action="listDrugs">
                  Límite:<br>
                  <input type="text" name="limit" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>Si clica en el botón "Submit", irá a la página "/listDrugs".</p>

                </body>
                </html>"""
    message +=  """<!DOCTYPE html>
                <html>
                <body>

                <h2>LIST COMPANIES</h2>

                <form action="listCompanies">
                  Límite:<br>
                  <input type="text" name="limit" value="">
                  <br>
                  <input type="submit" value="Submit">
                </form> 

                <p>Si clica en el botón "Submit", irá a la página "/listCompanies".</p>

                </body>
                </html>"""

    message += """<!DOCTYPE html>
                      <html>
                      <body>

                      <h2>LIST WARNINGS</h2>

                      <form action="listWarnings">
                        Límite:<br>
                        <input type="text" name="limit" value="">
                        <br>
                        <input type="submit" value="Submit">
                      </form> 

                      <p>Si clica en el botón "Submit", irá a la página "/listWarnings".</p>

                      </body>
                      </html>"""
    return message

@app.route('/secret')
def no_autorizado():
    content = 'WWW-Authenticate'
    return content, status.HTTP_401_UNAUTHORIZED #, {'WWWAuthenticate':'Basic realm="Login Required"'}

@app.route('/redirect')
def root():
    return redirect('http://localhost:8000/', code=302)


if __name__ == "__main__":
    app.run(port=8000)