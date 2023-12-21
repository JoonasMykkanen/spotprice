# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    db.py                                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 14:10:39 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 18:50:36 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# IMPORTANT NOTE
# All data inside db is going to be in [unit / hour] format
# except date.... dumass :D

from .utils.helpers import getTimeStamp
from peewee import *

db = SqliteDatabase('database.db')

class BaseModel(Model):
	timestamp = DateTimeField(index=True, default=getTimeStamp)

	class Meta:
		database = db
		order_by = ('timestamp',)

# Frequency: 60min
# Content: JSON 
# Example: {"Rig_[idx]: [kWh]"}
class PowerConsumption(BaseModel):
	value = TextField()

# Frequency: 60min
# Content: Float 
# Example: snt / [kWh] where kWh is a float
class ElectricityPrice(BaseModel):
	value = FloatField()

# Frequency: 60min
# Content: Integer 
# Example: MH/S average over 60 minute period
class HashRate(BaseModel):
	value = IntegerField()

# Frequency: 60min
# Content: Float [eur / hour]
# Example: Income - cost
class Profit(BaseModel):
	value = FloatField()

# Frequency: 60min
# Content: Float [eur / hour]
# Example: usage[kWh] * price[snt] converted to eur / hour
# NOTE: this is combined running costs, individual rigs can
# be calculated by querying their power usage and spot price
class Cost(BaseModel):
	value = FloatField()

# Frequency: 60min
# Content: interger
# Example: [EUR / BTC]
class priceBTC(BaseModel):
	value = IntegerField()

db.connect()
db.create_tables([
	ElectricityPrice,
	PowerConsumption,
	priceBTC,
	HashRate,
	Cost
])
