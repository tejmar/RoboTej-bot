from random import randint, randrange

from telegram import Update, Bot
from telegram.ext import run_async

from IHbot import dispatcher
from IHbot.modules.disable import DisableAbleCommandHandler


@run_async
def rollDice(bot: Bot, update: Update, args):
    text = ""
    dice_number = 0
    lower = 1

    try:
        dice_number = int(args[0])
    except ValueError:
        nums = args[0].split("d")
        if len(nums) == 2:
            try:
                lower = int(nums[0])
                dice_number = int(nums[0]) * int(nums[1])
            except ValueError:
                dice_number = 0
        else:
            dice_number = 0
    except IndexError:
        dice_number = 0

    if dice_number:
        result = randint(lower, dice_number)
        text = "You rolled " + str(result)
    else:

        text = str(randrange(10 ** 8, 10 ** 9))  # generate the roll

        # roll_list = []
        # for i in text:  # basically this whole chunk detects if there are dubs trips etc
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
        update.effective_message.reply_text(text)

        # here, congratulate for quads etc, if we implment the other part of what jan does ;-)
    except:
        pass


__help__ = """
 - /roll [number]: roll a die with [number] sides and return the result.
"""

__mod_name__ = "Roll"

ROLL_HANDLER = DisableAbleCommandHandler("roll", rollDice, pass_args=True)

dispatcher.add_handler(ROLL_HANDLER)
