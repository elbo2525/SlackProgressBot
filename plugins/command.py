import re

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


@respond_to('task (.*)', re.IGNORECASE)
def task(message, arg1=None):
    args = arg1.split(' ')
    if args[0] == 'add':
        if len(args) == 3:
            print("arg1: {}, arg2: {}".format(args[1], args[2]))
            tm.add_task(args[1], args[2])
            message.send('Added task: {} {}'.format(args[1], args[2]))
        else:
            message.send('usage: task add [name] [category_id]')
    elif args[0] == 'show':
        message.send('id name categoryid')
        for row in tm.show_task():
            message.send('{} {} {}'.format(row[0], row[1], row[2]))
    elif args[0] == 'remove':
        pass
    else:
        message.send('usage: task (add|show|remove)')


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
