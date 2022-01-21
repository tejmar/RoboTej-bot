from telegram import User

from IHbot import dispatcher
from IHbot.modules.disable import DisableAbleCommandHandler

characterList = []
playerIndex = 0
DM = User

attributes = False

# This module has a lot of issues I'd like to fix before pushing it into a production bot.
# I'm committing in an unsatisfactory spot so that I can catch any glaring derps before I start hacking it up.
# What I would like to investigate:
# 1. Starting or stopping a dungeon/game
# 2. Isolating a game to one particular chat
# 3. Persistence through "reboot"s
# 4. Identifying DMs/players by ID, not by name
# 5. Using command args where possible (not making assumptions about boundaries in strings etc)
# 6. DM is set *by anyone* to calling user (and can't be changed)
# 7. All commands produce un-graceful crashes when presented without input (except setdm and addcharacter)
# 8. Addcharacter doesn't might execute in wrong order or properly init character

# First I get everything working the way I want (args, syntax, business logic)
# The last step will be to use db and other stuff to solve problems 2 and 3.
# I think that'll be easier to test once the gist of everything mostly works.


class Character(object):
    playerName = None
    characterName = None
    race = None
    _class = None
    inventory = {}
    stats = {'strength': 0, 'dexterity': 0, 'wisdom': 0, "intelligence": 0, "constitution": 0, "charisma": 0,
             "health": 0}

    def __init__(self, player_name, character_name):
        self.playerName = player_name
        self.characterName = character_name.lower()

    def updateStats(self, race, _class):
        self.race = race
        self._class = _class

        # down here, why does it say like "if constitution x then health y"?
        # what if it doesn't? i don't understand the point of the conditional
        # i mean, it can't be false... ? ...

        # Race Stats for Human
        if self.race == 'human':
            self.stats['strength'] = 5
            self.stats['dexterity'] = 5
            self.stats['wisdom'] = 5
            self.stats['intelligence'] = 5
            self.stats['constitution'] = 5
            self.stats['charisma'] = 5
            if self.stats['constitution'] == 5:
                self.stats['health'] = 18
        # Race Stats for Dwarf
        elif self.race == 'dwarf':
            self.stats['strength'] = 6
            self.stats['dexterity'] = 3
            self.stats['wisdom'] = 3
            self.stats['intelligence'] = 3
            self.stats['constitution'] = 7
            self.stats['charisma'] = 3
            if self.stats['constitution'] == 7:
                self.stats['health'] = 20
        # Race Stats for Elf
        elif self.race == 'elf':
            self.stats['strength'] = 3
            self.stats['dexterity'] = 3
            self.stats['wisdom'] = 8
            self.stats['intelligence'] = 7
            self.stats['constitution'] = 3
            self.stats['charisma'] = 6
            if self.stats['constitution'] == 3:
                self.stats['health'] = 16
        # Race Stats for Ogre
        elif self.race == 'ogre':
            self.stats['strength'] = 10
            self.stats['dexterity'] = 3
            self.stats['wisdom'] = 3
            self.stats['intelligence'] = 3
            self.stats['constitution'] = 8
            self.stats['charisma'] = 3
            if self.stats['constitution'] == 8:
                self.stats['health'] = 21
        # Race Stats for Merman
        elif self.race == 'merman':
            self.stats['strength'] = 7
            self.stats['dexterity'] = 5
            self.stats['wisdom'] = 6
            self.stats['intelligence'] = 5
            self.stats['constitution'] = 4
            self.stats['charisma'] = 3
            if self.stats['constitution'] == 4:
                self.stats['health'] = 17

        # Class Stats for Fighter
        if self._class == 'fighter':
            self.stats['strength'] = self.stats['strength'] + 2
            self.stats['dexterity'] = self.stats['dexterity']
            self.stats['wisdom'] = self.stats['wisdom'] - 1
            self.stats['intelligence'] = self.stats['intelligence'] - 2
            self.stats['constitution'] = self.stats['constitution'] + 2
            self.stats['charisma'] = self.stats['charisma'] - 1
            self.stats['gold'] = 50
            self.stats['experience'] = 0
        # Class Stats for Mage
        elif self._class == 'mage':
            self.stats['strength'] = self.stats['strength'] - 2
            self.stats['dexterity'] = self.stats['dexterity']
            self.stats['wisdom'] = self.stats['wisdom'] + 2
            self.stats['intelligence'] = self.stats['intelligence'] + 2
            self.stats['constitution'] = self.stats['constitution'] - 1
            self.stats['charisma'] = self.stats['charisma'] - 1
            self.stats['gold'] = 100
        # Class Stats for Priest
        elif self._class == 'priest':
            self.stats['strength'] = self.stats['strength'] - 2
            self.stats['dexterity'] = self.stats['dexterity']
            self.stats['wisdom'] = self.stats['wisdom'] + 3
            self.stats['intelligence'] = self.stats['intelligence'] + 1
            self.stats['constitution'] = self.stats['constitution'] - 1
            self.stats['charisma'] = self.stats['charisma'] - 1
            self.stats['gold'] = 250
            self.stats['experience'] = 0
        # Class Stats for Thief
        elif self._class == 'thief':
            self.stats['strength'] = self.stats['strength'] - 1
            self.stats['dexterity'] = self.stats['dexterity'] + 2
            self.stats['wisdom'] = self.stats['wisdom'] - 2
            self.stats['intelligence'] = self.stats['intelligence']
            self.stats['constitution'] = self.stats['constitution'] - 1
            self.stats['charisma'] = self.stats['charisma'] + 2
            self.stats['gold'] = 200
            self.stats['experience'] = 0
        # Class Stats for Ranger
        elif self._class == 'ranger':
            self.stats['strength'] = self.stats['strength'] - 1
            self.stats['dexterity'] = self.stats['dexterity'] + 3
            self.stats['wisdom'] = self.stats['wisdom'] - 1
            self.stats['intelligence'] = self.stats['intelligence']
            self.stats['constitution'] = self.stats['constitution'] - 2
            self.stats['charisma'] = self.stats['charisma'] + 1
            self.stats['gold'] = 200
            self.stats['experience'] = 0


