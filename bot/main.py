import requests
import logging
from telegram.ext import Updater, CommandHandler
import telegram

token = "" # Reemplazar por el token
api_url = "http://localhost:3000/api/server-status" # TODO: Poner el endpoint en produccion

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def getServerStatus():
    response = requests.get(api_url)
    if response.status_code == 200 and "application/json" in response.headers['content-type']:
        return response.json()
    else:
        return {"status": "FAILURE"}

def formatResponse(data):
    if data["status"] == "FAILURE":
        return "Algo ha salido mal :C"
    else:
        message = "Estado del servidor:\n\n"
        message += "💻 <b>cpu</b>: " + str(data["cpu"]) + "\n"
        message += "🗂 <b>memmory</b>: " + str(data["memmory"]) + "\n"
        message += "📡 <b>connection</b>: " + str(data["net-mbps"]) + " mbps"
        return message

def sendServerStatus(update, context):
    message = formatResponse(getServerStatus())
    logging.info("Sending to [" + str(update.effective_chat.id) + "]: " + message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=telegram.ParseMode.HTML)

updater = Updater(token=token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('server_status', sendServerStatus))

updater.start_polling()

