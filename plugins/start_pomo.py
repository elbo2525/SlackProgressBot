import time
import subprocess
import threading

from slackbot.bot import respond_to

class Pomodoro(threading.Thread):
    def __init__(self, worktime, breaktime, notify_freq, message):
        threading.Thread.__init__(self)
        self.worktime = worktime
        self.breaktime = breaktime
        self.notify_freq = notify_freq
        self.message = message
        self.stop = False

    def run(self):
        self.stop = False
        self.message.send('Pomodoro start!')
        for i in range(self.worktime // self.notify_freq):
            time.sleep(60 * self.notify_freq)
            self.message.send('{} min'.format((i+1) * self.notify_freq))
            print("{} min has passed".format((i+1) * self.notify_freq))
        self.message.send('Break start!')
        for i in range(self.breaktime // self.notify_freq):
            time.sleep(60 * self.notify_freq)
            self.message.send('{} min'.format((i+1) * self.notify_freq))
            print("{} min has passed".format((i+1) * self.notify_freq))
        if not self.stop:
            pom = Pomodoro(self.worktime, self.breaktime, self.notify_freq, self.message)
            pom.setName('Pomodoro')
            pom.start()

    def _stop(self):
        self.stop = True


@respond_to('pomstart')
def pomtest(message):
    print("main: {}".format(threading.currentThread().getName()))
    pom = Pomodoro(25, 5, 5, message)
    pom.setName('Pomodoro')
    pom.start()


@respond_to('pomcancel')
def pomcancel(message):
    for th in threading.enumerate():
        if(th.getName() == 'Pomodoro'):
            th._stop()
