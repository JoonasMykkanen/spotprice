# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    db.py                                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 14:10:39 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/20 14:43:47 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# IMPORTANT NOTE
# All data inside db is going to be in [unit / hour] format
# except date.... dumass :D

# TODO: change imports to only used ones after module is ready
from peewee import *

from .utils.helpers import getTimeStamp

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
	kWh = TextField()

# Frequency: 60min
# Content: JSON 
# Example: {"Rig_[idx]: [Boolean]"} bool value based on if the rig was online during this hour
class RigStatus(BaseModel):
	status = BooleanField()

# Frequency: 60min
# Content: Float 
# Example: snt / [kWh] where kWh is a float
class ElectricityPrice(BaseModel):
	price = FloatField()

# Frequency: 60min
# Content: Integer 
# Example: MH/S average over 60 minute period
class HashRate(BaseModel):
	mhs = IntegerField()

# Frequency: 60min
# Content: Float [eur / hour]
# Example: Income - cost
class Profit(BaseModel):
	amount = FloatField()

# Frequency: 60min
# Content: Float [eur / hour]
# Example: usage[kWh] * price[snt] converted to eur / hour
class Cost(BaseModel):
	amount = FloatField()

# Frequency: 60min
# Content: interger
# Example: [EUR / BTC]
class priceBTC(BaseModel):
	value = IntegerField()

db.connect()
db.create_tables([
	ElectricityPrice,
	PowerConsumption,
	RigStatus,
	priceBTC,
	HashRate,
	Cost
])