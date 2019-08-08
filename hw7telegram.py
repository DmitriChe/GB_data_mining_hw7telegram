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
import pymongo
import re
import socks
from pymongo import MongoClient


CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.hhru  # Название базы данных: ico
collection_hhru = MONGO_DB.people  # Название коллекции документов: hhru

proxy = {
    'server': '192.169.249.49',
    'port': 62644,
    'login': '',
    'pass': '',
}
api_id = 777269
api_hash = '528cba48d3ea90a3afa789f6790c1ed0'


client = TelegramClient('che1', api_id, api_hash,
                        proxy=(socks.SOCKS5, '192.169.249.49', 62644, True))

client.start()
dialogs = client.get_dialogs()

print(dialogs[0])

print(23232)

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


