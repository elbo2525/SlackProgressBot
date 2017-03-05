import re

from slackbot.bot import respond_to

import plugins.pomodoro as pm

@respond_to('pom$', re.IGNORECASE)
@respond_to('pom (.*)', re.IGNORECASE)
def pom(message, arg1=None):
    if arg1 == 'start':
        pm.pom_start(message)
    elif arg1 == 'cancel':
        pm.pom_cancel(message)
    else:
        message.send('usage: pom [start/cancel]')
