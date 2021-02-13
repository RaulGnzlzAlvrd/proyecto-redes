import requests
import logging
from telegram.ext import Updater, CommandHandler
import telegram

token = "" # Reemplazar por el token
api_url = "" # TODO: Poner el endpoint en produccion

# logging previene errores y en caso de haberlos manejarlos de forma sencilla para llevar a cabo el análisis.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def getServerStatus():
    response = requests.get(api_url)
    if response.status_code == 200 and "application/json" in response.headers['content-type']:
        return response.json()
    else:
        return {"status": "FAILURE"}

# Función que realiza una petición a una API invocando el método get(), si es que existe,  regresa su respuesta 
# de lo contrario avisa que hubo una falla.
def formatResponse(data):
    if data["status"] == "FAILURE":
        return "Algo ha salido mal :C"
    else:
        message = "Estado del servidor:\n\n"
        message += "💻 <b>CPU promedio en uso</b>: " + str(round(data["cpu"], 2)) + "%\n"
        message += "🗂  <b>Memoria en uso</b>: " + str(round(data["memory"], 2)) + " MB\n"
        message += "📡 <b>Velocidad de conexión</b>: " + str(round(data["net-mbps"], 2)) + " mbps"
        return message

# Definición del formato de respuesta del servidor. De haber una falla la expresa, en otro caso obtiene
# el promedio del uso de CPU, la memoria usada y la velocidad de la conexión.
def sendServerStatus(update, context):
   message = formatResponse(getServerStatus())
   logging.info("Sending to [" + str(update.effective_chat.id) + "]: " + message)
   context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=telegram.ParseMode.HTML)

# Función que envia los resultados de los métodos pre definidos y los envia al bot de telegram para 
# mostrarlos dentro de la app.
def start(update, context):
   update.message.reply_text('Hola mundo!')

updater = Updater(token=token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('server_status', sendServerStatus))
dispatcher.add_handler(CommandHandler('start',start))

updater.start_polling()