def setDM(bot, update, args):
    global DM
    if DM is None:
        DM = update.message.from_user
        update.effective_message.reply_text(DM + " has been set as Dungeon Master")
    else:
        update.effective_message.reply_text("DM " + DM.first_name + " has already been set!")


def createCharacter(bot, update, args):
    global playerIndex
    if findCharacterIndex(update.message.from_user.first_name) != -1:
        update.effective_message.reply_text("@" + update.message.from_user.first_name + " already has a character")
        return None
    character_name = args[0]
    race = args[1]
    _class = args[2]
    player_name = update.message.from_user.first_name
    ch = Character(player_name, character_name)
    ch.updateStats(race, _class)
    characterList.append(ch)
    # Displays "Character [Character] has been created [Player]"
    update.effective_message.reply_text("Character " + character_name + "has been created  by " + player_name)
    playerIndex += 1
    # Displays "@[Player] Please enter your character's attributes in the format of [Race] [Class]"
    update.effective_message.reply_text("@" + player_name + "Please enter your character's Race & Class in the "
                                                            "format: [Name] [Race] [Class]")
    global attributes
    attributes = True


# def incomingMessages(bot, update, args):
#     global attributes
#     if attributes:
#         attributes_input = update.message.text.lower()
#         attributes_input = attributes_input.split()
#         i = findCharacterIndex(update.message.from_user.first_name)
#         characterList[i].race = attributes_input[0]
#         characterList[i]._class = attributes_input[1]
#         # Display "@[Player] [Character]'s race is [Race] and [Character]'s class is [Class]
#         bot.sendMessage(chat_id=update.message.chat_id,
#                         text="@" + characterList[i].playerName + " " + characterList[i].characterName + "'s race is " +
#                              characterList[i].race + " and " + characterList[i].characterName + "'s class is " +
#                              characterList[i]._class + ".")
#         characterList[i].updateStats(characterList[i].race, characterList[i]._class)
#         statsheet = (str(characterList[i].characterName) + "\n Created by: "
#                      + str(characterList[i].playerName)
#                      + "\n ----------------------------"
#                      + "\n Strength: " + str(characterList[i].stats['strength'])
#                      + "\n Dexterity: " + str(characterList[i].stats['dexterity'])
#                      + "\n Wisdom: " + str(characterList[i].stats['wisdom'])
#                      + "\n Intelligence: " + str(characterList[i].stats['intelligence'])
#                      + "\n Constitution: " + str(characterList[i].stats['constitution'])
#                      + "\n Charisma: " + str(characterList[i].stats['charisma'])
#                      + "\n ----------------------------"
#                      + "\n Health: " + str(characterList[i].stats['health'])
#                      + "\n Gold: " + str(characterList[i].stats['gold'])
#                      + "\n Experience: " + str(characterList[i].stats['experience']))
#         update.effective_message.reply_text(statsheet)
#         attributes = False


