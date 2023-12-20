# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tasks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 16:39:55 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 17:08:00 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# includes automatically called scheduled tasks
# scheduler found in /app/__init__.py

apis = [
	'nicehashAPI', 	# profitability, btc price
	'antminerAPI', 	# hashrate
	'nordpoolAPI', 	# electric price
	'tuyaAPI'		# power usage
]

# Will call pushNewData() once for each api
def updateDatabases(app):
	with app.app_context():
		for api in apis:
			pass