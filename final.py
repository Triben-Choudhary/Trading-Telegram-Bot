import urllib.request as request
from urllib.request import Request, urlopen
import json
import time 
import tele_script

cryptos = ('aave','algo','fet','comp','bnb','link','aion','avax','ankr','atom','ada','bnt','band','btc','bal','cake','cvc','crv','ckb','doge','dock','dgb','dot','egld','enj','eos','etc','eth','ftm','fil','ftt','gto','grt','hbar','iotx','iost','inj','kava','ksm','luna','mana','ren','sushi','sc','snx','uma','uni','vet','waves','win','wrx','xem','xtz','yfi','zec','zil','cos','zrx','ava')
price_data = {}
final_price_data = {}
while True:

    req = Request('https://api.binance.com/api/v3/ticker/price' , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    binance = json.loads(webpage)

    req = Request('https://api.wazirx.com/api/v2/tickers', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    wazirx = json.loads(webpage)
    for i in cryptos:
        price_data[i] = {}
        sym = i.upper() + 'USDT'
        for j in binance:
            if j['symbol'] == sym:
                price = j['price']
                break
        price_data[i]['Binance'] = float(price)

        sym = i + 'usdt'
        price = wazirx[sym]['last']
        price_data[i]['Wazirx'] = float(price)

    final_price_data = price_data.copy()
    price_data.clear()
    op = json.dumps(final_price_data)
    try:
        f = open('data.json','w')
        f.write(op)
        f.close()
    except:
        pass
    time.sleep(1)