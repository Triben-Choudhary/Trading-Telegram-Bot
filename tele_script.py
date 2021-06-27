import json
from threading import Timer
from telegram.ext import Updater
from telegram.ext import CommandHandler, Job, run_async
from telegram import ChatAction
from telegram import ParseMode
import os
import time
# import final
def startalert(percent,cid,update,context):
    alert_check = {"aave": 0, "algo": 0, "fet": 0, "comp": 0, "bnb": 0, "link": 0, "aion": 0, "avax": 0, "ankr": 0, "atom": 0, "ada": 0, "bnt": 0, "band": 0, "btc": 0, "bal": 0, "cake": 0, "cvc": 0, "crv": 0, "ckb": 0, "doge": 0, "dock": 0, "dgb": 0, "dot": 0, "egld": 0, "enj": 0, "eos": 0, "etc": 0, "eth": 0, "ftm": 0, "fil": 0, "ftt": 0, "gto": 0, "grt": 0, "hbar": 0, "iotx": 0, "iost": 0, "inj": 0, "kava": 0, "ksm": 0, "luna": 0, "mana": 0, "ren": 0, "sushi": 0, "sc": 0, "snx": 0, "uma": 0, "uni": 0, "vet": 0, "waves": 0, "win": 0, "wrx": 0, "xem": 0, "xtz": 0, "yfi": 0, "zec": 0, "zil": 0, "cos": 0, "zrx": 0, "ava": 0}
    
    def triger(*args):
        coin = ''
        for c in args:
            coin += c
        alert_check[coin] = 0
        return

    def alerting():
        while True:
            try:
                jk = open('check.json','r')
                ddd = jk.read()
                jk.close()
                the_file = json.loads(ddd)
            except:
                pass
            if the_file[cid] == 0:
                return
            elif os.path.getsize('data.json') > 0:
                try:
                    f = open('data.json', 'r')
                    content = f.read()
                    f.close()
                    result = json.loads(content)
                except:
                    pass
                for sym,value in result.items():
                    if alert_check[sym] == 0:
                        greater , lower = max(value['Binance'],value['Wazirx']) , min(value['Binance'],value['Wazirx'])
                        pd = ((greater - lower)/lower)*100
                        if pd >= percent:
                            context.bot.send_chat_action(chat_id=update.message.chat_id , action=ChatAction.TYPING)
                            alert_msg = f"{sym.upper()} is more than <b>{percent}%</b>"
                            context.bot.send_message(chat_id=update.message.chat_id, text = alert_msg, parse_mode = ParseMode.HTML)
                            alert_check[sym] = 1
                            timer = Timer(600,triger,sym)
                            timer.start()
            time.sleep(5)
    return alerting()

@run_async   
def start(update, context):
    get_chat = str(update.message.chat_id)
    new_dict = {}
    new_dict[get_chat] = 0
    with open('check.json', 'r+') as file:
        id_data = json.load(file)
        id_data.update(new_dict)
        file.seek(0)
        json.dump(id_data,file)
    context.bot.send_chat_action(chat_id=update.message.chat_id , action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome")

@run_async
def crypto(update, context):
    f = open('data.json', 'r')
    content = f.read()
    f.close()
    result = json.loads(content)
    symbol = update.message.text.split()[-1]
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    greater , lower = max(result[symbol]['Binance'],result[symbol]['Wazirx']) , min(result[symbol]['Binance'],result[symbol]['Wazirx'])
    pd = ((greater - lower)/lower)*100
    msg = f"Binance : <b>{result[symbol]['Binance']} USDT</b>\nWazirx : <b>{result[symbol]['Wazirx']} USDT</b>\nDifference Percentage : <b>{round(pd,2)}%</b>"
    context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode = ParseMode.HTML)

