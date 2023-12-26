# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    antminerService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 12:31:22 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/23 08:04:45 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# NOTE: This is probably only module that is currently not scalable
# with more rigs since this one only works with this specific address
# that is hosted by a specific machine.
# To make it scalable with multiple machines, will need to figure out a
# way to host them in the same endpoint with different paths that can
# be accessed based on rig index or something similar.

from .databaseService import pushHashRate
from flask import current_app
from pprint import pprint
import requests

baseUrl = 'http://louhos.ddns.net:1111'
statsUrl = '/cgi-bin/stats.cgi'

class antminerAPI:
	def __init__(self):
		self.headers = None
		self.error = False
		self.stats = None

	def setup(self):
		self.headers = {
			'Authorization': current_app.config['ANTMINER_AUTH']
		}
		self.testConnection()
		return self
	
	def testConnection(self):
		try:
			url = baseUrl + statsUrl
			response = requests.get(url, headers=self.headers)
			response.raise_for_status()
			print('Antminer dashboard connected succesfully')
		except Exception as e:
			print(f'antminerAPI: testConnection: {e}')
			self.error = True
	
	# Save all stats to api obj
	def getMinerStats(self):
		try:
			url = baseUrl + statsUrl
			response = requests.get(url, headers=self.headers)
			response.raise_for_status()
			data = response.json()
			self.stats = data
		except Exception as e:
			print(f'antminerAPI: testConnection: {e}')
			self.error = True

	# Returns current hashrate [MH / S] as float
	def getHashRate(self):
		try:
			self.getMinerStats()
			data = self.stats['STATS'][0]['rate_30m']
			return data
		except Exception as e:
			print(f'antminerAPI: getHashRate: {e}')
			self.error = True
			return 0
	
	# Returns fan speed, since there are four, will use the highest one
	def getFanRPM(self):
		self.getMinerStats()
		try:
			self.getMinerStats()
			data = self.stats['STATS'][0]['fan']
			return max(data)
		except Exception as e:
			print(f'antminerAPI: getFanRPM: {e}')
			self.error = True
			return 0
	
	# TODO: getters for Temp, Rejection rate, pool status
	def testRun(self):
		print(f'test from: {self.__class__.__name__}')

	# Will fetch all hourly data points for this api and push them to database
	def pollNewHourlyData(self):
		data = self.getHashRate()
		pushHashRate(data)
		print(f'{self.__class__.__name__} posted {data} into DB')
		return data
