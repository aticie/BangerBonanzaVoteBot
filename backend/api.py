from typing import List

from fastapi import FastAPI

from bonanza.database.votes import VotesDB

app = FastAPI()
db = VotesDB('votes.db')


@app.on_event("startup")
async def startup_event():
    await db.initialize_tables()


@app.get("/")
async def root():
    return {"me": "Banger Bonanza Voting API"}


@app.get("/votes/{song_id}")
async def get_votes(song_id: int):
    return await db.get_votes(song_id)


@app.get("/votes/{song_id}/{username}")
async def get_user_vote(song_id: int, username: int):
    return await db.get_user_vote(song_id, username)


@app.get("/votes/{username}")
async def get_user_votes(username: int):
    return await db.get_user_votes(username)


@app.get("/vote_count/{song_id}")
async def get_song_vote_count(song_id: int):
    return await db.get_song_vote_count(song_id)


@app.get("/vote_count/{username}")
async def get_user_vote_count(username: int):
    return await db.get_user_vote_count(username)


@app.get("/vote_count")
async def get_total_vote_count():
    return await db.get_total_vote_count()


@app.get("/vote_count/{username}")
async def get_user_vote_count_for_songs(username: int, song_ids: List[int]):
    return await db.get_user_vote_count_for_songs(username, song_ids)
