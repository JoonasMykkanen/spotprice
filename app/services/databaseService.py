# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    databaseService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/21 11:03:02 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 19:14:03 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Contains push and get functions for each table in database

from flask import jsonify
from ..db import *
import json

# TABLE: bitcoin price getter and setter
def pushBtcPrice(data):
	with db.atomic():
		try:
			newEntry = priceBTC.create(value=data)
			newEntry.save()
		except Exception as e:
			print(f'Database: pushBtcPrice: {e}')

def getBtcPrice():
    with db.atomic():
        try:
            response = {}
            data = priceBTC.select()
            for entry in data:
                response[entry.timestamp] = {'value': entry.value}
            return jsonify(response)
        except Exception as e:
            print(f'Database: getBtcPrice: {e}')
            return jsonify({'error': str(e)})


# TABLE: Electricity price data price getter and setter
def pushElectricityPrice(data):
    with db.atomic():
        try:
            newEntry = ElectricityPrice.create(value=data)
            newEntry.save()
        except Exception as e:
            print(f'Database: pushElectricityPrice: {e}')

def getElectricityPrice():
    with db.atomic():
        try:
            response = {}
            data = ElectricityPrice.select()
            for entry in data:
                response[entry.timestamp] = {'value': entry.value}
            return jsonify(response)
        except Exception as e:
            print(f'Database: getElectricityPrice: {e}')
            return jsonify({'error': str(e)})



# TABLE: power consumption price data price getter and setter
def pushPowerConsumption(data):
    with db.atomic():
        try:
            newEntry = PowerConsumption.create(value=data)
            newEntry.save()
        except Exception as e:
            print(f'Database: pushPowerConsumption: {e}')

def getPowerConsumption():
    with db.atomic():
        try:
            response = {}
            data = PowerConsumption.select()
            for entry in data:
                jsonData = entry.value
                response[entry.timestamp.isoformat()] = {'value': jsonData}
            return jsonify(response)
        except Exception as e:
            print(f'Database: getPowerConsumption: {e}')
            return jsonify({'error': str(e)})



# TABLE: hashrate price data price getter and setter
def pushHashRate(data):
    with db.atomic():
        try:
            newEntry = HashRate.create(value=data)
            newEntry.save()
        except Exception as e:
            print(f'Database: pushHashRate: {e}')

def getHashRate():
    with db.atomic():
        try:
            response = {}
            data = HashRate.select()
            for entry in data:
                response[entry.timestamp] = {'value': entry.value}
            return jsonify(response)
        except Exception as e:
            print(f'Database: getHashRate: {e}')
            return jsonify({'error': str(e)})



# TABLE: cost price data price getter and setter
def pushCost(data):
    with db.atomic():
        try:
            newEntry = Cost.create(value=data)
            newEntry.save()
        except Exception as e:
            print(f'Database: pushCost: {e}')

def getCost():
    with db.atomic():
        try:
            response = {}
            data = Cost.select()
            for entry in data:
                response[entry.timestamp] = {'value': entry.value}
            return jsonify(response)
        except Exception as e:
            print(f'Database: getCost: {e}')
            return jsonify({'error': str(e)})



# TABLE: profit price data price getter and setter
def pushProfit(data):
    with db.atomic():
        try:
            newEntry = Profit.create(value=data)
            newEntry.save()
        except Exception as e:
            print(f'Database: pushProfit: {e}')

def getProfit():
    with db.atomic():
        try:
            response = {}
            data = Profit.select()
            for entry in data:
                response[entry.timestamp] = {'value': entry.value}
            return jsonify(response)
        except Exception as e:
            print(f'Database: getCost: {e}')
            return jsonify({'error': str(e)})
