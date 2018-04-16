import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True  # Para no tener que estar cambiando el puerto

PORT = 8000


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

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

        self.wfile.write(bytes(message, "utf8"))
        print("File served!")


        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")  # Se define el nombre del servidor al que queremos conectarnos
        conn.request('GET', '/drug/label.json?search=active_ingredient:{}'.format("value"), None, headers)
        r1 = conn.getresponse()
        r2 = r1.read().decode("utf-8")  # Lee la respuesta y se convierte a una cadena
        conn.close()
        data = json.loads(r2)  # La respuesta se convierte en un diccionario para que sea más fácil de trabajar en Python

        contenido = ""
        for elem in data["results"]:  # Se itera sobre los elementos que tienen como clave "results"
            contenido += "Id: " + elem["id"] + " ---- Nombre: "
            if "brand_name" in elem["openfda"]:  # Si el medicamento tiene el nombre del fabricante
                contenido += (str(elem["openfda"]["brand_name"]).lower()[2:-2])  # Se añade el nombre a la variable
                # sin comillas ni corchetes ([2:-2]) y en minúsculas
                contenido += "</br>"
            else:
                contenido += "no hay registros" + "</br>"
                contenido += """
                      </body>
                      </html>
                """

        self.wfile.write(bytes(contenido, "utf8"))
        print("File served!")
        return


Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")