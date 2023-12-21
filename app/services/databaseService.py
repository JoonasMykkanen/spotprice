# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    databaseService.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/21 11:03:02 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 13:12:51 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Contains push and get functions for each table in database

from pprint import pprint
from ..db import *

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
			response = priceBTC.select()
			for entry in response:
				print(entry.value)
		except Exception as e:
			print(f'Database: getBtcPrice: {e}')


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
            response = ElectricityPrice.select()
            for entry in response:
                print(entry.value)
        except Exception as e:
            print(f'Database: getElectricityPrice: {e}')



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
            response = PowerConsumption.select()
            for entry in response:
                print(entry.value)
        except Exception as e:
            print(f'Database: getPowerConsumption: {e}')



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
            response = HashRate.select()
            for entry in response:
                print(entry.value)
        except Exception as e:
            print(f'Database: getHashRate: {e}')



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
            response = Cost.select()
            for entry in response:
                print(entry.value)
        except Exception as e:
            print(f'Database: getCost: {e}')
