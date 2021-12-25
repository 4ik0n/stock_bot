from bs4 import BeautifulSoup
import requests
import asyncio
import time
import fileinput
from telethon import TelegramClient, sync, events

INPUT_CHANNEL1 = 'https://t.me/joinchat/AAAAAFLDCjpm9veBn68xUQ'
OUTPUT_CHANNEL1 = '@stocks_analyst_bot'

api_id = 15837383
api_hash = '4face98e940e7f2b6a1d45324cbe61f0'

TAGS = ['#TAG1', '#TAG2']

client = TelegramClient('Ses', api_id, api_hash)

print("Client Created")

lines = open('text.txt', 'r').readlines()
lines[0] = '1'
out = open('text.txt', 'w')
out.writelines(lines)
out.close()

#тикеры компаний
listok = {'AWH', 'ILMN', 'EOG', 'DISH', 'AMGN', 'PM', 'DBX', 'DELL', 'MU', 'CHK', 'BA', 'GOOG', 'MSFT', 'AA', 'UA', 'BAC',
          'SO', 'GE', 'TXN', 'PD', 'MS', 'CCL', 'ORCL', 'MO', 'NKE', 'VEON', 'SLB', 'ENDP', 'CIEN', 'DAL', 'PG', 'PFE', 'NOK',
          'C', 'KO', 'KBH', 'NEM', 'D', 'EW', 'ZYNE', 'TAL', 'VALE', 'IDXX', 'ALLK', 'DD', 'HIG', 'INTC', 'UNP', 'KLAC', 'SWI',
          'AMAT', 'CB', 'MCD', 'AMZN', 'CSCO', 'SWN', 'EXC', 'VLO', 'GILD', 'XRX', 'MFGP', 'WMT', 'FDX', 'MLM', 'EMR', 'AVP',
          'ITT', 'JNPR', 'CTAS', 'PCAR', 'CME', 'BABA', 'ABBV', 'F', 'DIS', 'CAT', 'SBUX', 'JNJ', 'COST', 'FTI', 'PAAS', 'CMI',
          'GOLD', 'VIPS', 'DOW', 'OXY', 'VRTS', 'XLNX', 'NFLX', 'MET', 'EBAY', 'NTAP', 'T', 'ACH', 'V', 'YNDX', 'XOM', 'APA',
          'QCOM', 'VRSN', 'LPL', 'UPS', 'M', 'CLOV', 'SAVA', 'FB', 'NVDA', 'VZ', 'JPM', 'SLDB', 'TWTR', 'CI', 'GS', 'BR',
          'LI', 'TSLA', 'RIG', 'COF', 'FSLR', 'AAPL', 'IBM', 'BNGO', 'PRU', 'MOMO', 'CHKP', 'CVX', 'NRG', 'MMM', 'TROW'}
answer = []
def my_sort(sort_list):
    def compare(elem1, elem2):
        if (elem1[0] < elem2[0]):
            return True
        elif (elem1[0] > elem2[0]):
            return False
        else:
            if (elem1[1] > elem2[1]):
                return True
            else:
                return False
    for i in range(len(sort_list)):
        for j in range(len(sort_list) - 1 - i):
            elem_now = sort_list[j]
            if (compare(sort_list[j], sort_list[j + 1])):
                sort_list[j] = sort_list[j + 1]
                sort_list[j + 1] = elem_now
    return sort_list

async def inf(msg_id):
    #text - сообщение от того бота
    text = str(await client.get_messages(OUTPUT_CHANNEL1, ids = msg_id))
    ind = text.find('%')
    tik1 = text.find('$')
    ans1 = 0
    if (ind > 0):
        for i in range (4, 0, -1):
            try:
                ans1 += (int(text[ind - i]) * pow(10, i - 1))
            except:
                continue
    #анс1 - процент
    #анс2 - тикер компании
    ans2 = ''
    if (tik1 > 0):
        i = tik1 + 1
        while text[i] != '(':
            try:
                ans2 += text[i]
                i += 1
            except:
                i += 1
    if (ans2 != ''):
        #если бот нашел компанию
        #тут мы чекаем в гугле по тикеру компании скока стоит одна акция
        URL_d = 'https://www.google.com/search?q=' + ans2 + '+stock'
        HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50', 'accept': '*/*'
        }
        response = requests.get(URL_d, headers = HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup, 'soup')
        #прайс это скока стоит одна акция
        price = ''
        for tag in soup.find_all('span', class_ = 'IsqQVc NprOob wT3VGc'):
            price += tag.text
        if price != '':
            answer.append([ans1, float(price.replace(',', '.')), ans2])
        else:
            answer.append([ans1, 0.0, ans2])
    #дальше я сделал херню, чтобы мой бот проспамил компаниями только один раз
    f = open('text.txt', 'r')
    i = f.read(1)
    lines = open('text.txt', 'r').readlines()
    lines[0] = '2'
    out = open('text.txt', 'w')
    out.writelines(lines)
    out.close()
    #вызывается спам компаниями
    await spis(i)
    
async def spis(num):
    #проверка проспамил ли бот
    if num == '1':
        #спам компаниями
        for i in listok:
            await client.send_message(OUTPUT_CHANNEL1, i)
            await asyncio.sleep(2)
        s = ''
        for i in my_sort(answer):
            s += str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n'
        out = open('answer.txt', 'w')
        out.writelines(s)
        out.close()
                
    
@client.on(events.NewMessage(chats=(OUTPUT_CHANNEL1)))
async def normal_handler(event):
    #реакция на ответ бота
    await inf(event.id)


client.start()
client.run_until_disconnected()
