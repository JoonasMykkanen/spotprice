# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    data.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/26 10:05:05 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/26 13:42:15 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import current_app
from flask import Blueprint
from json import dumps

dataBP = Blueprint('data', __name__)

@dataBP.route('/stats')
def stats():
	response = {}
	response['hashrate'] = current_app.config['antminerAPI'].getHashRate()
	response['status'] = current_app.config['tuyaAPI'].getBoolMode(0)
	response['fan'] = current_app.config['antminerAPI'].getFanRPM()
	response['power'] = current_app.config['tuyaAPI'].getPower()

	response_json = dumps(response)
	return response_json

@dataBP.route('/today')
def today():
	pass