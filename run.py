# -*- coding: utf-8 -*-
from slackbot.bot import Bot

import task_manager
import settings

def main():
    task_manager.start(settings.SQLITE)

    bot = Bot()
    bot.run()

if __name__ == '__main__':
    main()