def printCharacterStats(bot, update, args):
    # /printcharacterstats CHARACTER_NAME
    user_input = parseInput(update.message.text, 2)
    i = getIndexFromCharacter(user_input[1])
    statsheet = (str(characterList[i].characterName) + "\n Created by: "
                 + str(characterList[i].playerName)
                 + "\n ----------------------------"
                 + "\n Strength: " + str(characterList[i].stats['strength'])
                 + "\n Dexterity: " + str(characterList[i].stats['dexterity'])
                 + "\n Wisdom: " + str(characterList[i].stats['wisdom'])
                 + "\n Intelligence: " + str(characterList[i].stats['intelligence'])
                 + "\n Constitution: " + str(characterList[i].stats['constitution'])
                 + "\n Charisma: " + str(characterList[i].stats['charisma'])
                 + "\n ----------------------------"
                 + "\n Health: " + str(characterList[i].stats['health'])
                 + "\n Gold: " + str(characterList[i].stats['gold'])
                 + "\n Experience: " + str(characterList[i].stats['experience']))
    update.effective_message.reply_text(statsheet)


def findCharacterIndex(first_name):
    for i in range(len(characterList)):
        if characterList[i].playerName == first_name:
            return i
    return -1


def alterHealth(bot, update, args):
    # /changehealth charactername value
    user = update.message.from_user
    if DM and user.id != DM.id:
        update.effective_message.reply_text("You're not authorised to use this command!")
    else:
        user_input = parseInput(update.message.text, 3)
        i = getIndexFromCharacter(user_input[1])
        value = int(user_input[2])
        characterList[i].stats['health'] += value
        update.effective_message.reply_text(characterList[i].characterName + "'s health has been changed " + user_input[
            2] + " to " + str(characterList[i].stats['health']))


def inventoryUpdate(bot, update, args):
    user = update.message.from_user
    if DM and user.id != DM.id:
        update.effective_message.reply_text("You're not authorised to use this command!")
    else:
        inventory_input = parseInput(update.message.text, 5)
        i = getIndexFromCharacter(inventory_input[1])
        print(inventory_input[1] + characterList[i].playerName)
        if inventory_input[2] == "remove":
            if inventory_input[3] not in characterList[i].inventory:
                update.effective_message.reply_text("@" + characterList[i].playerName + "You don't have %s in your "
                                                                                        "inventory!" % (
                                                        inventory_input[3]))
            elif inventory_input[3] in characterList[i].inventory:
                if int(inventory_input[4]) > characterList[i].inventory[inventory_input[3]]:
                    update.effective_message.reply_text("@" + characterList[i].playerName + " You don't have enough " +
                                                        inventory_input[3] + "!")
                elif int(inventory_input[4]) == characterList[i].inventory[inventory_input[3]]:
                    del characterList[i].inventory[inventory_input[3]]
                elif int(inventory_input[4]) < characterList[i].inventory[inventory_input[3]]:
                    characterList[i].inventory[inventory_input[3]] = characterList[i].inventory[
                                                                         inventory_input[3]] - int(
                        inventory_input[4])
        elif inventory_input[2] == "add":
            if inventory_input[3] not in characterList[i].inventory:
                characterList[i].inventory[inventory_input[3]] = int(inventory_input[4])
            elif inventory_input[3] in characterList[i].inventory:
                characterList[i].inventory[inventory_input[3]] = characterList[i].inventory[inventory_input[3]] + int(
                    inventory_input[4])
        print(characterList[i].inventory)
        items = characterList[i].inventory.items()
        text = characterList[i].characterName + "'s Inventory \n"
        for item in items:
            text += item[0] + ": " + str(item[1]) + "\n"
        update.effective_message.reply_text(text)


