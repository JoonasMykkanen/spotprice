# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tasks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 16:39:55 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 13:26:45 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# includes automatically called scheduled tasks
# scheduler found in /app/__init__.py

from .services.databaseService import *

# Contains all apis' that are supposed to be polled once an hour
apis = [
	'nicehashAPI', 	# profitability, btc price
	'nordpoolAPI', 	# electric price
	'antminerAPI', 	# hashrate
	'tuyaAPI'		# power usage
]

def	pollDataPoints(app):
	for api in apis:
		app.config[f'{api}'].testRun()


# Main function to run once an hour, will update database with fresh data
# and make decision on mining operations based on costs and incomes
def hourlyRun(app):
	with app.app_context():
		pollDataPoints(app)
