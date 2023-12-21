# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    nicehashService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 09:14:03 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 11:19:13 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..utils.nicehash import private_api
from datetime import timedelta
from datetime import datetime
from datetime import timezone
from flask import current_app
import requests

from pprint import pprint

url = 'https://api2.nicehash.com'

class nicehashAPI:
	def __init__(self):
		self.error = False
		self.api = None
	
	def setup(self):
		secret = current_app.config['NICEHASH_SECRET']
		key = current_app.config['NICEHASH_KEY']
		id = current_app.config['NICEHASH_ID']
		self.api = private_api(url, id, key, secret)
		self.testConnection()
		return self

	# instantly test connection during init
	def testConnection(self):
		try:
			self.api.get_accounts()
			print(f'Nicehash api connected succesfully')
		except Exception as e:
			print(f'NicehashAPI: testConnection: {e}')
			self.error = True

	# Returning [BTC / EUR] integer to quicly calculate profitablity
	def getBtcPrice(self):
		try:
			response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur')
			response.raise_for_status()
			data = response.json()
			return data['bitcoin']['eur']
		except Exception as e:
			print(f'nicehashAPI: getBitcoinPrice: {e}')
			self.error = True
			return 0