def printInventory(bot, update, args):
    inventory_input = update.message.text
    inventory_input = inventory_input.split()
    name = inventory_input[1]
    i = getIndexFromCharacter(name)
    items = characterList[i].inventory.items()
    text = characterList[i].characterName + "'s Inventory \n"
    for item in items:
        text += item[0] + ": " + str(item[1]) + "\n"
    update.effective_message.reply_text(text)


def alterGold(bot, update, args):
    # /changehealth charactername value
    user = update.message.from_user
    if DM and user.id != DM.id:
        update.effective_message.reply_text("You're not authorised to use this command!")
    else:
        user_input = parseInput(update.message.text, 3)
        character_name = user_input[1]
        value = int(user_input[2])
        i = getIndexFromCharacter(character_name)
        characterList[i].stats['gold'] += value
        update.effective_message.reply_text(characterList[i].characterName + "'s gold has been changed by" + user_input[
            2] + " to " + str(characterList[i].stats['gold']))


def alterExperience(bot, update, args):
    # /changeXP character_name value
    user = update.message.from_user
    if DM and user.id != DM.id:
        update.effective_message.reply_text("You're not authorised to use this command!")
    else:
        user_input = parseInput(update.message.text, 3)
        character_name = user_input[1]
        value = int(user_input[2])
        i = getIndexFromCharacter(character_name)
        characterList[i].stats['experience'] += value
        update.effective_message.reply_text(characterList[i].characterName + "'s XP has been changed by" + user_input[
            2] + " to " + str(characterList[i].stats['experience']))


def parseInput(words, no):
    words = words.split()
    a = len(words) - no
    oup = words[1]
    for i in range(2, 2 + a):
        oup += words[i]
    out = [words[0].lower(), oup.lower()]
    for i in range(2, no):
        out.append(words[a + i].lower())
    return out


def getIndexFromCharacter(name):
    for i in range(len(characterList)):
        if characterList[i].characterName == name:
            return i


__help__ = """
 - /roll [number]: roll a die with [number] sides and return the result.
"""

__mod_name__ = "DnDMain"

SETDM_HANDLER = DisableAbleCommandHandler("setdm", setDM, pass_args=True)
CHANGEHEALTH_HANDLER = DisableAbleCommandHandler("changehealth", alterHealth, pass_args=True)
CHANGEGOLD_HANDLER = DisableAbleCommandHandler("changegold", alterGold, pass_args=True)
CHANGEXP_HANDLER = DisableAbleCommandHandler("changexp", alterExperience, pass_args=True)

dispatcher.add_handler(SETDM_HANDLER)
dispatcher.add_handler(CHANGEHEALTH_HANDLER)
dispatcher.add_handler(CHANGEGOLD_HANDLER)
dispatcher.add_handler(CHANGEXP_HANDLER)

CREATECHARACTER_HANDLER = DisableAbleCommandHandler("createcharacter", createCharacter, pass_args=True)
PRINTCHARACTERSTATS_HANDLER = DisableAbleCommandHandler("printcharacterstats", printCharacterStats, pass_args=True)
UPDATEINVENTORY_HANDLER = DisableAbleCommandHandler("updateinventory", inventoryUpdate, pass_args=True)
PRINTINVENTORY_HANDLER = DisableAbleCommandHandler("printinventory", printInventory, pass_args=True)

dispatcher.add_handler(CREATECHARACTER_HANDLER)
dispatcher.add_handler(PRINTCHARACTERSTATS_HANDLER)
dispatcher.add_handler(UPDATEINVENTORY_HANDLER)
dispatcher.add_handler(PRINTINVENTORY_HANDLER)


