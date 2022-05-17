import json
import os
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from bonanza.database.votes import VotesDB
from bonanza.osu_api import OsuApiV2

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = VotesDB(os.getenv('DB_DIR', 'votes.db'))
secret_key = os.getenv('SECRET_KEY')
osu_client_id = os.getenv("OSU_CLIENT_ID")
osu_client_secret = os.getenv("OSU_CLIENT_SECRET")


@app.on_event("startup")
async def startup_event():
    await db.initialize_tables()


@app.get("/")
async def root():
    return {"me": "Banger Bonanza Voting API"}


@app.get("/votes")
async def get_user_vote(beatmap_id: int, username: str):
    """
    Returns the vote for a single user on a beatmap.
    :param beatmap_id: Beatmap id
    :param username: Voter username
    :return: Dictionary
    """
    return await db.get_user_vote(username=username,
                                  beatmap_id=beatmap_id)


@app.get("/votes/b/{beatmap_id}")
async def get_votes(beatmap_id: int):
    """
    Returns the votes for a single beatmap.
    :param beatmap_id: beatmap_id
    :return: List[Dictionary]
    """
    return await db.get_votes(beatmap_id)


@app.get("/votes/u/{username}")
async def get_user_votes(username: str):
    """
    Returns the votes for a single user.
    :param username: Voter username
    :return: Dictionary
    """
    return await db.get_user_votes(username)


@app.get("/vote_count/b/{beatmap_id}")
async def get_song_vote_count(beatmap_id: int):
    """
    Returns the vote count for a single beatmap.
    :param beatmap_id:
    :return: Integer
    """
    return await db.get_beatmap_vote_count(beatmap_id)


@app.get("/vote_count/u/{username}")
async def get_user_vote_count(username: str, beatmap_ids: Optional[List[int]] = Query(None)):
    """
    Returns the vote count for a single user.
    :param username: Voter username
    :param beatmap_ids: List of beatmap ids
    :return: Integer
    """
    if beatmap_ids is None:
        return await db.get_user_vote_count(username)
    else:
        return await db.get_user_vote_count_for_beatmaps(username, beatmap_ids)


@app.get("/vote_count")
async def get_total_vote_count(beatmap_ids: Optional[List[int]] = Query(None)):
    """
    Returns the total vote count.
    :return: Integer
    """
    if beatmap_ids is None:
        return await db.get_total_vote_count()
    else:
        return await db.get_total_vote_count_for_beatmaps(beatmap_ids)


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


@app.post("/current_beatmap")
async def change_current_beatmap(beatmap_id: int, auth: str):
    """
    Changes the current beatmap to the specified one.
    """

    if auth != secret_key:
        return {'error': 'You shouldn\'t do that.'}

    async with OsuApiV2(osu_client_id, osu_client_secret) as osu_api:
        current_beatmap = await osu_api.get_beatmap(beatmap_id)
        await db.set_current_beatmap(current_beatmap)
