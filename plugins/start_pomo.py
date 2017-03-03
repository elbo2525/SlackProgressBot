from slackbot.bot import respond_to

@respond_to('pom')
def pom(message):
    message.reply('test')

@respond_to('pom start')
def pom(message):
    print("message: {}".format(message))
    message.reply('test pom')
