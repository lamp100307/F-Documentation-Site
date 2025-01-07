from sqlite3 import IntegrityError
from typing import Optional

import aiosqlite

class Database:
    def __init__(self):
        self.path = 'temp/Database.db'

    async def restart_db(self):
        async with aiosqlite.connect(self.path) as db:
            await db.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER NOT NULL PRIMARY KEY,
                    send BOOLEAN NOT NULL,
                    counter INTEGER DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    text TEXT NOT NULL
                )
            ''')
            await db.commit()


    @property
    async def users(self) -> list[Optional[dict[int, bool]]]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM users') as cursor:
                users = await cursor.fetchall()
                return [dict(user) for user in users]

    async def add_user(self, id_: int, send: bool):
        async with aiosqlite.connect(self.path) as db:
            try:
                await db.execute('INSERT INTO users (id, send) VALUES (?, ?)', (id_, send))
                await db.commit()
            except IntegrityError:
                pass


    @property
    async def questions(self, id_: int = None) -> list[Optional[tuple[int, str, str]]]:
        async with aiosqlite.connect(self.path) as db:
            command = 'SELECT * FROM questions'
            if id_ is not None:
                command += ' WHERE id = ?'
                args = (id_,)
            else:
                args = ()
            async with db.execute(command, args) as cursor:
                return await cursor.fetchall()

    async def add_question(self, name: str, question: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute('INSERT INTO questions (name, text) VALUES (?, ?)', (name, question))
            await db.commit()

    async def increase_counter(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute('UPDATE users SET counter = counter + 1')
            await db.commit()

    async def reset_counter(self, id_: int):
        async with aiosqlite.connect(self.path) as db:
            await db.execute('UPDATE users SET counter = 0 WHERE id = ?', (id_,))
            await db.commit()