@run_async
def prices(update, context):
    f = open('data.json', 'r')
    content = f.read()
    f.close()
    result = json.loads(content)
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    pr=[]
    for sym,value in result.items():
        greater , lower = max(value['Binance'],value['Wazirx']) , min(value['Binance'],value['Wazirx'])
        pd = ((greater - lower)/lower)*100
        pr.append(f"{sym.upper()} :\n\t\tBinance : <b> {value['Binance']} USDT </b>\n\t\tWazirx : <b> {value['Wazirx']} USDT </b>\n\t\tDifference Percentage : <b>{round(pd,2)}%</b>\n")

    first_half = pr[0:30]
    second_half = pr[30:]
    pri = '\n'.join(first_half)
    sec = '\n'.join(second_half)
    context.bot.send_message(chat_id=update.message.chat_id, text=pri, parse_mode = ParseMode.HTML)
    context.bot.send_message(chat_id=update.message.chat_id, text=sec, parse_mode = ParseMode.HTML)

@run_async
def sortprices(update, context):
    f = open('data.json', 'r')
    content = f.read()
    f.close()
    result = json.loads(content)
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    pr=[]
    pdlist = []
    for sym,value in result.items():
        greater , lower = max(value['Binance'],value['Wazirx']) , min(value['Binance'],value['Wazirx'])
        pd = ((greater - lower)/lower)*100
        pdlist.append(pd)
        pr.append(f"{sym.upper()} :\n\t\tBinance : <b> {value['Binance']} USDT </b>\n\t\tWazirx : <b> {value['Wazirx']} USDT </b>\n\t\tDifference Percentage : <b>{round(pd,2)}%</b>\n")
    zipped_list = zip(pdlist,pr)
    sort_zip_list = sorted(zipped_list)
    sort_list = [element for _, element in sort_zip_list]
    first_half = sort_list[0:30]
    second_half = sort_list[30:]
    pri = '\n'.join(first_half)
    sec = '\n'.join(second_half)
    context.bot.send_message(chat_id=update.message.chat_id, text=pri, parse_mode = ParseMode.HTML)
    context.bot.send_message(chat_id=update.message.chat_id, text=sec, parse_mode = ParseMode.HTML)

@run_async
def alert(update, context):
    if len(update.message.text.split()) != 2:
        context.bot.send_message(chat_id=update.message.chat_id, text='Wrong Argument')
    else:
        cid = str(update.message.chat_id)
        print(cid)
        li = open('check.json', 'r')
        che = li.read()
        li.close()
        cd = json.loads(che)
        
        if cd[cid] == 0:
            percent = update.message.text.split()[-1]
            try:
                percent = float(percent)
            except:
                context.bot.send_message(chat_id=update.message.chat_id, text='Enter correct percent')
                return
            new_dict = {}
            new_dict[cid] = 1
            with open('check.json', 'r+') as file:
                id_data = json.load(file)
                id_data.update(new_dict)
                file.seek(0)
                json.dump(id_data,file)
            context.bot.send_message(chat_id=update.message.chat_id, text='Alert Starting')
            return startalert(percent,cid,update,context)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='Already Triggered')
@run_async
def offalert(update, context):
    get_chat = str(update.message.chat_id)
    new_dict = {}
    new_dict[get_chat] = 0
    with open('check.json', 'r+') as file:
        id_data = json.load(file)
        id_data.update(new_dict)
        file.seek(0)
        json.dump(id_data,file)
    context.bot.send_message(chat_id=update.message.chat_id, text='Turning off alert')


updater = Updater(token = '1760981034:AAENTfXmFRBfTQJTCIscsoTWXukLLW5AIhs', use_context=True)
dp = updater.dispatcher
j = updater.job_queue
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("crypto", crypto))
dp.add_handler(CommandHandler("prices", prices))
dp.add_handler(CommandHandler("alert", alert))
dp.add_handler(CommandHandler("offalert", offalert))
dp.add_handler(CommandHandler("sortprices", sortprices))

updater.start_polling()
