import random
import sqlite3
import time

from faker import Faker

fake = Faker()

conn = sqlite3.connect('votes.db')

beatmap_id = range(0, 100)
user_id = range(0, 100)
usernames = [fake.user_name() for _ in range(100)]

for bmap in beatmap_id:
    for user, uname in zip(user_id, usernames):
        vote = random.randint(1, 5)
        conn.execute("INSERT INTO votes (beatmap_id, user_id, username, vote, timestamp) VALUES (?, ?, ?, ?, ?)", (bmap, user, uname, vote, time.time()))
conn.commit()