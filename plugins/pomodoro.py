import time
import threading


def pom_start(message):
    print("main: {}".format(threading.currentThread().getName()))
    pom = Pomodoro(25, 5, 5, message)
    pom.setName('Pomodoro')
    pom.start()


def pom_cancel(message):
    for th in threading.enumerate():
        if(th.getName() == 'Pomodoro'):
            th._stop()

class Pomodoro(threading.Thread):
    def __init__(self, worktime, breaktime, notify_freq, message):
        threading.Thread.__init__(self)
        self.worktime = worktime
        self.breaktime = breaktime
        self.notify_freq = notify_freq
        self.message = message
        self.stop = False

    def pmsend(self, message):
        if not self.stop:
            self.message.send(message)
            print("{} min has passed".format((i+1) * self.notify_freq))

    def run(self):
        self.stop = False
        self.pmsend('Pomodoro start!')
        for i in range(self.worktime // self.notify_freq):
            time.sleep(6 * self.notify_freq)
            self.pmsend('{} min'.format((i+1) * self.notify_freq))
        self.pmsend('Break start!')
        for i in range(self.breaktime // self.notify_freq):
            time.sleep(60 * self.notify_freq)
            self.pmsend('{} min'.format((i+1) * self.notify_freq))
        if not self.stop:
            pom = Pomodoro(self.worktime, self.breaktime, self.notify_freq, self.message)
            pom.setName('Pomodoro')
            pom.start()

    def _stop(self):
        self.message.send('pomodoro cannceled!')
        self.stop = True
