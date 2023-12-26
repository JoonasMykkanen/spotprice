# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    rigService.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 11:09:25 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/26 13:04:48 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from pprint import pprint

# commands for smart socets (on / off)
TURN_OFF = { "commands": [{"code": "switch_1", "value": False},{"code": "countdown_1", "value": 0},] }
TURN_ON = { "commands": [{"code": "switch_1", "value": True},{"code": "countdown_1", "value": 0},] }

class Rig:
	def __init__(self, index, api, s0, s1):
		self.status = None
		self.api = api
		self.socket0 = s0
		self.socket1 = s1
		self.index = index
		self.testConnection()
		self.error = False

	def testConnection(self):
		try:
			res0 = self.api.getstatus(self.socket0)
			status0 = res0['result'][0]['value']
			res1 = self.api.getstatus(self.socket1)
			status1 = res1['result'][0]['value']
			if status0 is True and status1 is True:
				self.status = True
			else:
				self.status = False
			print(f'Rig{self.index}: connected & status: {self.status}')
		except Exception as e:
			print(f'Rig: testConnection: {e}')
			self.error = True
		
	def switchOff(self):
		try:
			self.api.sendcommand(self.socket0, TURN_OFF)
			print(f'socket: {self.index} turned off')
			self.api.sendcommand(self.socket1, TURN_OFF)
			print(f'socket: {self.index} turned off')
		except Exception as e:
			print('Rig: switchOff: {e}')
			self.error = True
		self.updateStatus()
		return self.status
		
	def switchOn(self):
		try:
			self.api.sendcommand(self.socket0, TURN_ON)
			print(f'socket: {self.index} turned on')
			self.api.sendcommand(self.socket1, TURN_ON)
			print(f'socket: {self.index} turned on')
		except Exception as e:
			print('Rig: switchOff: {e}')
			self.error = True
		self.updateStatus()
		return self.status

	# Retrieve status from server and update local variable accordingly
	def updateStatus(self):
		try:
			res0 = self.api.getstatus(self.socket0)
			status0 = res0['result'][0]['value']
			res1 = self.api.getstatus(self.socket1)
			status1 = res1['result'][0]['value']
			if status0 is True and status1 is True:
				self.status = True
			elif status0 is False and status1 is False:
				self.status = False
			else:
				raise ValueError('Socket_0 & Socket_1 status does not match')
			print(f'Rig{self.index}: connected & status: {self.status}')
		except Exception as e:
			print(f'Rig: testConnection: {e}')
			self.error = True

	# Will return used power as [kWh] integer
	def getRigPower(self):
		try:
			response_S0 = self.api.getstatus(self.socket0)
			response_S1 = self.api.getstatus(self.socket1)
			data = response_S0['result'] + response_S1['result']
			curPower = 0
			for item in data:
				if item['code'] == 'cur_power':
					curPower += item['value']
			# TODO: Possible problem --> api claims to return W but in reality it's not.
			# if it were to return watts, each outlet would be drawing 15kW wich is not
			# possible, normally W / 1000 would give kW but now its divided by 10,000
			return curPower / 10000
		except Exception as e:
			print(f'Rig: getPowerUsage: {e}')
			self.error = True
			return None

	# will return if rig is online or offline [true / false]
	def getRigStatus(self):
		return self.status

			