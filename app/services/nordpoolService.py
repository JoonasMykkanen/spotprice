# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    nordpoolService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 15:03:14 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/20 12:28:57 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import timedelta
from datetime import datetime
from nordpool import elspot
import pytz

transferCost = 6.59
defaultPrice = 10
FINLAND = ['FI']

# Helper function to return actual cost of electricity [eur / kWh]
def calcRealPrice(price):
	return ((price / 10) * 1.24) + transferCost

class nordpoolAPI:
	def __init__(self):
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
		
