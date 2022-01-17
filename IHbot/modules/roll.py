
import telegram
from random import randint, randrange
from telegram import Update, Bot
from telegram.ext import MessageHandler, Filters, run_async

from IHbot import dispatcher
from IHbot.modules.disable import DisableAbleCommandHandler


@run_async
def rollDice(bot: Bot, update: Update):
    text = ""
    dice_number = 0

    try:
        dice_number = int(update.effective_message.text[5:])
    except ValueError:
        dice_number = 0

    if dice_number:
        result = randint(1, dice_number)
        text = "You rolled " + str(result)
    else:
        # roll_list = []

        # roll = [below]
        text = str(randrange(10 ** 8, 10 ** 9))  # generate the roll

        message.reply_text(roll)

        # for i in roll:  # basically this whole chunk detects if there are dubs trips etc
        #     roll_list.append(i)
        # counter = 0
        # for i in range(0, 8):
        #     if roll_list[i] == roll_list[i + 1]:
        #         counter += 1
        #     else:
        #         counter = 0
    try:
        # Perhaps we can use tg die emoji thing for D6.
        # Then again, you could do that without the bot. So perhaps not.
        message.reply_text(text)

        # here, congratulate for quads etc, if we implment the other part of what jan does ;-)
    except:
        pass


__help__ = """
 - /roll [number]: roll a die with [number] sides and return the result.
"""

__mod_name__ = "Roll"

ROLL_HANDLER = DisableAbleCommandHandler("roll", rollDice)

dispatcher.add_handler(ROLL_HANDLER)
