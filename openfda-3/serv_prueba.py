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

        data1 = "" #Se crea una variable vacía
        for elem in data["results"]: #Se itera sobre los elementos que tienen como clave "results"
        #Dentro de esos valores hay más diccionarios
            if "brand_name" in elem["openfda"]: #Si el medicamento tiene el nombre del fabricante
                data1 += (str(elem["openfda"]["brand_name"])[2:-2]) #Se añade el nombre a la variable
                # sin comillas ni corchetes ([2:-2]) y además separados por comas
                data1 += ", "

        f = open('medicamentos.html', 'w') #Se abre el fichero "medicamentos.html" para guardar los datos
        datos = """<html>\n\t<head>\n\t\tNombres de medicamentos:\n\t</head>\n\t<body>\n"""
        datos += "\t\t<p>{}</p>\n".format(data1)
        datos += "\t</body>\n</html>"
        f.write(datos)
        f.close()

        if self.path == "/" or self.path == "/medicamentos": #Si el parámetro del GET es "/" o "/medicamentos"
            with open("medicamentos.html", "r") as f: #Se abre ese fichero
                message = f.read() #y el mensaje que se manda es su contenido
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