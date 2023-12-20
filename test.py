# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 15:59:16 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 16:04:01 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import timedelta
from datetime import datetime
from nordpool import elspot
import pytz



for index in range(0, 50):
	finlandTZ = pytz.timezone('Europe/Helsinki')
	currentDate = datetime.now(finlandTZ).date() + timedelta(hours=index)
	next = datetime.now(pytz.timezone('Europe/Helsinki')) + timedelta(hours=index+1)
	print(f'date: {currentDate} next hour: {next}')
	index += 1