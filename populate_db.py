import random
import sqlite3
import time

from faker import Faker

fake = Faker()

conn = sqlite3.connect('votes.db')

song_id = range(0, 100)
user_id = range(0, 100)
usernames = [fake.user_name() for _ in range(100)]

for song in song_id:
    for user, uname in zip(user_id, usernames):
        vote = random.randint(1, 5)
        conn.execute("INSERT INTO votes (song_id, user_id, username, vote, timestamp) VALUES (?, ?, ?, ?, ?)", (song, user, uname, vote, time.time()))
conn.commit()