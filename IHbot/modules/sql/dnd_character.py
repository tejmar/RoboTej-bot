# import threading
#
# from sqlalchemy import Column, UnicodeText, Integer
#
# from IHbot.modules.sql import BASE, SESSION
#
# class RSS(BASE):
#     __tablename__ = "dnd_character"
#     id = Column(Integer, primary_key=True)
#     chat_id = Column(UnicodeText, nullable=False)
#     dungeon_master = Column(UnicodeText)
#
#     def __init__(self, chat_id, dm):
#         self.chat_id = chat_id
#         self.dungeon_master = dm
#
#     def __repr__(self):
#         return "<DND_GAME for chatID {} at with master {}>".format(self.chat_id, self.dungeon_master)
#
#
# RSS.__table__.create(checkfirst=True)
# INSERTION_LOCK = threading.RLock()
#
