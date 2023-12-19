# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/17 17:30:32 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 10:37:47 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# General imports for app to work
from flask_cors import CORS
from config import Config
from flask import Flask

from .utils.initExternalApi import initExternalAPI

def create_app():
	# Create flask application
	app = Flask(__name__)

	# Get configuration --> .env variables & external api's
	app.config.from_object(Config)
	initExternalAPI(app)

	# Use cors to make react frontend able to connect
	CORS(app)

	return app