import re
from glob import glob
from os import system

import aiml

import telegram
from telegram import Update, Bot

from IHbot import dispatcher
from IHbot.modules.disable import DisableAbleRegexHandler

# The Kernel object is the public interface to
# the AIML interpreter.
alice = aiml.Kernel()


# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
print("started learning")
print(system('ls /app/IHBot/'))
alice.learn("/app/IHBot/std-startup.xml")
alice.learn('/app/IHBot/aiml/botdata/standard/std-turing.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-hello.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-sales.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-dont.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/dev-scripts.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-errors.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-pickup.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-connect.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-religion.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-inventions.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-numbers.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/dev-webhelper.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-botmaster.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-yesno.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-profile.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-sports.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/dev-testcases.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-german.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-sextalk.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/dev-examples.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-gossip.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-politics.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-atomic.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-knowledge.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/per-drWallace.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-lizards.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-login.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-srai.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-robot.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-that.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-dictionary.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-inactivity.aiml')
# alice.learn('/app/IHBot/aiml/botdata/standard/dev-translation.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-disconnect.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-personality.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-geography.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-65percent.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-gender.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/dev-calendar.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-brain.aiml')
alice.learn('/app/IHBot/aiml/botdata/standard/std-suffixes.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/psychology.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/phone.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/sports.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/music.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/stack.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/mp5.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/wallace.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/science.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/computers.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/update_mccormick.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/reduction1.safe.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/reductions-update.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/mp3.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/sex.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/personality.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/reduction4.safe.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/movies.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/emotion.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/mp0.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/loebner10.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/bot_profile.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/astrology.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/inquiry.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/reduction0.safe.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/reduction2.safe.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/date.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/ai.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/numbers.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/money.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/primeminister.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/mp1.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/mp4.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/update1.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/history.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/reduction.names.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/reduction3.safe.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/gossip.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/bot.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/politics.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/that.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/mp2.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/mp6.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/atomic.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/client_profile.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/imponderables.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/stories.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/default.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/knowledge.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/drugs.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/xfind.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/pickup.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/biography.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/literature.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/client.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/humor.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/salutations.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/interjection.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/food.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/geography.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/continuation.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/alice.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/iu.aiml')
alice.learn('/app/IHBot/aiml/botdata/alice/religion.aiml')
# alice.respond('load aiml b')
print("finished learning")

def words_are_greeting(msg):
    return re.match("(how a?bout ?(cha|y?o?u)|hi[ $!.]|hello|fine,? (thanks|y?o?ur ?self)|what'?s? up|wh?addup|^yo[ $!.])", msg)

def converse(bot: Bot, update: Update):
    # # empty string errors -_-
    # if len(res.text) >= telegram.MAX_MESSAGE_LENGTH:
    #     update.effective_message.reply_text("I lost my train of thought...")
    # res = update.effective_message.reply_text()
    message = update.effective_message
    if message.reply_to_message or words_are_greeting(message):
        bot.sendChatAction(update.effective_chat.id, "typing")  # Bot typing before send messages
        try:
            message.reply_to_message.reply_text(alice.respond(update.effective_message.text, update.effective_user.name))
        except:
            pass

__help__ = """
 - Bot responds to certain messages conversationally
""".format(telegram.MAX_MESSAGE_LENGTH)

__mod_name__ = "Converse"


CONVERSE_HANDLER = DisableAbleRegexHandler(r'^[^sS/?!.].*', converse, friendly="converse", run_async=True)

dispatcher.add_handler(CONVERSE_HANDLER)

