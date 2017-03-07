import re
import time

from slackbot.bot import respond_to

import plugins.pomodoro as pm
import task_manager as tm


@respond_to('pom ([a-z]*)', re.IGNORECASE)
def pom(message, arg1=None):
    if arg1 == 'start':
        pm.pom_start(message)
    elif arg1 == 'cancel':
        pm.pom_cancel(message)
    else:
        message.send('usage: pom [start/cancel]')


@respond_to('work (.*)', re.IGNORECASE)
def work(message, arg1=None):
    args = arg1.split(' ')
    if args[0] == 'add':
        if len(args) == 4:
            print("args: {},{},{}".format(args[1], args[2], args[3]))
            tm.add_work(args[1], args[2], args[3])
            message.send('Added work: {} {} {}'.format(args[1], args[2], args[3]))
        else:
            message.send('usage: work add [name] [category id] [(i|o|io|np)]')
    elif args[0] == 'show':
        for row in tm.show_work():
            if row[5] is not None:
                message.send('{} {} {} {} {} {}min'.format(row[0], row[1], row[2], row[3], row[6], (row[5]-row[4]) // 60))
            else:
                message.send('current: {} {} {} {} {} {}min'.format(row[0], row[1], row[2], row[3], row[6], (int(time.time()) - row[4]) // 60))
    elif args[0] == 'end':
        pass


@respond_to('category (.*)', re.IGNORECASE)
def category(message, arg1=None):
    args = arg1.split(' ')
    if args[0] == 'add':
        if len(args) == 2:
            tm.add_category(args[1])
            message.send('Added category: {}!'.format(args[1]))
        else:
            message.send('usage: category add [category name]')
    elif args[0] == 'show':
        message.send('id name')
        for row in tm.show_category():
            message.send('{} {}'.format(row[0], row[1]))
    elif args[0] == 'remove':
        pass
    else:
        message.send('usage: category (add|show|remove)')
