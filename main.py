from flask import Flask, render_template_string
from datetime import datetime, timedelta
from dotenv import load_dotenv
from nordpool import elspot
import time as clock
import threading
import tinytuya
import requests
import nicehash
import logging
import pytz
import os

class Socket:
	def __init__ (self, api_key, api_secret, device_name, socket_id):
		self.secret = api_secret
		self.name = device_name
		self.id = socket_id
		self.key = api_key
		self.status = self._init_mode()
		self.status_update()
  
	def _init_mode(self):
		try:
			tuya_api.sendcommand(self.name, turn_off)
			socket_logger.info(f"Created socket_{self.id}")
			return False
		except Exception:
			send_notification(f"Error turning off socket_{self.id}")
			exit()
   
	def switch(self):
		new_status = not self.status
		payload = { "commands": [{"code": "switch_1", "value": new_status},{"code": "countdown_1", "value": 0},] }
		try:
			tuya_api.sendcommand(self.name, payload)
			socket_logger.info(f"Switched socket_{self.id} mode to: {new_status}")
			self.status = new_status
		except Exception:
			send_notification(f"Error switching socket_{self.id} mode")
			exit()
   
	def status_update(self):
		try:
			res = tuya_api.getstatus(self.name)
			status = res['result'][0]['value']
			self.status = status
		except Exception:
			send_notification(f"Error checking socket_{self.id} status")
			exit()
#	____END_CLASS____

app = Flask(__name__)

# Loop trough all switches and turn on or off
# RETURN: None
def loop_rig_switches(target):
	global rig_mode
	global sockets

	for device in sockets:
		device.status_update()
		if (device.status != target):
			device.switch()
			send_notification(f"Socket_{device.id} switched to: {device.status}")
	rig_mode = target

# Custom print function to also store logs in flask
# RETURN: None
def ft_print(msg):
    price_logger.info(msg)
    print(msg)

# Function to display flask logs
# RETURN: flask template
@app.route('/')
def display():
	with open(data_log_path, 'r') as log_file:
		logs = log_file.read()
		content = logs.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
	if not logs:
		return "No logs to display"
	return render_template_string(content)

# function to display 
# RETURN: flask template
@app.route('/socket')
def display_socket_log():
	with open(socket_log_path, 'r') as log_file:
		logs = log_file.read()
		content = logs.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
	if not logs:
		return "No logs to display"
	return render_template_string(content)
  

# Get timestamp for logs
# RETURN: datetime obj
def current_time(): return datetime.now(pytz.timezone('Europe/Helsinki')).strftime('%D %H:%M:%S')

# Convert eur / MWh to snt / KWh and also add VAT 24% also add transfer costs
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
	global	rig_mode
	global last_hour
    
	start = datetime.now(pytz.timezone('Europe/Helsinki'))
	while start.minute != end_of_hour:
		start = datetime.now(pytz.timezone('Europe/Helsinki'))
		miner = nicehash_api.get_rigs()
		if (rig_mode == True):
			last_hour.append(miner['totalProfitability'])
		clock.sleep(60)
	
	bitcoin_price = get_btc_price()
	if (len(last_hour) > 0):
		profitability = (((sum(last_hour) / len(last_hour)) * bitcoin_price) / 24)
	else:
		profitability = 0
	ft_print(f"{current_time()}    Profitability for next hour {round(profitability, 2)}€/h")
	if (rig_mode == True):
		last_hour = []
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
    uptime_logger.info(msg)
    display_uptime()

# Display uptime statistics
# RETURN: route template
@app.route('/uptime')
def display_uptime():
	with app.app_context():
		with open(uptime_log_path, 'r') as file:
			stats = file.read()
			content = stats.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
		if not content:
			return "No stats to display"
		return render_template_string(content)

# waits until start of next hour
# RETURN: None
def wait_until_start():
	now = datetime.now(pytz.timezone('Europe/Helsinki'))
	while (now.minute != 0):
		now = datetime.now(pytz.timezone('Europe/Helsinki'))
		clock.sleep(60)

# Based on previous rig status, send notification or print log
# RETURN: None
def check_success():
	global rig_mode

	if (rig_mode == False):
		send_notification(f"Price check: \U00002705")
	else:
		ft_print(f"Price check: \U00002705")
	wait_until_start()
	loop_rig_switches(True)
	
