# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    data.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/26 10:05:05 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/28 09:31:48 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..utils.helpers import parseTimestamp
from ..utils.helpers import getTimeStamp
from datetime import timedelta
from datetime import datetime
from flask import current_app
from flask import Blueprint
from pprint import pprint
from json import dumps
from ..db import *

dataBP = Blueprint('data', __name__)

@dataBP.route('/stats')
def stats():
	response = {}
	response['hashrate'] = current_app.config['antminerAPI'].getHashRate()
	response['status'] = current_app.config['tuyaAPI'].getBoolMode(0) # TODO: Does not scale to multiple rigs
	response['fan'] = current_app.config['antminerAPI'].getFanRPM()
	response['power'] = current_app.config['tuyaAPI'].getPower()

	response_json = dumps(response)
	return response_json

# TODO: Move queries to their own dabaseService module and provide function for get method
@dataBP.route('/today')
def today():
	with db.atomic():
		revenue = Revenue.select().order_by(Revenue.timestamp.desc()).limit(24)
		profit = Profit.select().order_by(Profit.timestamp.desc()).limit(24)
		cost = Cost.select().order_by(Cost.timestamp.desc()).limit(24)
	
	today = parseTimestamp(getTimeStamp())

	totalRevenue = 0
	for entry in revenue:
		entryDate = parseTimestamp(entry.timestamp)
		if today.date() == entryDate.date():
			totalRevenue += entry.value

	totalProfit = 0
	for entry in profit:
		entryDate = parseTimestamp(entry.timestamp)
		if today.date() == entryDate.date():
			totalProfit += entry.value

	totalCost = 0
	for entry in cost:
		entryDate = parseTimestamp(entry.timestamp)
		if today.date() == entryDate.date():
			totalCost += entry.value

	response = {}
	response['revenue'] = round(totalRevenue, 2)
	response['profit'] = round(totalProfit, 2)
	response['cost'] = round(totalCost, 2)

	return dumps(response)



@dataBP.route('/month')
def month():
	with db.atomic():
		# 744 = 31 days * 24 hours = 744 --> will filter overflow out based on datetime
		revenueData = Revenue.select().order_by(Revenue.timestamp.desc()).limit(744)
		profitData = Profit.select().order_by(Profit.timestamp.desc()).limit(744)
		costData = Cost.select().order_by(Cost.timestamp.desc()).limit(744)

	endDate = datetime.now()
	delta = endDate.day - 1
	startDate = datetime.now() - timedelta(days=(delta))
	
	labels = []
	while startDate.day <= endDate.day:
		labels.append(startDate.strftime('%d-%m'))
		startDate += timedelta(days=1)

	# for entry in revenueData:
	# 	time = parseTimestamp(entry.timestamp)
	# 	while time.day >= parseTimestamp(entry.timestamp).day:
	# 		continue
	# 	labels.append(time.strftime('%d-%m'))
		
	print(labels)

	revenue = []
	for entry in revenueData:
		revenue.append(entry.value)

	profit = []
	for entry in profitData:
		profit.append(entry.value)

	cost = []
	for entry in costData:
		cost.append(entry.value)
		
	data = {
		"labels": labels,
		"datasets": [
			{
				"label": "Revenue",
				"data": revenue,
				"borderColor": "rgb(54, 162, 235)",
            	"backgroundColor": "rgba(54, 162, 235, 0.5)",
			},
			{
				"label": "Profit",
				"data": profit,
				"borderColor": "rgb(75, 192, 192)",
            	"backgroundColor": "rgba(75, 192, 192, 0.5)",
			},
			{
				"label": "Cost",
				"data": cost,
				"borderColor": "rgb(255, 99, 132)",
            	"backgroundColor": "rgba(255, 99, 132, 0.5)",
			},
		]
	}
	
	return dumps(data)



	
		
