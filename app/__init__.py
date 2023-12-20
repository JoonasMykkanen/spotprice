# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/17 17:30:32 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/20 14:32:36 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# General imports for app to work
from flask_cors import CORS
from config import Config
from flask import Flask

from apscheduler.schedulers.background import BackgroundScheduler
from .utils.initExternalApi import initExternalAPI
from .tasks import updateDatabases
from .db import db

def create_app():
	# Create flask application
	app = Flask(__name__)

	# Get configuration --> .env variables & external api's
	app.config.from_object(Config)
	initExternalAPI(app)

	# init database
	# db.init(app)

	# Creating scheduler for automated data retrieving from api's
	scheduler = BackgroundScheduler()
	scheduler.add_job(lambda: updateDatabases(app), 'interval', seconds=5)
	scheduler.start()

	# Use cors to make react frontend able to connect
	CORS(app)

	return app