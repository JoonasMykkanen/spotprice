# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 09:19:59 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 12:38:45 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os

class Config:
	# Nicehash mining market place to get miner stats
	NICEHASH_KEY = os.environ.get('NICEHASH_KEY')
	NICEHASH_SECRET = os.environ.get('NICEHASH_SECRET')
	NICEHASH_ID = os.environ.get('NICEHASH_ID')

	# ENTSO api is nordic electricity spot price API
	ENTSO_KEY = os.environ.get('ENTSO_KEY')

	# Pushover is a notification system
	PUSHOVER_KEY = os.environ.get('PUSHOVER_KEY')
	PUSHOVER_USER = os.environ.get('PUSHOVER_USER')

	# Tuya is used to control smart sockets that rigs are connected to
	TUYA_KEY = os.environ.get('TUYA_KEY')
	TUYA_SECRET = os.environ.get('TUYA_SECRET')

	# Used with tuya api to identify each socket from local wifi network
	# each rig has 2 socets linked to them. NAMING: RIG[idx]SOCKET[idx]
	R0S0_ID = os.environ.get('R0S0_ID')		# RIG 0 SOCKET 0
	R0S0_ADDR = os.environ.get('R0S0_ADDR')	# RIG 0 SOCKET 0
	R0S0_KEY = os.environ.get('R0S0_KEY')	# RIG 0 SOCKET 0
	R0S1_ID = os.environ.get('R0S1_ID')		# RIG 0 SOCKET 1
	R0S1_ADDR = os.environ.get('R0S0_ADDR')	# RIG 0 SOCKET 1
	R0S1_KEY = os.environ.get('R0S0_KEY')	# RIG 0 SOCKET 1

	# antminer header
	ANTMINER_AUTH = os.environ.get('ANTMINER_AUTH')
