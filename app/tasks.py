# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tasks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 16:39:55 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 15:23:04 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# includes automatically called scheduled tasks
# scheduler found in /app/__init__.py

# Contains all apis' that are supposed to be polled once an hour
apis = [
	'nicehashAPI', 	# profitability, btc price
	'nordpoolAPI', 	# electric price
	'antminerAPI', 	# hashrate
	'tuyaAPI'		# power usage
]

# Main function to run once an hour, will update database with fresh data
# and make decision on mining operations based on costs and incomes
def hourlyRun(app):
	with app.app_context():
		for api in apis:
			app.config[f'{api}'].pollNewHourlyData()