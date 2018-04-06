import http.server
import socketserver
import http.client
import json

PORT = 8000
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler): #Se define la clase del manejador

    def do_GET(self): #Se define el comportamiento del servidor al recibir el GET de un cliente
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov") #El programa se conecta con la página de la api fda
        conn.request('GET', '/drug/label.json?&limit=10', None, headers) #Con un GET pide la información de la etiqueta
        #de diez medicamentos (limit=10) en un fichero json
        r1 = conn.getresponse()
        r2 = r1.read().decode("utf-8") #Lee la respuesta y la decodifica en formato utf-8
        conn.close() #Se cierra la conexión
        data = json.loads(r2) #La respuesta en código utf-8 se convierte en un diccionario para que sea más
        #fácil de trabajar en Python

        contenido = """
              <!doctype html>
              <html>
              <body style='background-color: lavender'>
                <h1>Nombres de medicamentos:</h2>
              </body>
              </html>
            """

        for elem in data["results"]: #Se itera sobre los elementos que tienen como clave "results"
        #Dentro de esos valores hay más diccionarios
            contenido += "El nombre del fabricante del medicamento con id: "
            contenido += elem["id"]
            contenido += " es: "
            if "brand_name" in elem["openfda"]: #Si el medicamento tiene el nombre del fabricante
                contenido += (str(elem["openfda"]["brand_name"]).lower()[2:-2]) #Se añade el nombre a la variable
                # sin comillas ni corchetes ([2:-2]) y además separados por comas
                contenido += "</br></body></html>"
            else:
                contenido += "no hay registros"
                contenido += "</br></body></html>"

        if self.path == "/" or self.path == "/medicamentos": #Si el parámetro del GET es "/" o "/medicamentos"
            message = contenido #y el mensaje que se manda es su contenido
        else:
            message = "Error" #Si no el mensaje es error

        #Se envía el mensaje completo
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return

#El servidor comienza a aquí
#Se establece como manejador la clase definida anteriormente
Handler = testHTTPRequestHandler

#Se configura el socket del servidor, para esperar conexiones de clientes
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)

    #Entrar en el bucle principal
    #Las peticiones se atienden desde el manejador
    #Cada vez que se ocurra un "GET" se invoca al metodo do_GET del manejador
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido por el usuario")

print("")
print("Servidor parado")