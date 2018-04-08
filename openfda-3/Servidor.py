import http.server
import socketserver
import http.client
import json

PORT = 8000
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler): # Se define la clase del manejador

    def do_GET(self): # Se define el comportamiento del servidor al recibir el GET de un cliente
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov") # Se define el nombre del servidor al que queremos conectarnos
        conn.request('GET', '/drug/label.json?&limit=10', None, headers) # Con un GET pide la información de la etiqueta
        # de diez medicamentos (limit=10) en un fichero json
        r1 = conn.getresponse()
        r2 = r1.read().decode("utf-8") # Lee la respuesta y se convierte a una cadena
        conn.close()
        data = json.loads(r2) # La respuesta se convierte en un diccionario para que sea más fácil de trabajar en Python

        cont_inicial = """
              <!doctype html>
              <html>
              <body style='background-color: darkblue'>
              <font color = "white">
                <h1>Nombres de medicamentos:</h1>
                <h2>Se muestra el id del medicamento y su nombre</h2>
            """

        contenido = cont_inicial
        for elem in data["results"]: # Se itera sobre los elementos que tienen como clave "results"
            contenido += "Id: " + elem["id"] + " ---- Nombre: "
            if "brand_name" in elem["openfda"]: # Si el medicamento tiene el nombre del fabricante
                contenido += (str(elem["openfda"]["brand_name"]).lower()[2:-2]) # Se añade el nombre a la variable
                # sin comillas ni corchetes ([2:-2]) y en minúsculas
                contenido += "</br>"
            else:
                contenido += "no hay registros" + "</br>"
        contenido += """
              </body>
              </html>
        """

        if self.path == "/" or self.path == "/medicamentos": # Si el parámetro del GET es "/" o "/medicamentos"
            message = contenido # y el mensaje que se manda es su contenido
        else:
            message = cont_inicial + "Path incorrecto (debe ser / o /medicamentos)" # Si no el mensaje es error
            message += """
              </body>
              </html>
            """

        # Se envía el mensaje completo
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return

# Se establece como manejador la clase definida anteriormente
Handler = testHTTPRequestHandler

# Se configura el socket del servidor, para esperar conexiones de clientes
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)

    # Las peticiones se atienden desde el manejador
    # Cada vez que se reciba un "GET" se llama al metodo do_GET del manejador
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido por el usuario")

print("")
print("Servidor parado")