from flask import Flask, render_template_string
from datetime import datetime, timedelta
from dotenv import load_dotenv
from nordpool import elspot
import time as clock
import threading
import requests
import nicehash
import pytz
import os

app = Flask(__name__)

# Custom print function to also store logs in flask
def flask_print(msg):
    global flask_output
    flask_output.append(msg)
    print(msg)

# Function to display flask logs
@app.route('/output')
def display():
    global flask_output
    return render_template_string('<br>'.join(flask_output))

# Get timestamp for logs
def current_time(): return datetime.now(pytz.timezone('Europe/Helsinki')).strftime('%D %H:%M:%S')

# Convert eur / MWh to snt / KWh and also add VAT 24%
# also add transfer costs of electricity
def calculate_actual_price(price): return ((price / 10) * 1.24) + electricity_transfer

# send_notification('<Your User Key>', '<Your API Token>', 'This is a test message')
def send_notification(message):
	payload = {
        'token': pushover_key,
        'user': pushover_user,
        'message': message,
	}
	flask_print("Log: " + message)
	req = requests.post(pushover_url, data=payload)
	if (req.status_code == 200):
		flask_print(f"{current_time()} Log: Notification sent")
	else:
		flask_print(f"{current_time()} Log: Notification failed {req.status_code}")

# Get next hour price for electricity spot pricces
# RETURN: snt / h
def price_for_next_hour():
	next = datetime.now(pytz.timezone('Europe/Helsinki')) + timedelta(hours=1)
	current_day_cet = datetime.now().date()
	prices = nordpool_api.hourly(end_date=current_day_cet, areas=finland)
 
	for area, data in prices['areas'].items():
		for hour_data in data['values']:
			start_time = (hour_data['start'] + timedelta(hours=2))
			end_time = (hour_data['end'] + timedelta(hours=2))
			if next.hour == start_time.hour:
				price = round(calculate_actual_price(hour_data['value']), 2)
				flask_print(f"{current_time()} Log: {start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}: {price}snt/kWh")
    
				return price

# Retrives current btc price
# RETURN: eur / btc
def get_btc_price():
	response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
	data = response.json()
	price = round(data['bpi']['EUR']['rate_float'], 2)
	flask_print(f"{current_time()} Log: btc price: {price}€/btc")
	
	return price

# Calculate last hours profitability to decide wheter next hour is worth it
# RETURN: snt / h
def get_profitability():
    last_hour = []
    start = datetime.now(pytz.timezone('Europe/Helsinki'))
    
    while start.hour != end_of_hour:
        start = datetime.now(pytz.timezone('Europe/Helsinki'))
        miner = nicehash_api.get_rigs()
        last_hour.append(miner['totalProfitability'])
        clock.sleep(60)
	
    bitcoin_price = round(get_btc_price(), 2)
    profitability = round((((sum(last_hour) / len(last_hour)) * bitcoin_price) / 24), 2)
    flask_print(f"{current_time()} Log: Profitability for next hour {profitability}€/h")
    
    return profitability

# mainloop
def background_task():
	running = True
	send_notification("Starting script")
	while running == True:
		income = get_profitability()
		cost = (price_for_next_hour() / 100)
		profit = round(income - cost, 2)
		flask_print(f"{current_time()} Log: income:{income}€ - cost:{cost}€ = {profit}€/hour")
		if (profit < max_price):
			send_notification(f"Price check: \U0000274C")
		else:
			send_notification(f"Price check: \U00002705")

# Define constants
pushover_url = 'https://api.pushover.net/1/messages.json'
nicehas_url = 'https://api2.nicehash.com'
finland = ['FI']
electricity_transfer = 4.69 + 2.79	# transfer + tax
end_of_hour = 50					# minutes
max_price = 0.1						# eur / kWh

# getting env variables
load_dotenv()
nicehash_secret = os.getenv("NICEHASH_SECRET")
nicehash_key = os.getenv("NICEHASH_API_KEY")
nicehash_id = os.getenv("NICEHASH_ID")
pushover_key = os.getenv("PUSHOVER_API_KEY")
pushover_user = os.getenv("PUSHOVER_USER")

# init
nicehash_api = nicehash.private_api(nicehas_url, nicehash_id, nicehash_key, nicehash_secret)
nordpool_api = elspot.Prices(currency='EUR')

# flask stuff
flask_output = []
@app.route('/')
def home():
    return "Starting script..."

# running flask app
if __name__ == "__main__":
    thread = threading.Thread(target=background_task)
    thread.start()
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))