# задание основное
# В базе полученных данных о различных ICO проектах (все источники), необходимо выделить ссылки на телеграмм группы,
# Создать Телеграмм клиента, авторизоваться, посетить полученые группы и собрать список участников данных групп.
# В базе данных создать коллекцию в которой хранить Список пройденных каналов, имя канала, количество участников.
# Отдельно создать коллекцию для людей, где с привязкой к группе хранить информацию о людях.
#
# В результате, при анализе данных необходимо получив ICO проект из базы, выделить группу (если есть), и список участников.
# Так-же должно легко получиться проанализировать частовстречающихся пользователей в этих группах.
#
# Для тех кто желает чуть расширить задачу
# можно попробовать проанализировать и понять какой пользователь Телеграмм соответсвует Учатнику ICO или Advisor

from telethon import TelegramClient
import re
import socks
from pymongo import MongoClient


CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico  # Название базы данных: ico
documents = MONGO_DB.icobench  # Название коллекции документов


re_tg_link = re.compile('http(s?):\/\/(t.me|telegram.me)\/[\d?=\-_a-zA-Z]+')

result = documents.find({"ico_socials": {'$regex': re_tg_link}})

tg_links = []
for itm in result:
    a = itm['ico_socials']
    for i in a:
        if re.fullmatch(re_tg_link, i):
            tg_links.append(i)

print(tg_links)


# Стучимся в телегу
api_id = 777269
api_hash = '528cba48d3ea90a3afa789f6790c1ed0'

proxy = {
    'server_ip': '138.128.118.100',
    'server_port': 42970,
    'login': '',
    'pass': '',
}

client = TelegramClient('che1', api_id, api_hash,
                        proxy=(socks.SOCKS5, proxy['server_ip'], proxy['server_port'], True))

client.start()
dialogs = client.get_dialogs()

print(dialogs[0])

print('*'*8, 'DONE', '*'*8)
#
urls = []
re_path = re.compile(r'http(s?):\/\/[\da-z-_]+.[a-z]+\/?[\d\?=\-_a-zA-Z]+')

for message in client.iter_messages(dialogs[0]):
    if not message.text and not message.web_preview:
        continue
    url_str = message.web_preview.url if message.web_preview else message.text

    try:
        match = re.fullmatch(re_path, url_str)
        if match:
            urls.append(match.group())
            print(match.group())
    except Exception as e:
        print(e)

with open('message.txt', 'w') as file:
    file.write('\n'.join(urls))


