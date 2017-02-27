# # -*- coding: utf-8 -*-

import time
import eventlet
import requests
import logging
import telebot
from time import sleep

# Каждый раз получаем по 10 последних записей со стены
URL_VK = 'https://api.vk.com/method/wall.get?domain=kaspercareer&count=10&filter=owner'
BOT_TOKEN = '349421716:AAECbgHPZrUU0E6XMhTR3q-DnbwtYliPDYY'
FILENAME_VK = 'last_known_id.txt'
BASE_POST_URL = 'https://vk.com/wall-98006063_'
SINGLE_RUN = 0

bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
	f = open('chats.txt')
	text = f.read()
	if not str(message.chat.id) in text:
		#print('here')
		bot.send_message(message.chat.id,"ЛК — это:\n— 37 офисов на всех континентах и штаб-квартира в Москве;\n — 400 000 000 пользователей и 270 000 корпоративных клиентов во всех странах мира;\n — Круглосуточный мониторинг вирусной активности в четырех вирусных лабораториях в России, Китае, Великобритании и США;\n — Больше 3000 специалистов, треть из которых постоянно работает над более чем шести десятками уникальных программных решений для большинства существующих платформ;\n — Более 325 000 новых вредоносных программ, обнаруживаемых каждые 24 часа.\n — Своя атмосфера, в которой интересно и приятно работать.\nНаша группа ВК - https://vk.com/kaspercareer")
		f = open('chats.txt', 'a')
		f.write(str(message.chat.id)+"\n")
	else:
		bot.send_message(message.chat.id, "Вы уже подписались на нашу рассылку")
	f.close()

def get_data():
    timeout = eventlet.Timeout(10)
    try:
        feed = requests.get(URL_VK)
        return feed.json()
    except eventlet.timeout.Timeout:
        logging.warning('Got Timeout while retrieving VK JSON data. Cancelling...')
        return None
    finally:
        timeout.cancel()

def send_new_posts(items, last_id):
    for item in items:
        if item['id'] <= last_id:
            break
        link = '{!s}{!s}'.format(BASE_POST_URL, item['id'])
        f = open('chats.txt')
        for line in f:
        	bot.send_message(line, link)
        # Спим секунду, чтобы избежать разного рода ошибок и ограничений (на всякий случай!)
        time.sleep(1)
    return


def check_new_posts_vk():
    # Пишем текущее время начала
    logging.info('[VK] Started scanning for new posts')
    with open(FILENAME_VK, 'rt') as file:
        last_id = int(file.read())
        if last_id is None:
            logging.error('Could not read from storage. Skipped iteration.')
            return
        logging.info('Last ID (VK) = {!s}'.format(last_id))
    try:
        feed = get_data()
        # Если ранее случился таймаут, пропускаем итерацию. Если всё нормально - парсим посты.
        if feed is not None:
            entries = feed['response'][1:]
            try:
                # Если пост был закреплен, пропускаем его
                tmp = entries[0]['is_pinned']
                # И запускаем отправку сообщений
                send_new_posts(entries[1:], last_id)
            except KeyError:
                send_new_posts(entries, last_id)
            # Записываем новый last_id в файл.
            with open(FILENAME_VK, 'wt') as file:
                try:
                    tmp = entries[0]['is_pinned']
                    # Если первый пост - закрепленный, то сохраняем ID второго
                    file.write(str(entries[1]['id']))
                    logging.info('New last_id (VK) is {!s}'.format((entries[1]['id'])))
                except KeyError:
                    file.write(str(entries[0]['id']))
                    logging.info('New last_id (VK) is {!s}'.format((entries[0]['id'])))
    except Exception as ex:
        logging.error('Exception of type {!s} in check_new_post(): {!s}'.format(type(ex).__name__, str(ex)))
        pass
    logging.info('[VK] Finished scanning')
    return

if __name__ == '__main__':
    # Избавляемся от спама в логах от библиотеки requests
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    # Настраиваем наш логгер
    logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
    
    if not SINGLE_RUN:
        while True:
            check_new_posts_vk()
            # Пауза в 4 минуты перед повторной проверкой
            logging.info('[App] Script went to sleep.')
            time.sleep(60 * 4)
    else:
        check_new_posts_vk()
    logging.info('[App] Script exited.\n')

