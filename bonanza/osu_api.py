import datetime

import aiohttp


class OsuApiV2(aiohttp.ClientSession):
    def __init__(self, client_id, client_secret):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://osu.ppy.sh/api/v2/"
        self.token = None
        self.token_expire = datetime.datetime.now()

    async def _get_token(self):
        url = "https://osu.ppy.sh/oauth/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            'scope': 'public'
        }
        async with self.post(url, json=params) as resp:
            return await resp.json()

    async def _get_endpoint(self, endpoint, params=None):
        if params is None:
            params = {}

        if self.token_expire < datetime.datetime.now():
            self.token = await self._get_token()
            self.token_expire = datetime.datetime.now() + datetime.timedelta(seconds=self.token["expires_in"])

        headers = {"Authorization": "Bearer " + self.token["access_token"]}
        async with self.get(self.base_url + endpoint, params=params, headers=headers) as resp:
            return await resp.json()

    async def get_beatmap(self, beatmap_id):
        return await self._get_endpoint(f"beatmaps/{beatmap_id}")

