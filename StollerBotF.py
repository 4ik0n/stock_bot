from bs4 import BeautifulSoup
import requests
import asyncio
import time
import fileinput
import unidecode
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
listok = {'TRIP', 'MRC', 'NFLX', 'MU', 'VRTS', 'TD', 'CL', 'APH', 'EW', 'BSX', 'ALLK', 'CLOV', 'CHGG', 'PD', 'LIN', 'PXD', 'HON', 'TTD', 'DXCM', 'RIVN', 'CARR', 'PUK', 'APTV', 'PDD', 'KKR', 'UNP', 'WBA', 'ET', 'CORR', 'CAT', 'WTTR', 'DISH', 'REGN', 'TXN', 'LMT', 'BAM', 'NKE', 'KLAC', 'PAYX', 'AMT', 'DM', 'FIS', 'AMD', 'HPQ', 'ACN', 'UL', 'SWN', 'CHTR', 'EPD', 'TWTR', 'ILMN', 'GSK', 'MOMO', 'BZUN', 'BTI', 'FTI', 'BDX', 'FDX', 'CDNS', 'ADSK', 'TRI', 'ZM', 'RBLX', 'TJX', 'TTM', 'RACE', 'DHR', 'SHOP', 'IQV', 'NEM', 'NTR', 'VZ', 'AIG', 'GEVO', 'NRG', 'MRVL', 'PBR', 'KO', 'ISRG', 'MMC', 'JNPR', 'RY', 'ETN', 'AMZN', 'SOHU', 'RDS-B', 'KBH', 'AMAT', 'BLK', 'CP', 'PRU', 'RIO', 'T', 'COST', 'HCA', 'VTI', 'FISV', 'PBR-A', 'SAP', 'SNP', 'AXP', 'BTO', 'PG', 'ECL', 'M', 'SLB', 'HNP', 'HIG', 'FRHC', 'ZYNE', 'SQ', 'UA', 'A', 'LLY', 'ENB', 'VEON', 'DOW', 'MSFT', 'COF', 'JPM', 'ABT', 'NSC', 'KMB', 'STZ', 'TSLA', 'MRNA', 'SAN', 'CME', 'RIG', 'IBN', 'PGR', 'MDT', 'DE', 'KHC', 'CNQ', 'APD', 'EQNR', 'TWLO', 'NOK', 'RTX', 'OXY', 'COP', 'BK', 'BUD', 'NVO', 'D', 'TAK', 'MLM', 'CSCO', 'VMW', 'MELI', 'LEVI', 'LOW', 'AAPL', 'BNS', 'PTR', 'CVX', 'ING', 'SKLZ', 'BR', 'TM', 'GS', 'NGG', 'IBM', 'ORCL', 'SMFG', 'AVP', 'BABA', 'CB', 'MDLZ', 'SO', 'AMX', 'MAR', 'MSI', 'IDXX', 'BMY', 'ALGN', 'PLTR', 'TROW', 'CIEN', 'CTAS', 'EOG', 'F', 'ADI', 'GDEV', 'NXPI', 'NU', 'PANW', 'MFGP', 'STM', 'V', 'LULU', 'BIDU', 'FCX', 'SNAP', 'PLD', 'USB', 'BA', 'PEP', 'ZTS', 'RDS-A', 'ABB', 'SONY', 'SPOT', 'LPL', 'COUR', 'NEE', 'RSG', 'TAL', 'KOPN', 'SPGI', 'DAL', 'ITT', 'NOW', 'WM', 'RELX', 'JNJ', 'JCI', 'ABNB', 'BNGO', 'SWI', 'HHR', 'KEP', 'SYK', 'VIPS', 'BNTX', 'ENDP', 'NTAP', 'HUM', 'PNC', 'EQIX', 'LI', 'INFY', 'CHKP', 'MCD', 'WIT', 'TMUS', 'HSBC', 'MCHP', 'SHW', 'EBAY', 'INSG', 'TT', 'CHK', 'CM', 'CNC', 'BAC', 'CRM', 'UBS', 'LFC', 'BKNG', 'DBX', 'VNR', 'PM', 'FOLD', 'INTC', 'QCOM', 'KDP', 'BBL', 'TRIT', 'AZN', 'SBUX', 'INFO', 'DUK', 'CMCSA', 'MLCO', 'DEO', 'E', 'AA', 'MCO', 'SCHW', 'ANTM', 'TGT', 'MNST', 'MUFG', 'NOC', 'SE', 'SPG', 'UBER', 'TRP', 'DIS', 'ADP', 'ASML', 'DLR', 'GE', 'MRK', 'SLDB', 'GILD', 'DD', 'AON', 'QIWI', 'AVGO', 'TEAM', 'MBT', 'GD', 'MVIS', 'NVS', 'AWH', 'WFC', 'JD', 'ORLY', 'ITW', 'TEL', 'HMC', 'EMR', 'PYPL', 'ADBE', 'CPNG', 'DASH', 'DG', 'APPH', 'NIO', 'MMM', 'CI', 'YNDX', 'MS', 'SNOW', 'MSCI', 'AMGN', 'FB', 'CNI', 'STLA', 'EXC', 'DISCA', 'TFC', 'CTSH', 'ATVI', 'VRTX', 'GOLD', 'NVDA', 'SNY', 'SCCO', 'CCL', 'ICE', 'WBK', 'GOOG', 'FTNT', 'DELL', 'BHP', 'PAAS', 'MET', 'TCS', 'CMI', 'CCI', 'WMT', 'XLNX', 'DDOG', 'LCID', 'CMG', 'BX', 'APA', 'VALE', 'AEP', 'BMO', 'ZS', 'BP', 'PSA', 'EL', 'ABBV', 'SAVA', 'TMO', 'HDB', 'ACH', 'WDAY', 'LYG', 'COTY', 'UPS', 'BCE', 'MO', 'GM', 'CVS', 'VLO', 'NTES', 'CSX', 'C', 'PCAR', 'VRSN', 'CRWD', 'PFE', 'TTE', 'XOM', 'ROP', 'INTU', 'XRX', 'COIN', 'LRCX', 'OIS', 'SNPS', 'RIDE', 'FSLR'}
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.438'
        }
        try:
            response = requests.get(URL_d, headers = HEADERS)
        except:
            response = requests.get(URL_d, headers = HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        #прайс это скока стоит одна акция
        price = ''
        for tag in soup.find_all('span', class_ = 'IsqQVc NprOob wT3VGc'):
            price += tag.text
        if price != '':
            answer.append([ans1, float(unidecode.unidecode(price).replace(',', '.').replace(' ', '')), ans2])
        else:
            answer.append([ans1, 0.0, ans2])
    
async def spis(num):
    global flag_ans
    #проверка проспамил ли бот
    if num == '1':
        #спам компаниями
        for i in listok:
            await client.send_message(OUTPUT_CHANNEL1, i)
            time_begin = time.time()
            await asyncio.sleep(1.25)
            while not flag_ans:
                if (time.time() - time_begin > 10):
                    time_begin = time.time()
                    await client.send_message(OUTPUT_CHANNEL1, i)
                await asyncio.sleep(0.5)
            flag_ans = False
        s = ''
        for i in my_sort(answer):
            s += str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n'
        out = open('answer.txt', 'w')
        out.writelines(s)
        out.close()
        print('I`m finished!')
                
    
@client.on(events.NewMessage(chats=(OUTPUT_CHANNEL1)))
async def normal_handler(event):
    global flag_ans
    #реакция на ответ бота
    flag_ans = True
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
    await inf(event.id)

client.start()
client.run_until_disconnected()
