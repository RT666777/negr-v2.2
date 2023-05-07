import yaml
import sqlite3

with open("config.yml", "r", encoding="UTF-8") as file:
    data = yaml.load(file, Loader=yaml.FullLoader)


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(data['databaseDefPath'])
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS dialogs (number INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "id1 INTEGER UNIQUE, "
                       "id2 INTEGER UNIQUE)")
        self.conn.commit()

    async def replaceDialogs(self, id1, id2):
        self.c.execute("REPLACE INTO dialogs VALUES (?, ?, ?)", (None, id1, id2))
        self.conn.commit()

    async def updateDialogs(self, num, id):
        self.c.execute(f"UPDATE dialogs set id{num}=? WHERE id2 IS NULL", (id, ))
        self.conn.commit()

    async def getDialogs(self, id):
        self.c.execute("SELECT * FROM dialogs WHERE id1=? OR id2=?", (id, id))
        dialogs = self.c.fetchall()
        return dialogs

    async def getNullDialogs(self):
        self.c.execute("SELECT id1 FROM dialogs WHERE id2 IS NULL")
        nullDialog = self.c.fetchone()
        return nullDialog

    async def stopDialog(self, id):
        self.c.execute("DELETE FROM dialogs WHERE id1=? OR id2=?", (id, id))
        self.conn.commit()