# Based on previous rig status, send notification or print log
# RETURN: None
def check_failure():
	global rig_mode

	if (rig_mode == True):
		send_notification(f"Price check: \U0000274C")
	else:
		ft_print(f"Price check: \U0000274C")
	loop_rig_switches(False)

# mainloop
# RETURN: None
def main():
	running = True
	send_notification("Starting script")
	while running == True:
		income = get_profitability()
		cost = (price_for_next_hour() / 100)
		profit = income - cost
		ft_print(f"{current_time()}    income: {round(income, 2)}€ - cost: {round(cost, 2)}€ = {round(profit, 2)}€/hour")
		uptime(profit)
		if (profit < threshold):
			check_failure()
		else:
			check_success()
		clock.sleep(61)
   
# start app in it's own thread
# RETURN: None
def start():
	main_thread = threading.Thread(target=main)
	background_thread = threading.Thread(target=background_worker)
	main_thread.start()
	background_thread.start()

# Define constants
turn_off = { "commands": [{"code": "switch_1", "value": False},{"code": "countdown_1", "value": 0},] }
turn_on = { "commands": [{"code": "switch_1", "value": True},{"code": "countdown_1", "value": 0},] }
pushover_url = 'https://api.pushover.net/1/messages.json'
render_url = 'https://spotprice.onrender.com'
nicehas_url = 'https://api2.nicehash.com'
socket_log_path = 'logs/socket.log'
uptime_log_path = 'logs/uptime.log'
data_log_path = 'logs/data.log'
daily_prices = []
finland = ['FI']
daily_uptime = 0
electricity_transfer = 6.56			# transfer snt / kWh
end_of_hour = 45					# minutes
threshold = 0.15					# eur / h
rig_mode = True
last_hour = []
sockets = []

# getting env variables
load_dotenv()
nicehash_secret = os.getenv("NICEHASH_SECRET")
nicehash_key = os.getenv("NICEHASH_API_KEY")
nicehash_id = os.getenv("NICEHASH_ID")
pushover_key = os.getenv("PUSHOVER_API_KEY")
pushover_user = os.getenv("PUSHOVER_USER")
tuya_secret = os.getenv("TUYA_SECRET")
tuya_key = os.getenv("TUYA_KEY")
garage_0 = os.getenv("G0_ID")
garage_1 = os.getenv("G1_ID")

# init apis
nicehash_api = nicehash.private_api(nicehas_url, nicehash_id, nicehash_key, nicehash_secret)
nordpool_api = elspot.Prices(currency='EUR')
tuya_api = tinytuya.Cloud(
    apiRegion='eu',
	apiKey=tuya_key,
	apiSecret=tuya_secret,
	apiDeviceID=garage_0
)

# General logging
log_format = logging.Formatter('%(message)s')
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# init price logging
price_logger = logging.getLogger('Price_logger')
price_log = logging.FileHandler(data_log_path)
price_log.setLevel(logging.DEBUG)
price_log.setFormatter(log_format)
price_logger.addHandler(price_log)
price_logger.setLevel(logging.DEBUG)

# init socket logging
socket_logger = logging.getLogger('Socket_logger')
socket_log = logging.FileHandler(socket_log_path)
socket_log.setLevel(logging.DEBUG)
socket_log.setFormatter(log_format)
socket_logger.addHandler(socket_log)
socket_logger.setLevel(logging.DEBUG)

# init uptime logging
uptime_logger = logging.getLogger('Uptime_Logger')
uptime_log = logging.FileHandler(uptime_log_path)
uptime_log.setLevel(logging.DEBUG)
uptime_log.setFormatter(log_format)
uptime_logger.addHandler(uptime_log)
uptime_logger.setLevel(logging.DEBUG)

sockets.append(Socket(tuya_key, tuya_secret, garage_0, 0))
sockets.append(Socket(tuya_key, tuya_secret, garage_1, 1))

# running app based on if it's local developement or production
if __name__ == '__main__':
	ft_print("Running in developement...")
	start()
	app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)
else:
    ft_print("Running in production...")
    start()