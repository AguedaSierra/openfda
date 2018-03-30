import http.server
import socketserver
import http.client
import json

PORT = 8000
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request('GET', '/drug/label.json?&limit=10', None, headers)
        r1 = conn.getresponse()
        r2 = r1.read().decode("utf-8")
        conn.close()
        data = json.loads(r2)
        data1 = []
        for elem in data["results"]:
            if "brand_name" in elem["openfda"]:
                data1.append(str(elem["openfda"]["brand_name"]))
        mensaje = " ".join(data1)
        print("Datos en servidor {}".format(mensaje))
        f = open('medicamentos.html', 'w')
        message = """<html>\n\t<head>\n\t\tNombres de medicamentos\n\t</head>\n\t<body>\n"""
        message += "\t\t<p>{}</p>\n".format(mensaje)
        message += "\t</body>\n</html>"
        f.write(message)
        f.close()

        # Enviar el mensaje completo
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return


# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# -- Configurar el socket del servidor, para esperar conexiones de clientes
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)

    # Entrar en el bucle principal
    # Las peticiones se atienden desde nuestro manejador
    # Cada vez que se ocurra un "GET" se invoca al metodo do_GET de
    # nuestro manejador
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido por el usuario")

print("")
print("Servidor parado")