# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/21 15:28:03 by jmykkane          #+#    #+#              #
#    Updated: 2023/12/21 15:59:51 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# includes test route to testout anything
from flask import Blueprint

from ..services.databaseService import *

testBP = Blueprint('test', __name__)

@testBP.route('/')
def root():
	return getBtcPrice()