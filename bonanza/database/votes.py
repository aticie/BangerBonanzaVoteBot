import json
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
                beatmap_id INTEGER NOT NULL,
                vote INTEGER NOT NULL,
                timestamp INTEGER NOT NULL
            )
        """)
        await self.con.execute("""
                    CREATE TABLE IF NOT EXISTS current_beatmap (
                        beatmap_id INTEGER NOT NULL,
                        beatmap_details TEXT NOT NULL
                    )
                """)
        await self.con.commit()

    async def get_current_beatmap(self):
        cursor = await self.con.execute("""
            SELECT beatmap_id, beatmap_details FROM current_beatmap
        """)
        beatmap_details = await cursor.fetchone()
        return beatmap_details

    async def get_current_beatmap_id(self):
        cursor = await self.con.execute("""
            SELECT beatmap_id FROM current_beatmap
        """)
        beatmap_id = await cursor.fetchone()
        return beatmap_id

    async def remove_current_beatmap(self):
        current_beatmap = await self.get_current_beatmap()
        if current_beatmap is not None:
            current_beatmap_id = current_beatmap['beatmap_id']
            await self.con.execute("""
                DELETE FROM current_beatmap WHERE beatmap_id = ?
            """, (current_beatmap_id,))
            await self.con.commit()

    async def set_current_beatmap(self, beatmap_details: dict):
        await self.remove_current_beatmap()

        beatmap_id = beatmap_details["id"]
        beatmap_details_txt = json.dumps(beatmap_details)
        await self.con.execute("""
            INSERT INTO current_beatmap (beatmap_id, beatmap_details) VALUES (?, ?)
        """, (beatmap_id, beatmap_details_txt))
        await self.con.commit()

    async def add_vote(self, user_id, username, beatmap_id, vote):
        user_voted = await self.get_user_vote(username, beatmap_id)
        if user_voted is not None:
            await self.con.execute("""
                UPDATE votes SET vote = ?, timestamp = ? WHERE user_id = ? AND beatmap_id = ?
            """, (vote, int(time.time()), user_id, beatmap_id))
        else:
            await self.con.execute("""
                INSERT INTO votes (user_id, username, beatmap_id, vote, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, beatmap_id, vote, int(time.time())))
        await self.con.commit()

    async def get_votes(self, beatmap_id):
        cursor = await self.con.execute("""
            SELECT user_id, username, vote FROM votes WHERE beatmap_id = ?
        """, (beatmap_id,))
        return await cursor.fetchall()

    async def get_user_votes(self, username):
        cursor = await self.con.execute("""
            SELECT beatmap_id, vote FROM votes WHERE username = ?
        """, (username,))
        return await cursor.fetchall()

    async def get_user_vote(self, username, beatmap_id):
        cursor = await self.con.execute("""
            SELECT vote FROM votes WHERE username = ? AND beatmap_id = ?
        """, (username, beatmap_id))
        vote = await cursor.fetchone()
        return vote

    async def get_beatmap_vote_count(self, beatmap_id):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes WHERE beatmap_id = ?
        """, (beatmap_id,))
        vote_count = await cursor.fetchone()
        return vote_count['COUNT(*)']

    async def get_user_vote_count(self, username):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes WHERE username = ?
        """, (username,))
        vote_count = await cursor.fetchone()
        return vote_count['COUNT(*)']

    async def get_user_vote_count_for_beatmaps(self, username, beatmap_ids):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes WHERE username = ? AND beatmap_id IN ({})
        """.format(",".join(["?"] * len(beatmap_ids))), (username,) + tuple(beatmap_ids))
        vote_count = await cursor.fetchone()
        return vote_count['COUNT(*)']

    async def get_total_vote_count_for_beatmaps(self, beatmap_ids):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes WHERE beatmap_id IN ({})
        """.format(",".join(["?"] * len(beatmap_ids))), tuple(beatmap_ids))
        vote_count = await cursor.fetchone()
        return vote_count['COUNT(*)']

    async def get_total_vote_count(self):
        cursor = await self.con.execute("""
            SELECT COUNT(*) FROM votes
        """)
        vote_count = await cursor.fetchone()
        return vote_count['COUNT(*)']
