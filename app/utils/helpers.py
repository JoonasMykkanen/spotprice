# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    helpers.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 14:38:49 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/19 16:38:15 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import datetime

# will return datetime object in a format of = YYYY-MM-DDTHH
def getTimeStamp():
	return datetime.now().strftime('%Y-%m-%dT%H')