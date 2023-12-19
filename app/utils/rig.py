# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    rig.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 11:09:25 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 12:09:42 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

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

	def testConnection(self):
		try:
			res0 = self.api.getstatus(self.socket0)
			status0 = res0['result'][0]['value']
			res1 = self.api.getstatus(self.socket1)
			status1 = res1['result'][0]['value']
			if status0 == True and status1 == True:
				self.status = True
			else:
				self.status = False
			print(f'Rig{self.index}: connected')
		except Exception as e:
			print(f'Rig: testConnection: {e}')