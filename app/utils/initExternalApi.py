# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    initExternalApi.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 10:29:43 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/20 11:53:04 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# importing and defining lazy load for api imports
from ..services.nicehashService import nicehashAPI
from ..services.pushoverService import pushoverAPI
from ..services.antminerService import antminerAPI
from ..services.nordpoolService import nordpoolAPI
from ..services.tuyaService import tuyaAPI

def initExternalAPI(app):
	global nicehashAPI
	global pushoverAPI
	global antminerAPI
	global nordpoolAPI
	global tuyaAPI

	with app.app_context():
		# app.config['nicehashAPI'] = nicehashAPI().setup()
		# app.config['pushoverAPI'] = pushoverAPI().setup()
		# app.config['antminerAPI'] = antminerAPI().setup()
		# app.config['nordpoolAPI'] = nordpoolAPI().setup()
		app.config['tuyaAPI'] = tuyaAPI().setup()
		app.config['tuyaAPI'].getStatus()
		app.config['tuyaAPI'].getPower()
