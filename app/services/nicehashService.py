# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    nicehashService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 09:14:03 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 12:33:46 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..utils.nicehash import private_api
from flask import current_app

url = 'https://api2.nicehash.com'

class nicehashAPI:
	def __init__(self):
		self.api = None
	
	def setup(self):
		secret = current_app.config['NICEHASH_SECRET']
		key = current_app.config['NICEHASH_KEY']
		id = current_app.config['NICEHASH_ID']
		self.api = private_api(url, id, key, secret)
		self.testConnection()

	# instantly test connection during init
	def testConnection(self):
		try:
			my_accounts = self.api.get_accounts()
			print(f'Nicehash api connected succesfully')
		except Exception as e:
			print(f'NicehashAPI: testConnection: {e}')
	