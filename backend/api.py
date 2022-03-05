import json
import os
from typing import List

from fastapi import FastAPI

from bonanza.database.votes import VotesDB

app = FastAPI()
db = VotesDB(os.getenv('DB_DIR', 'votes.db'))


@app.on_event("startup")
async def startup_event():
    await db.initialize_tables()


@app.get("/")
async def root():
    return {"me": "Banger Bonanza Voting API"}


@app.get("/votes/{beatmap_id}")
async def get_votes(beatmap_id: int):
    """
    Returns the votes for a single beatmap.
    :param beatmap_id: beatmap_id
    :return: List[Dictionary]
    """
    return await db.get_votes(beatmap_id)


@app.get("/votes/{beatmap_id}/{username}")
async def get_user_vote(beatmap_id: int, username: int):
    """
    Returns the vote for a single user on a beatmap.
    :param beatmap_id: Beatmap id
    :param username: Voter username
    :return: Dictionary
    """
    return await db.get_user_vote(beatmap_id, username)


@app.get("/votes/{username}")
async def get_user_votes(username: int):
    """
    Returns the votes for a single user.
    :param username: Voter username
    :return: Dictionary
    """
    return await db.get_user_votes(username)


@app.get("/vote_count/{beatmap_id}")
async def get_song_vote_count(beatmap_id: int):
    """
    Returns the vote count for a single beatmap.
    :param beatmap_id:
    :return: Integer
    """
    return await db.get_beatmap_vote_count(beatmap_id)


@app.get("/vote_count/{username}")
async def get_user_vote_count(username: int):
    """
    Returns the vote count for a single user.
    :param username: Voter username
    :return: Integer
    """
    return await db.get_user_vote_count(username)


@app.get("/vote_count")
async def get_total_vote_count():
    """
    Returns the total vote count.
    :return: Integer
    """
    return await db.get_total_vote_count()


@app.get("/vote_count/{username}")
async def get_user_vote_count_for_songs(username: int, beatmap_ids: List[int]):
    """
    Returns the vote count for a list of beatmaps of a single user.
    :param username: Voter username
    :param beatmap_ids: Beatmap ids
    :return: Integer
    """
    return await db.get_user_vote_count_for_beatmaps(username, beatmap_ids)


@app.get("/current_beatmap")
async def get_current_beatmap():
    """
    Returns details about the current beatmap.

    Returned object is the same as https://osu.ppy.sh/docs/index.html#beatmap
    :return: Dictionary
    """
    current_beatmap_dict = await db.get_current_beatmap()
    if current_beatmap_dict is None:
        return None
    else:
        return json.loads(current_beatmap_dict['beatmap_details'])


@app.get("/current_beatmap/id")
async def get_current_beatmap_id():
    """
    Returns the id of the current beatmap.

    :return: String
    """
    return await db.get_current_beatmap_id()
