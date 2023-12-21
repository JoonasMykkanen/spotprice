# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    api.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/21 15:50:37 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 18:43:29 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from flask import Blueprint

from ..services.databaseService import *

apiBP = Blueprint('api', __name__)

@apiBP.route('/')
def root():
	return "Hello sir, nothing to see here :)"

@apiBP.route('/btc')
def btc():
	return getBtcPrice()

@apiBP.route('/spot')
def spot():
	return getElectricityPrice()

@apiBP.route('/power')
def power():
	return getPowerConsumption()

@apiBP.route('/hashrate')
def hashrate():
	return getHashRate()

@apiBP.route('/cost')
def cost():
	return getCost()

@apiBP.route('/profit')
def profit():
	return getProfit()
