import requests
import datetime

address = ['3PEEsRmcWspCxhKqobvKY3axW1846AMRwzr',
           '3P54eYZMTtQnJn8XtUr7Ag3FeyJxpXq2hV7',
           '3PMUTKMtJxfG5pWZYwRcabnP16HYqo4fYK7',
           '3PPuzqQC4bHxWitTyndySGcaMzHHNGipQns',
           '3P5TkQBU68n6YMiiA8zEVSVqwhLcqNYVBFW',
           '3PAU7WdQQUFANNggeHJH7DqDQ1sZxT9Veho',
           '3P5TkQBU68n6YMiiA8zEVSVqwhLcqNYVBFW',
           '3PAmh6W79BVqzVPckUFTfH9epTyzvF9FseB']

vires = 'DSbbhLsSTeDg5Lsiufk2Aneh3DjVqJuPr2M9uU1gwy5p'
USDT_ID = '34N9YcEETLWn93qYQ64EsP1x89tSruJU44RrEMSXXEPJ'
USDC_ID = '6XtHjpXbs9RRJP2Sr9GUyVqzACcby9TkThHXnjVC5CDJ'
USDN_ID = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'

def height():
     headers = {
     'accept': 'application/json',
     }

     response = requests.get('http://nodes.wavesnodes.com/blocks/height', headers=headers).json()
     return response['height']

def check(address):
     headers = {
     'accept': 'application/json',
     }
     json_data = {
     'expr': 'getUserHealth("'+address+'")',
     }
     response = requests.post('https://nodes.wavesnodes.com/utils/script/evaluate/3PAZv9tgK1PX7dKR7b4kchq5qdpUS3G5sYT', headers=headers, json=json_data).json()

     value = response['result']['value'].split(sep=',')

     bp = float(value[0].replace("bp:",""))
     bpu = float(value[1].replace("bpu:",""))

     if bp == 0:
          account_health = 100
     else:
          account_health = round((bp - bpu) / bp *100,2)

     return account_health

# 1 dia es igual a 1440

height = height() - 1
lastAddress = ''

directory = []
directoryFull = []

mirar = []

mi_path = "C:/Users/MCGrafika/Desktop/directoryFull.txt"
txt_file = open(mi_path, "r")
directoryFull = txt_file.read().split(",")
txt_file.close()

del directoryFull[-1]

directoryFull = set(directoryFull)

eliminar =    ['3P5PcgULPQbVmGjNhtwVsdnDoHqpfarguVa',
               '3P6RvKQQvqBw96rtvZ5R5habkSSqgNTZQCY',
               '3PM9tqMkozG5CvgkKwoGjDTCFpKjGuTdwDP',
               '3PGeeDnBr6XCKUdSpPrEwtgKS2KL3goRcCn',
               '3PKdBQrFJgZPv1BJrS8RP6nTzJCXbu6X9LQ',
               '3PAU7WdQQUFANNggeHJH7DqDQ1sZxT9Veho',
               '3P2eDCYsbgriXYm7FR9DmgoDY8123sVVFcF',
               '3PM4hYCY4bKTFBJdxZECweRujhGNuBV5aLi'
               ]

for i in eliminar:
     while i in directoryFull:
          directoryFull.remove(i)

for i in directoryFull:
          p = check(i)
          if p<10:
               current_time = str(datetime.datetime.now())
               message = "{} Direccion: {} - Salud: {}".format(current_time,i,str(p))
               print(message)
