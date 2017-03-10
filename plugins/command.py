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


def work_add(message, args):
    if args[0] == 'add':
        if len(args) == 4:
            print("args: {},{},{}".format(args[1], args[2], args[3]))
            tm.add_work(args[1], args[2], args[3])
            message.send('Added work: {} {} {}'.format(args[1], args[2], args[3]))
        else:
            message.send('usage: work add [name] [category id] [(i|o|io|np)]')


def work_show(message, args):
    row_num = 5
    works = tm.show_work()
    if len(args) > 1:
        row_num = min(int(args[1]), len(works))
    for row in works[-row_num:]:
        if row[5] is not None:
            message.send('{} {} {} {} {} {}min'.format(row[0], row[1], row[3], row[2], row[6], (row[5]-row[4]) // 60))
        else:
            message.send('current: {} {} {} {} {} {}min'.format(row[0], row[1], row[3], row[2], row[6], (int(time.time()) - row[4]) // 60))


def work_edit(message, args):
    if len(args) == 4 and args[2] in ['name', 'categoryid', 'worktype', 'duration']:
        tm.edit_work(args[1], args[2], args[3])
        message.send('Edited work: {} to {}'.format(args[2], args[3]))
    else:
        message.send('usage: work edit [starttime] [(name|categoryid|worktype|duration)] [value]')

def work_insert(message, args):
    if len(args) == 7:
        tm.insert_work(args[1], args[2], args[3], args[4], args[5], args[6])
        message.send('Inserted work: {} {} {}'.format(args[4], args[5], args[6]))
    else:
        message.send('usage: work insert [basetime] [difftime] [endtime] [name] [categoryid] [(i|o|io|np)]')


@respond_to('work (.*)', re.IGNORECASE)
def work(message, arg1=None):
    args = arg1.split(' ')
    commands = {
        'add':work_add,
        'show':work_show,
        'edit':work_edit,
        'insert':work_insert,
    }
    if args[0] in commands:
        commands[args[0]](message,args)
    else:
        message.send('usage: work (add|show|end|edit|insert)')

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
