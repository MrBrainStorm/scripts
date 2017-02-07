import requests
import misc
from yobit import get_btc
from time import sleep



token = misc.token
URL = 'https://api.telegram.org/bot' + token + '/'
# https://api.telegram.org/bot329543008:AAGG33WmXdWWC77OORfB3uLGTABowJRv3IE/sendmessage?chat_id=258077370&text=hi

global last_update_id
last_update_id = 0



def get_updates():
	url = URL + 'getupdates'
	r = requests.get(url)
	return r.json()



def get_message():

	#Отвечать только на новые сообщения.

	#Для этого получаем update_id каждого обновления
	#Записуем его в переменную и сравнить его с update_id последнего элемента в списке result
	data = get_updates()

	last_object = data['result'][-1]
	current_update_id = last_object['update_id']

	global last_update_id
	if last_update_id != current_update_id:
		last_update_id = current_update_id

		chat_id = last_object['message']['chat']['id']
		message_text = last_object['message']['text'] 
		message = {'chat_id': chat_id, 'text': message_text}
		return message
	return None



def send_message(chat_id, text='Please wait because i am bot...'):
	url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
	requests.get(url)



def main():


	while True:
		
		answer = get_message()
		
		if answer != None:
			
			chat_id = answer['chat_id']
			text = answer['text']
			
			if text == '/btc':
				
				send_message(chat_id, get_btc())
		else:
			
			continue
		
		sleep(2)



if __name__ == '__main__':
	main()