# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    antminerService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 12:31:22 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/20 08:47:45 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import current_app
import requests

url = 'http://louhos.ddns.net:1111'

class antminerAPI:
	def __init__(self):
		self.headers = None
		self.error = False

	def setup(self):
		self.headers = {
			'Authorization': current_app.config['ANTMINER_AUTH']
		}
		self.testConnection()
		return self
	
	def testConnection(self):
		try:
			response = requests.get(url, headers=self.headers)
			response.raise_for_status()
			print('Antminer dashboard connected succesfully')
		except Exception as e:
			print(f'antminerAPI: testConnection: {e}')
			self.error = True