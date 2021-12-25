from bs4 import BeautifulSoup
import requests
import asyncio
import time
import fileinput
from telethon import TelegramClient, sync, events

#хуй

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
listok = {'AA', 'AAPL', 'AAPL', 'ABBV', 'AET', 'AET', 'AGN', 'AGN',
          'AHC', 'AHC', 'AMAT', 'AMAT', 'AMCC', 'AMCC', 'AMGN', 'AMGN',
          'AMZN', 'AMZN', 'APA', 'APA', 'APC', 'APC', 'ARBA', 'ARBA',
          'ATML', 'ATML', 'AVP', 'BA', 'BA', 'BABA', 'BAC', 'BAC', 'BDK',
          'BDK', 'BEAS', 'BEAS', 'BMET', 'BMET', 'BR', 'BR', 'BRCD', 'BRCD',
          'BRCM', 'BRCM', 'BTU', 'BTU', 'C', 'C', 'CAT', 'CB', 'CB', 'CBS',
          'CDWC', 'CDWC', 'CHK', 'CHKP', 'CHKP', 'CI', 'CI', 'CIEN', 'CIEN',
          'CME', 'CMI', 'CMI', 'CNXT', 'CNXT', 'COF', 'COF', 'COST', 'COST',
          'CSCO', 'CSCO', 'CTAS', 'CTAS', 'CTX', 'CTX', 'CVX', 'CYTC', 'CYTC',
          'D', 'D', 'DAL', 'DD', 'DELL', 'DELL', 'DIS', 'DISH', 'DISH', 'DNA',
          'DNA', 'DO', 'DO', 'DOW', 'EBAY', 'EBAY', 'EMR', 'EMR', 'EOG', 'EOG',
          'ERICY', 'ERICY', 'ERTS', 'ERTS', 'ESRX', 'ESRX', 'ETFC', 'EXC', 'F',
          'FB', 'FDX', 'FDX', 'FLEX', 'FLEX', 'FSLR', 'GE', 'GENZ', 'GENZ', 'GILD',
          'GILD', 'GMST', 'GMST', 'GOOG', 'GS', 'GS', 'HANS', 'HANS', 'HIG', 'HIG',
          'IBM', 'IBM', 'ICOS', 'ICOS', 'IDTI', 'IDTI', 'IMCL', 'IMCL', 'IMNX',
          'IMNX', 'INTC', 'INTC', 'ITT', 'ITT', 'ITWO', 'ITWO', 'IVGN', 'IVGN',
          'JDSU', 'JDSU', 'JNJ', 'JNPR', 'JNPR', 'JPM', 'JPM', 'KBH', 'KBH', 'KLAC',
          'KLAC', 'KO', 'LEH', 'LEH', 'LLL', 'LLL', 'LLTC', 'LLTC', 'MCD', 'MET',
          'MFNX', 'MFNX', 'MLM', 'MLM', 'MMM', 'MMM', 'MO', 'MO', 'MOLX', 'MOLX',
          'MON', 'MON', 'MS', 'MSFT', 'MSFT', 'MU', 'MXIM', 'MXIM', 'NBR', 'NBR',
          'NE', 'NE', 'NEM', 'NFLX', 'NKE', 'NKE', 'NRG', 'NTAP', 'NTAP', 'NVDA',
          'NVDA', 'NVLS', 'NVLS', 'NXTL', 'NXTL', 'ORCL', 'ORCL', 'OXY', 'OXY',
          'PCAR', 'PCAR', 'PD', 'PD', 'PDLI', 'PDLI', 'PFE', 'PFE', 'PG', 'PM',
          'PMCS', 'PMCS', 'PRU', 'PRU', 'PSFT', 'PSFT', 'QCOM', 'QCOM', 'QLGC',
          'QLGC', 'RAI', 'RAI', 'RATL', 'RATL', 'RFMD', 'RFMD', 'RIMM', 'RIMM',
          'RYL', 'RYL', 'SANM', 'SANM', 'SBUX', 'SEBL', 'SEBL', 'SHLD', 'SHLD',
          'SLB', 'SLB', 'SPY', 'SPY', 'STI', 'STI', 'SUN', 'SUN', 'SUNW', 'SUNW',
          'T', 'TIF', 'TLAB', 'TLAB', 'TMPW', 'TMPW', 'TROW', 'TROW', 'TSLA', 'TWTR',
          'TXN', 'TXN', 'UNP', 'UNP', 'UPS', 'UPS', 'V', 'VLO', 'VRSN', 'VRSN',
          'VRTS', 'VRTS', 'VTSS', 'VTSS', 'VZ', 'WCOM', 'WCOM', 'WLP', 'WLP',
          'WMT', 'XLNX', 'XLNX', 'XOM ', 'YHOO ', 'YNDX', 'VIPS', 'MOMO', 'VALE',
          'ILMN', 'EW', 'IDXX', 'NOK', 'SO', 'ENDP', 'SWN', 'CLOV', 'FTI', 'VEON',
          'ZYNE', 'RIG', 'LI', 'SAVA', 'TAL', 'ALLK', 'CCL', 'TCSG', 'AWH', 'SLDB',
          'BNGO', 'MFGP', 'LPL', 'ACH', 'SWI', 'UA', 'F', 'XRX', 'DBX', 'T', 'M',
          'PAAS', 'GOLD'}
answer = []
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
    ans1 = str(ans1)
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.438'
        }
        response = requests.get(URL_d, headers = HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        #прайс это скока стоит одна акция
        price = ''
        for tag in soup.find_all('span', class_ = 'IsqQVc NprOob wT3VGc'):
            price += tag.text
        if price != '':
            answer.append(ans1 + ' ' + price + ' $' + ans2)
        else:
            answer.append(ans1 + ' ' + '*' + ' $' + ans2)
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
        for i in sorted(answer):
            s += i + '\n'
        out = open('answer.txt', 'w')
        out.writelines(s)
        out.close()
                
    
@client.on(events.NewMessage(chats=(OUTPUT_CHANNEL1)))
async def normal_handler(event):
    #реакция на ответ бота
    await inf(event.id)


client.start()
client.run_until_disconnected()
