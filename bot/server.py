# Código para crear una instancia de Flask.

from flask import Flask
from flask_restful import Api, Resource
import psutil
import speedtest

# param __name__ sirve para indicar la ubicación de la aplicación.
app = Flask(__name__)
api = Api(app)

# Clase que obtiene los datos  del servidor de manera "oculta" al usuario.
class ServerInfo(Resource):
        def get(self):
            cpu = psutil.getloadavg()[0] * 100  ## Tupla nombrada con estadisticas del CPU.
            memory = psutil.virtual_memory()[5] / 1024 / 1024 ## Tupla nombrada con estadisticas de la memoria.
            netmbps = speedtest.Speedtest().download() / 1024 / 1024 ##Velocidad de descarga del servidor.
            return {"cpu": cpu, "memory": memory, "net-mbps": netmbps, "status": "SUCCESS"}

api.add_resource(ServerInfo, "/serverinfo")


if __name__ == "__main__":
    app.run(debug=True)

