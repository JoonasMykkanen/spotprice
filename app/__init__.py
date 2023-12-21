# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/17 17:30:32 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 16:08:35 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
from config import Config
from flask import Flask

from .utils.initExternalApi import initExternalAPI
from .tasks import hourlyRun

from .routes.test import testBP

def create_app():
	# Create flask application
	app = Flask(__name__)

	# Register all blueprints / routes
	app.register_blueprint(testBP, url_prefix='/test')

	# Get configuration --> .env variables & external api's
	app.config.from_object(Config)

	# Init external apis before first request
	initExternalAPI(app)

	# Creating scheduler for automated data retrieving from api's
	# scheduler = BackgroundScheduler()
	# scheduler.add_job(lambda: hourlyRun(app), 'interval', seconds=5)
	# scheduler.start()

	# Use cors to make react frontend able to connect
	CORS(app)

	return app