# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    pushoverService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 12:13:49 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 12:23:31 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import current_app
import requests

url = 'https://api.pushover.net/1/messages.json'

class pushoverAPI:
	def __init__(self):
		self.payload = None
		self.user = None
		self.key = None
		self.url = url

	def setup(self):
		self.key = current_app.config['PUSHOVER_KEY']
		self.user = current_app.config['PUSHOVER_USER']
		self.testConnection()
	
	def testConnection(self):
		payload = {
			'token': self.key,
			'user': self.user,
			'message': 'Connection test'
		}
		try:
			response = requests.post(url, data=payload)
			response.raise_for_status()
			print('Pushover connected succesfully')
		except Exception as e:
			print(f'pushoverAPI: testConnection: {e}')
