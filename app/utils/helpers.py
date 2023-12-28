# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    helpers.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 14:38:49 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/27 11:33:36 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import datetime

# will return datetime object in a format of = YYYY-MM-DDTHH
def getTimeStamp():
	return datetime.now().strftime('%Y-%m-%dT%H')

def parseTimestamp(timestamp_str):
    return datetime.strptime(timestamp_str, '%Y-%m-%dT%H')



	