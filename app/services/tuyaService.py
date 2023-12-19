# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tuyaService.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 10:53:45 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 12:06:33 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..utils.constants import *
from flask import current_app
from ..utils.rig import Rig
import tinytuya

# https://auth.tuya.com/?from=http%3A%2F%2Fiot.tuya.com%2F
class tuyaAPI:
	def __init__(self):
		self.api = None
		self.rigs = []
	
	def setup(self):
		secret = current_app.config['TUYA_SECRET']
		key = current_app.config['TUYA_KEY']
		self.api = tinytuya.Cloud(apiRegion='eu', apiKey=key, apiSecret=secret, apiDeviceID=current_app.config['R0S0_ID'])

		# Creating Rig objects from sockets
		for index in range(0, rig_count):
			socket0 = current_app.config[str(f'R{index}S0_ID')]
			socket1 = current_app.config[str(f'R{index}S1_ID')]
			try:
				self.rigs.append(Rig(index, self.api, s0=socket0, s1=socket1))
			except Exception as e:
				print(f'TuyaAPI: setup: {e}')

		
	