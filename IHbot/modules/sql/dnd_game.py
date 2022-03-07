import threading

from sqlalchemy import Column, UnicodeText, Integer

from IHbot.modules.sql import BASE, SESSION


class DND_GAME(BASE):
    __tablename__ = "dnd_games"
    id = Column(Integer, primary_key=True)
    chat_id = Column(UnicodeText, nullable=False)
    dungeon_master = Column(UnicodeText)

    def __init__(self, chat_id, dm):
        self.chat_id = chat_id
        self.dungeon_master = dm

    def __repr__(self):
        return "<DND_GAME for chatID {} at with master {}>".format(self.chat_id, self.dungeon_master)


DND_GAME.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def check_availability(tg_chat_id):
    try:
        return SESSION.query(DND_GAME).filter(DND_GAME.chat_id == tg_chat_id).all()
    finally:
        SESSION.close()


def check_exists(tg_chat_id, dm):
    try:
        return SESSION.query(DND_GAME).filter(DND_GAME.chat_id == tg_chat_id, DND_GAME.dungeon_master == dm).all()
    finally:
        SESSION.close()


def add_game(tg_chat_id, dm):
    with INSERTION_LOCK:
        action = DND_GAME(tg_chat_id, dm)

        SESSION.add(action)
        SESSION.commit()


def remove_game(tg_chat_id):
    found = False
    with INSERTION_LOCK:
        # this loops to delete any possible duplicates
        for row in check_availability(tg_chat_id):
            SESSION.delete(row)
            found = True

        SESSION.commit()
        return found


def get_game(tg_chat_id):
    try:
        return SESSION.query(DND_GAME).filter(DND_GAME.chat_id == tg_chat_id).first()
    finally:
        SESSION.close()


def set_dm(tg_chat_id, user, new_dm, is_admin):
    with INSERTION_LOCK:
        # this loops to delete any possible duplicates
        for row in check_availability(tg_chat_id):
            if row.dungeon_master == user or is_admin:
                # add the action to the DB query
                row.dungeon_master = new_dm
                return True
        SESSION.commit()
        return False
