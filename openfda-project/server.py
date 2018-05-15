# Se importan de flask las funcionalidades de redirect, request (para conseguir parámetros en la URL)
from flask import Flask, redirect
from flask import request
# De flask_api se importan las funcionalidades de los códigos de status de HTTP
from flask_api import status
# Se importa json para tratar el formato de datos adecuadamente
import json
# Se importa http.client para acceder a las funcionalidades de cliente
import http.client

app = Flask(__name__)

conn = http.client.HTTPSConnection("api.fda.gov") # Se define el nombre de dominio de la conexión

class OpenFDAClient(): # Clase que incluye la lógica para comunicarse con la API de OpenFDA
    def __init__(self, enlace=""): # Se incializa el enlace
        self.enlace = enlace
    # fda_connection realiza una petición al servidor de OpenFDA de acuerdo al argumento "enlace"
    def fda_connection(self, enlace):
        headers = {'User-Agent': 'http-client'}
        conn.request('GET', enlace, None, headers)
        r1 = conn.getresponse()
        return r1

class OpenFDAParser(): # Clase que incluye la lógica para obtener los datos de los medicamentos
    def __init__(self, r1=""): # Se inicaliza r1
        self.r1 = r1
    # get_data lee los datos recibidos (en formato json) y los transforma a diccionario python
    def get_data(self):
        r2 = self.r1.read().decode("utf-8")
        conn.close()
        data = json.loads(r2)
        return data

class OpenFDAHTML(): # Clase que genera el HTML para la visualización de la información
    def __init__(self, datos=""" """): # Se inicializan los datos
        self.datos = datos
    # convert_into_html transforma los datos obtenidos en texto HTML con encabezados distintos
    # según los argumentos que se le pase.
    # Posteriormente, en el programa principal, clave tomará los valores "openfda" o "warnings", mientras que
    # subclave podrá tomar los valores "brand_name", "manufacturer_name" o "" (para el caso de warnings)
    def convert_into_html(self, clave, subclave):
        if clave == "warnings":
            encabezado = "Warnings de los medicamentos:"
        else:
            if subclave == "brand_name":
                encabezado = "Nombres de los medicamentos:"
            else:
                encabezado = "Nombres de las empresas:"

        # Los tags <ul> y <li> presentan cada uno de los datos con bullets
        info = """
                <!DOCTYPE html>
                    <html>
                        <body>
                        <h1>""" + encabezado + """</h1>
                        <ul>
                        """

        # Si en los datos recibidos se encuentra la clave "results", se cogen los datos de un campo o de otro
        # en función de la clave y la subclave
        if "results" in self.datos:
            for elem in self.datos["results"]:
                if subclave != "": # clave = "openfda" y subclave es "brand_name" o "manufacturer_name"
                    if subclave in elem[clave]: #
                        info += "<li>"
                        info += (str(elem[clave][subclave]).lower()[2:-2]) # Se eliminan los corchetes
                        info += "</li>"
                    else:
                        info += "<li>"
                        info += "No hay resultados"
                        info += "</li>"
                else:
                    if clave in elem: # clave = "warnings" y subclave = ""
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

# Con la ruta /searchDrug?active_ingredient=<name> se obtienen los nombres de los medicamentos que tienen
# como principio activo <name>
@app.route("/searchDrug")
def get_ingredient():
   # Se obtiene de la URL el parámetro "active_ingredient"
   nombre = request.args.get('active_ingredient')
   num = request.args.get('limit')
   if num == None: # Si no se pone el parámetro "limit" se toma como 10
       num = "10"

   act_ing = nombre
   # En caso de que en el nombre haya un espacio se sustituye por "%20" para evitar errores
   act_ing = act_ing.replace(" ", "%20")

   # Se establece la conexión con OpenFDA usando la clase OpenFDAClient definida anteriormente
   direccion = OpenFDAClient()
   respuesta = direccion.fda_connection('/drug/label.json?search=active_ingredient:"' + act_ing + '"&limit=' + num)

   # Se obtienen los datos de OpenFDA usando la clase OpenFDAParser definida anteriormente
   data1 = OpenFDAParser(respuesta)
   data = data1.get_data()

   # Se convierten los datos obtenidos a HTML usando OpenFDAHTML definida anteriormente
   datos_html = OpenFDAHTML(data)
   datos = datos_html.convert_into_html("openfda", "brand_name")

   return datos

