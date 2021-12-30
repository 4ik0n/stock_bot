from bs4 import BeautifulSoup
import requests
import asyncio
import time
import fileinput
import unidecode
from telethon import TelegramClient, sync, events

INPUT_CHANNEL1 = 'https://t.me/joinchat/AAAAAFLDCjpm9veBn68xUQ'
OUTPUT_CHANNEL1 = '@stocks_analyst_bot'

api_id = 18191105
api_hash = '01b32c4a3a7b04deb4960b874af0d50e'

TAGS = ['#TAG1', '#TAG2']

client = TelegramClient('Session', api_id, api_hash)

print("Client Created")

lines = open('text.txt', 'r').readlines()
lines[0] = '1'
out = open('text.txt', 'w')
out.writelines(lines)
out.close()

id_step = 2

#тикеры компаний
if id_step == 1:
    listok = open('spis.txt', 'r').readlines()
elif id_step == 2:
    listok = open('case.txt', 'r').readlines()
for j, i in enumerate(listok):
    listok[j] = i[:len(i) - 1]
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
    global answer
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
        f = open('ua.txt', 'r')
        i = f.read()
        HEADERS = {
            'user-agent': i
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
            await asyncio.sleep(3)
            while not flag_ans:
                if (time.time() - time_begin > 30):
                    time_begin = time.time()
                    await client.send_message(OUTPUT_CHANNEL1, i)
                await asyncio.sleep(0.25)
            flag_ans = False
        await write()
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
    exit(0)

async def write():
    global id_step
    global answer
    if id_step == 1:
        s = ''
        for i in my_sort(answer):
            s += str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n'
        out = open('answer.txt', 'w')
        out.writelines(s)
        out.close()
    elif id_step == 2:
        s = ''
        for i in my_sort(answer):
            if (i[0] < 80):
                s += str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + '\n'
        out = open('sell.txt', 'w')
        out.writelines(s)
        out.close()
        

client.start()
client.run_until_disconnected()
