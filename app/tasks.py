# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tasks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 16:39:55 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 12:07:08 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# includes automatically called scheduled tasks
# scheduler found in /app/__init__.py

from .services.databaseService import *

# Contains all apis' that are supposed to be polled once an hour
apis = [
	'nicehashAPI', 	# profitability, btc price
	'antminerAPI', 	# hashrate
	'nordpoolAPI', 	# electric price
	'tuyaAPI'		# power usage
]

# Main function to run once an hour, will update database with fresh data
# and make decision on mining operations based on costs and incomes
def hourlyRun(app):
	with app.app_context():
		pass