# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    nordpoolService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 15:03:14 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/24 12:11:40 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from .databaseService import pushElectricityPrice
from datetime import timedelta
from datetime import datetime
from nordpool import elspot
import pytz

transferCost = 6.59	# snt / kWh
defaultPrice = 10	# snt / kWh
FINLAND = ['FI']	# Area code
threshold = 20		# snt / kWh

# Helper function to return actual cost of electricity [eur / kWh]
def calcRealPrice(price):
	return round((((price / 10) * 1.24) + transferCost), 2)

class nordpoolAPI:
	def __init__(self):
		self.threshold = threshold
		self.error = False
		self.api = None
	
	def setup(self):
		self.api = elspot.Prices(currency='EUR')
		self.testConnection()
		return self

	# instantly test connection during init
	def testConnection(self):
		try:
			response = self.api.hourly(areas=FINLAND)
			print('NordPool connected succesfully')
		except Exception as e:
			print(f'nordpoolAPI: testConnection: {e}')
			self.error = True

	def getPrices(self, date):
		try:
			return self.api.hourly(end_date=date, areas=FINLAND)
		except Exception as e:
			print(f'nordpoolAPI: getPrices: {e}')
			return None

	# Returns [snt / kWh] price as float for next hour
	def	getNextHour(self):
		finlandTZ = pytz.timezone('Europe/Helsinki')
		next = datetime.now(pytz.timezone('Europe/Helsinki')) + timedelta(hours=1)
		currentDate = datetime.now(finlandTZ).date()
		prices = self.getPrices(currentDate)

		if not prices:
			print('nordpoolAPI: getNextHour: no data found for next hour... returning default')
			return calcRealPrice(defaultPrice)

		for area in prices['areas']:
			for price_data in prices['areas'][area]['values']:
				price_data['start'] = price_data['start'].astimezone(finlandTZ)
				price_data['end'] = price_data['end'].astimezone(finlandTZ)
				if (price_data['start'].hour == next.hour):
					return calcRealPrice(price_data['value'])
	
	# Returns [snt / kWh] price as float for current hour
	def	getCurHour(self):
		finlandTZ = pytz.timezone('Europe/Helsinki')
		cur = datetime.now(pytz.timezone('Europe/Helsinki'))
		currentDate = datetime.now(finlandTZ).date()
		prices = self.getPrices(currentDate)

		if not prices:
			print('nordpoolAPI: getCurHour: no data found for cur hour... returning default')
			return calcRealPrice(defaultPrice)

		for area in prices['areas']:
			for price_data in prices['areas'][area]['values']:
				price_data['start'] = price_data['start'].astimezone(finlandTZ)
				price_data['end'] = price_data['end'].astimezone(finlandTZ)
				if (price_data['start'].hour == cur.hour):
					return calcRealPrice(price_data['value'])
	
	def testRun(self):
		print(f'test from: {self.__class__.__name__}')
	
	# Will fetch all hourly data points for this api and push them to database
	def pollNewHourlyData(self):
		data = self.getCurHour()
		pushElectricityPrice(data)
		print(f'{self.__class__.__name__} posted {data} into DB')
		return data
	
	# returns current threshold value
	def getThreshold(self):
		return self.threshold
	
	# calculates new threshold
	# TODO: Finish logic for this
	def setThreshold(self):
		pass
