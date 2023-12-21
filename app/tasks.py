# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tasks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 16:39:55 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 20:26:53 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# includes automatically called scheduled tasks
# scheduler found in /app/__init__.py

from .services.databaseService import pushCost
from pprint import pprint
import json

# Contains all apis' that are supposed to be polled once an hour
apis = [
	'nicehashAPI', 	# profitability, btc price
	'nordpoolAPI', 	# electric price
	'antminerAPI', 	# hashrate
	'tuyaAPI'		# power usage
]

DAY = 24

# All rigs combined cost for given hour
def pollCost(data):
	rigs = json.loads(data['tuyaAPI'])
	spot = data['nordpoolAPI']
	kWh = 0
	
	for rig in rigs:
		for name, value in rig.items():
			kWh  += value
	
	cost = (kWh * spot) / 100 # convert snt / kWh --> eur / kWh
	pushCost(cost)
	return cost

# All rigs combined profit for given hour
def pollProfit(data, cost):
	profitability = data['profitability']
	coinValue = data['nicehashAPI']
	grossRevenue = (profitability * coinValue) / DAY
	# TODO add post for revenue if want to, not for MVP So gonna skip for now
	print(grossRevenue)
	profit = grossRevenue - cost
	print(profit)

# Will fill in the blanks since not everything can be directly accessed
# Some data will need to be calculated and manipulated before saving
# for example: cost, profit
def handleOtherTables(data):
	pprint(data)
	cost = pollCost(data)
	pollProfit(data, cost)
	

# Main function to run once an hour, will update database with fresh data
# and make decision on mining operations based on costs and incomes
def hourlyRun(app):
	with app.app_context():
		data = {}
		for api in apis:
			apiData = app.config[f'{api}'].pollNewHourlyData()
			data[api] = apiData

		# Gather data that was not gotten from automatic poll
		# Such as: profitability, 
		data['profitability'] = app.config['nicehashAPI'].getProfitability()
		
		handleOtherTables(data)

