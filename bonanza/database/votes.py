import time

import aiosqlite



class VotesDB:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = "/bonanza/database/votes.db"
        self.db_path = db_path
        self.con = None

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    async def initialize_tables(self):
        self.con = await aiosqlite.connect(self.db_path)
        self.con.row_factory = VotesDB.dict_factory
        await self.con.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                song_id INTEGER NOT NULL,
                vote INTEGER NOT NULL,
                timestamp INTEGER NOT NULL
            )
        """)
        await self.con.commit()

    async def add_vote(self, user_id, song_id, vote):
        user_voted = await self.get_user_vote(user_id, song_id)
        if user_voted is not None:
            await self.con.execute("""
                UPDATE votes SET vote = ?, timestamp = ? WHERE user_id = ? AND song_id = ?
            """, (vote, int(time.time()), user_id, song_id))
        else:
            await self.con.execute("""
                INSERT INTO votes (user_id, username, song_id, vote, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, song_id, vote, int(time.time())))
        await self.con.commit()

    async def get_votes(self, song_id):
        cursor = await self.con.execute("""
            SELECT user_id, username, vote FROM votes WHERE song_id = ?
        """, (song_id,))
        return await cursor.fetchall()

    async def get_user_votes(self, username):
        cursor = await self.con.execute("""
            SELECT song_id, vote FROM votes WHERE username = ?
        """, (username,))
        return await cursor.fetchall()

    async def get_user_vote(self, username, song_id):
        cursor = await self.con.execute("""
            SELECT vote FROM votes WHERE username = ? AND song_id = ?
        """, (username, song_id))
        return await cursor.fetchone()[0]

    async def get_song_vote_count(self, song_id):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes WHERE song_id = ?
        """, (song_id,))
        return await cursor.fetchone()[0]

    async def get_user_vote_count(self, username):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes WHERE username = ?
        """, (username,))
        return await cursor.fetchone()[0]

    async def get_user_vote_count_for_songs(self, username, song_ids):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes WHERE username = ? AND song_id IN ({})
        """.format(",".join(["?"] * len(song_ids))), (username,) + tuple(song_ids))
        return await cursor.fetchone()[0]

    async def get_total_vote_count(self):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes
        """)
        return await cursor.fetchone()[0]
