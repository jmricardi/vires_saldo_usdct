from time import sleep
from tokens import TeleBotToken
import requests
import telebot
import os

# from tokens import TeleBotToken

def monitor():
    resp = requests.get("https://api.vires.finance/state")
        
    if resp.status_code != 200:
        print("Error del servidor Vires")
        return "error"
    else:
        resp = resp.json()
    # condicional saldo USDC

    USDC_supply = resp['markets'][3]['supply']
    USDC_debt = resp['markets'][3]['totalDebt']
    USDC_saldo = USDC_supply - USDC_debt

    # condicional saldo USDT

    USDT_supply = resp['markets'][2]['supply']
    USDT_debt = resp['markets'][2]['totalDebt']
    USDT_saldo = USDT_supply - USDT_debt

    return (USDT_saldo, USDC_saldo)

def formatNumber(number, decimals, espanol=True):
    if type(number) != int and type(number) != float:
        return number
    
    d={'.':',',',':'.'}
    return ''.join(d.get(s, s) for s in f"{number:,.{decimals}f}") \
        if espanol \
        else f"{number:,.{decimals}f}"    

bot = telebot.TeleBot(TeleBotToken, parse_mode=None)

@bot.message_handler(commands=['help'])
def greet(message):
    bot.reply_to(message, "Hola. Este bot tiene 3 comandos utiles:")
    bot.reply_to(message, "/chatid empleado para indentificar el ID del chat")
    bot.reply_to(message, "/saldos para mostrar los saldos de libre disponibilidad de USDC y USDT de Vires")
    bot.reply_to(message, "/monitor para activar el monitor continuo de saldos de USDC y USDT de Vires. Informara continuamente cuando haya cambios en la disponibilidad")

@bot.message_handler(commands=['chatid'])
def chatid(message):
    bot.reply_to(message, "Tu chat ID es: " + str(message.chat.id))

@bot.message_handler(commands=['hola'])
def hola(message):
    bot.reply_to(message, "Hey! Como estas")

@bot.message_handler(commands=['saldos'])
def saldos(message):

    bot.send_message(message.chat.id, "Iniciando...")

    USDT = ""
    USDC = ""
    estado_USDT = "-"
    estado_USDC = "-"
    
    while True:

        response = monitor()

        if response =="error":
            print("Error Server - FIN")
            break

        estado_USDT = USDT
        estado_USDC = USDC

        if response[0] < 0:
            USDT = "sin"
        else:
            USDT = "con"

        if response[1] < 0:
            USDC = "sin"
        else:
            USDC = "con"

        if estado_USDT != USDT or estado_USDC != USDC:
            bot.send_message(message.chat.id,"Saldo USDT -> USD " + str(formatNumber(response[0],2,True)) + " " + USDT + " saldo")
            bot.send_message(message.chat.id,"Saldo USDC -> USD " + str(formatNumber(response[1],2,True)) + " " + USDC + " saldo")

bot.polling(none_stop=True)






