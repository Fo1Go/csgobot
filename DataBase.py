import sqlite3

database = 'database/database.db'

class DataBase():
    def __init__(self):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def addUser(self, telegram_id):
        if not self.user_exist(telegram_id):
            with self.connection:
                return self.cursor.execute(f"INSERT INTO `bot_Users` (`telegram_id`,`subscribed_matches`,`subscribed_updates`,`subscribed_news`) VALUES({telegram_id},False,False,False)")

    def get_subscriptions_matches(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `bot_Users` WHERE `subscribed_matches` = True")

    def get_subscriptions_news(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `bot_Users` WHERE `subscribed_news` = True")

    def get_subscriptions_updates(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `bot_Users` WHERE `subscribed_updates` = True")

    def update_subscription_matches(self, telegram_id, val):
        if self.user_exist(telegram_id):
            with self.connection:
                return self.cursor.execute(f"UPDATE `bot_Users` SET `subscribed_matches` = {val} WHERE `telegram_id` = {telegram_id}")
        else:
            self.addUser(telegram_id)
            with self.connection:
                return self.cursor.execute(f"UPDATE `bot_Users` SET `subscribed_matches` = {val} WHERE `telegram_id` = {telegram_id}")

    def update_subscription_news(self, telegram_id, val):
        if self.user_exist(telegram_id):
            with self.connection:
                return self.cursor.execute(f"UPDATE `bot_Users` SET `subscribed_news` = {val} WHERE `telegram_id` = {telegram_id}")
        else:
            self.addUser(telegram_id)
            with self.connection:
                return self.cursor.execute(f"UPDATE `bot_Users` SET `subscribed_news` = {val} WHERE `telegram_id` = {telegram_id}")

    def update_subscription_updates(self, telegram_id, val):
        if self.user_exist(telegram_id):
            with self.connection:
                return self.cursor.execute(f"UPDATE `bot_Users` SET `subscribed_updates` = {val} WHERE `telegram_id` = {telegram_id}")
        else:
            self.addUser(telegram_id)
            with self.connection:
                return self.cursor.execute(f"UPDATE `bot_Users` SET `subscribed_updates` = {val} WHERE `telegram_id` = {telegram_id}")

    def user_exist(self,telegram_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `bot_Users` WHERE `telegram_id` = {telegram_id}')
            return bool(len(list(result)))

    def close(self):
        self.connection.close()