# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 09:22:36 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 15:22:49 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from dotenv import load_dotenv
load_dotenv()
from app import create_app

app = create_app()

if __name__ == '__main__':
	app.run()	