# Con la ruta /searchCompany?company=<company_name> se obtienen los nombres de los medicamentos que
# están fabricados por la empresa <company_name>
@app.route("/searchCompany")
def get_company():
    empresa = request.args.get('company')
    num = request.args.get('limit')
    if num == None:
        num = "10"
    emp = empresa
    emp = emp.replace(" ", "%20")

    direccion = OpenFDAClient()
    respuesta = direccion.fda_connection('/drug/label.json?search=manufacturer_name:"' + emp + '"&limit=' + num)

    data1 = OpenFDAParser(respuesta)
    data = data1.get_data()

    datos_html = OpenFDAHTML(data)
    datos = datos_html.convert_into_html("openfda", "brand_name")

    return datos

# Con la ruta /listDrugs?limit=<limit> se obtiene una lista con los nombres de <limit> medicamentos
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

# Con la ruta /listCompanies?limit=<limit> se obtiene una lista con los nombres de <limit> empresas
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

# Con la ruta /listWarnings?limit=<limit> se obtiene una lista con los warnings de <limit> medicamentos
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

# Con la ruta raíz se presenta un formulario a través del cual se puede acceder a cada una de las rutas anteriores
# introduciendo el parámetro correspondiente
@app.route("/")
def do_get():
    # Formulario "Drug"
    message = """<!DOCTYPE html>
                <html>
                <body>
                <h2>DRUG</h2>
                <form action="searchDrug">
                  Ingrediente activo:<br>
                  <input type="text" name="active_ingredient" value="">
                  <br>
                  <input type="submit" value="Enviar">
                </form> 
                <p>Si clica en el botón "Enviar", irá a la página "/searchDrug".</p>
                </body>
                </html>"""

    # Formulario "Company"
    message +=  """<!DOCTYPE html>
                <html>
                <body>
                <h2>COMPANY</h2>
                <form action="searchCompany">
                  Empresa:<br>
                  <input type="text" name="company" value="">
                  <br>
                  <input type="submit" value="Enviar">
                </form> 
                <p>Si clica en el botón "Enviar", irá a la página "/searchCompany".</p>
                </body>
                </html>"""

    # Formulario "ListDrugs"
    message +=  """<!DOCTYPE html>
                <html>
                <body>
                <h2>LIST DRUGS</h2>
                <form action="listDrugs">
                  Límite:<br>
                  <input type="text" name="limit" value="">
                  <br>
                  <input type="submit" value="Enviar">
                </form> 
                <p>Si clica en el botón "Enviar", irá a la página "/listDrugs".</p>
                </body>
                </html>"""

    # Formulario "List Companies"
    message +=  """<!DOCTYPE html>
                <html>
                <body>
                <h2>LIST COMPANIES</h2>
                <form action="listCompanies">
                  Límite:<br>
                  <input type="text" name="limit" value="">
                  <br>
                  <input type="submit" value="Enviar">
                </form> 
                <p>Si clica en el botón "Enviar", irá a la página "/listCompanies".</p>
                </body>
                </html>"""

    # Formulario "List Warnings"
    message += """<!DOCTYPE html>
                      <html>
                      <body>
                      <h2>LIST WARNINGS</h2>
                      <form action="listWarnings">
                        Límite:<br>
                        <input type="text" name="limit" value="">
                        <br>
                        <input type="submit" value="Enviar">
                      </form> 
                      <p>Si clica en el botón "Enviar", irá a la página "/listWarnings".</p>
                      </body>
                      </html>"""
    return message

# Con la ruta /secret se accede a una página en la que aparece un cuadro de diálogo para introducir usuario y contraseña
@app.route('/secret')
def no_autorizado():
    content = 'Es necesaria autenticación para acceder a esta página'
    # Se devuelve el código HTTP 401 y se presenta un ventana pidiendo usuario y contraseña
    return content, status.HTTP_401_UNAUTHORIZED, {'WWW-Authenticate':'Basic realm="Login Required"'}

# Con la ruta /redirect se vuelve a la ruta raíz
@app.route('/redirect')
def root():
    # Se devuelve el código HTTP 302 (redirect)
    return redirect('http://localhost:8000/', code=302)

# No es necesario implementar código para el error 404 (Not found) porque flask lo hace automáticamente
# cuando no es una de las rutas definidas mediante un @app.route()

if __name__ == "__main__":
    app.run(port=8000)