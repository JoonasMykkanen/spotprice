# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tuyaService.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 10:53:45 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/20 12:01:13 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import current_app
from .rigService import Rig
import tinytuya
import json

from pprint import pprint

rigCount = 1

# https://auth.tuya.com/?from=http%3A%2F%2Fiot.tuya.com%2F
class tuyaAPI:
	def __init__(self):
		self.api = None
		self.rigs = []
		self.error = False
	
	def setup(self):
		secret = current_app.config['TUYA_SECRET']
		key = current_app.config['TUYA_KEY']
		self.api = tinytuya.Cloud(\
			apiRegion='eu', \
			apiKey=key, \
			apiSecret=secret, \
			apiDeviceID=current_app.config['R0S0_ID'] \
		)

		# Creating Rig objects from sockets
		for index in range(0, rigCount):
			socket0 = current_app.config[str(f'R{index}S0_ID')]
			socket1 = current_app.config[str(f'R{index}S1_ID')]
			try:
				self.rigs.append(Rig(index, self.api, s0=socket0, s1=socket1))
			except Exception as e:
				print(f'TuyaAPI: setup: {e}')
				self.error = True

		return self
	
	# Will return json object containing a list of rig and their power usage
	def getPower(self):
		try:
			response = []
			for index, rig in enumerate(self.rigs):
				response.append({f"Rig_{index}": rig.getRigPower()})
			responseJSON = json.dumps(response)
			return responseJSON
		except Exception as e:
			print(f'TuyaAPI: getPower: {e}')
			self.error = True
			return {}

	# Returns json object containing rig index and their status with [true / false]
	def getStatus(self):
		try:
			response = []
			for index, rig in enumerate(self.rigs):
				response.append({f"Rig_{index}": rig.getRigStatus()})
			responseJSON = json.dumps(response)
			return responseJSON
		except Exception as e:
			print(f'TuyaAPI: getStatus: {e}')
			self.error = True
			return "{}"