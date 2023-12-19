# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    initExternalApi.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 10:29:43 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 12:25:21 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# importing and defining lazy load for api imports
from ..services.nicehashService import nicehashAPI
from ..services.pushoverService import pushoverAPI
from ..services.tuyaService import tuyaAPI

def initExternalAPI(app):
	global nicehashAPI
	global pushoverAPI
	global tuyaAPI

	with app.app_context():
		app.config['nicehashAPI'] = nicehashAPI().setup()
		app.config['pushoverAPI'] = pushoverAPI().setup()
		app.config['tuyaAPI'] = tuyaAPI().setup()
