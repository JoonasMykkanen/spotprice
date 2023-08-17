from flask import Flask, render_template_string
from datetime import datetime, timedelta
from dotenv import load_dotenv
from nordpool import elspot
import time as clock
import threading
import requests
import nicehash
import logging
import pytz
import os

app = Flask(__name__)

# Custom print function to also store logs in flask
# RETURN: None
def ft_print(msg):
    logger.info(msg)
    print(msg)

# Function to display flask logs
# RETURN: flask template
@app.route('/')
def display():
	with open('app.log', 'r') as log_file:
		logs = log_file.read()
		content = logs.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
	if not logs:
		return "No logs to display"
	return render_template_string(content)

# Get timestamp for logs
# RETURN: datetime obj
def current_time(): return datetime.now(pytz.timezone('Europe/Helsinki')).strftime('%D %H:%M:%S')

# Convert eur / MWh to snt / KWh and also add VAT 24%
# RETURN: snt / kwh
def calculate_actual_price(price): return ((price / 10) * 1.24) + electricity_transfer

# send_notification('<Your User Key>', '<Your API Token>', 'This is a test message')
# RETURN: None
def send_notification(message):
	payload = {
        'token': pushover_key,
        'user': pushover_user,
        'message': message,
	}
	ft_print(f"{current_time()}    " + message)
	try:
		req = requests.post(pushover_url, data=payload)
		req.raise_for_status()
		ft_print(f"{current_time()}    Notification sent")
	except requests.RequestException as err:
		error_msg = err.response.text if err.response else str(err)
		ft_print(f"{current_time()}    Notification failed {req.status_code}: {error_msg}")

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
				ft_print(f"{current_time()}    {start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}: {price}snt/kWh")

				return price

# Retrives current btc price
# RETURN: eur / btc
def get_btc_price():
	response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
	data = response.json()
	price = round(data['bpi']['EUR']['rate_float'], 2)
	ft_print(f"{current_time()}    btc price: {price}€/btc")
	
	return price

# Calculate last hours profitability to decide wheter next hour is worth it
# RETURN: snt / h
def get_profitability():
    last_hour = []
    start = datetime.now(pytz.timezone('Europe/Helsinki'))
    
    while start.minute != end_of_hour:
        start = datetime.now(pytz.timezone('Europe/Helsinki'))
        miner = nicehash_api.get_rigs()
        last_hour.append(miner['totalProfitability'])
        clock.sleep(60)
	
    bitcoin_price = get_btc_price()
    profitability = (((sum(last_hour) / len(last_hour)) * bitcoin_price) / 24)
    ft_print(f"{current_time()}    Profitability for next hour {round(profitability, 2)}€/h")
    
    return profitability

# work around for Render.com throttle for inactivity
# RETURN: None
def background_worker():
    while True:
        try:
            req = requests.get(render_url)
            req.raise_for_status()
        except requests.RequestException as err:
            send_notification(f"bg: keep alive request \U0000274C: {err}")
        clock.sleep(300)
        
# keep track of uptime and price
# RETURN: None
def uptime(profit):
    global daily_prices
    global daily_uptime
    now = datetime.now(pytz.timezone('Europe/Helsinki'))
    if (profit > threshold):
        daily_prices.append(profit)
        daily_uptime += 1
    if (now.hour == 0):
        save_daily(daily_prices)
        daily_uptime = 0
        daily_prices = []

# save daily statistics and display them on route 
# RETURN: None
def save_daily(prices):
    avg_price = sum(prices) / len(prices) if prices else 0
    msg = f"{datetime.now(pytz.timezone('Europe/Helsinki')).strftime('%D')} - Uptime: {len(prices)} hours, Average Price: {avg_price:.2f} snt/kWh\n"
    with open('daily_stats.txt', 'a') as file:
        file.write(msg)
    send_notification(msg)
    display_uptime()

# Display uptime statistics
# RETURN: route template
@app.route('/uptime')
def display_uptime():
	with open('daily_stats.txt', 'r') as file:
		stats = file.read()
		content = stats.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
	if not content:
		return "No stats to display"
	return render_template_string(content)

# mainloop
# RETURN: None
def main():
	running = True
	send_notification("Starting script...")
	while running == True:
		income = get_profitability()
		cost = (price_for_next_hour() / 100)
		profit = income - cost
		ft_print(f"{current_time()}    income: {round(income, 2)}€ - cost: {round(cost, 2)}€ = {round(profit, 2)}€/hour")
		uptime(profit)
		if (profit < threshold):	# price check failed
			send_notification(f"Price check: \U0000274C")
		else:						# price check succeeded
			ft_print(f"Price check: \U00002705")
		clock.sleep(61)
   
# start app in it's own thread
# RETURN: None
def start():
	main_thread = threading.Thread(target=main)
	background_thread = threading.Thread(target=background_worker)
	main_thread.start()
	background_thread.start()

# Define constants
pushover_url = 'https://api.pushover.net/1/messages.json'
render_url = 'https://spotprice.onrender.com'
nicehas_url = 'https://api2.nicehash.com'
finland = ['FI']
daily_prices = []
daily_uptime = 0
electricity_transfer = 4.69 + 2.79	# transfer + VAT
end_of_hour = 50					# minutes
threshold = 0.15					# eur / h


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
format = logging.Formatter('%(message)s')
logger = logging.getLogger('Logger')
log = logging.FileHandler('app.log')
log.setLevel(logging.DEBUG)
log.setFormatter(format)
logger.addHandler(log)
logger.setLevel(logging.DEBUG)

# running app based on if it's local developement or production
if __name__ == '__main__':
	ft_print("Running in developement...")
	start()
	app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)
else:
    ft_print("Running in production...")
    start()