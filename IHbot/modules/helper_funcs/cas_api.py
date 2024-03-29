# # DON'T BE A DICK PUBLIC LICENSE B
#
# > Version 1.1, October 2020
#
# > Copyright (C) 2020 Nuno Penim
#
#  Everyone is permitted to copy and distribute verbatim or modified
#  copies (as long as the name changes) of this license document.
#
# > DON'T BE A DICK PUBLIC LICENSE B
# > TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  1. Do whatever you like with the original work, just don't be a dick.
#
#      Being a dick includes - but is not limited to - the following instances:
#
# 1a. Outright copyright infringement - Don't just copy the original work/works and change the name. 1b. Selling the
# unmodified original with no work done what-so-ever, that's REALLY being a dick. 1c. Modifying the original work to
# contain hidden harmful content. That would make you a PROPER dick. 1d. Selling a project with educational purposes
# without consulting the original creator. That would make you a BAG of dicks.
#
#  2. If you become rich through modifications, related works/services, or supporting the original work,
#  share the love. Only a dick would make loads off this work and not buy the original work's
#  creator(s) a beer or a pizza.
#
# 3. Code is provided with no warranty. Using somebody else's code and bitching when it goes wrong makes you a DONKEY
# dick. Fix the problem yourself or submit a [bug report](https://www.chiark.greenend.org.uk/~sgtatham/bugs.html),
# so that the original creator can attempt to fix the problem. Just don't bitch about it.

# https://github.com/nunopenim/pyCombotCAS_API

import datetime
import json

import requests

VERSION = "1.4.0"
CAS_QUERY_URL = "https://api.cas.chat/check?user_id="
DL_DIR = "./csvExports"


def get_user_data(user_id):
    with requests.request('GET', CAS_QUERY_URL + str(user_id)) as userdata_raw:
        userdata = json.loads(userdata_raw.text)
        return userdata


def isbanned(userdata):
    return userdata['ok']


def banchecker(userdata):
    return isbanned(userdata)


def vercheck() -> str:
    return str(VERSION)


def offenses(userdata):
    try:
        offenses = userdata['result']['offenses']
        return str(offenses)
    except:
        return None


def timeadded(userdata):
    try:
        timeEp = userdata['result']['time_added']
        timeHuman = datetime.datetime.utcfromtimestamp(timeEp).strftime('%H:%M:%S, %d-%m-%Y')
        return timeHuman
    except:
        return None
