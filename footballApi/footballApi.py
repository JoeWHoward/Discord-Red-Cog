import datetime

import requests
from dotmap import DotMap
from redbot.cogs.cleanup.converters import positive_int
from redbot.core import commands

LEAGUE_ID_MAP = {
    "epl": {"id": 39, "name": "English Premier League"},
    "gbl": {"id": 78, "name": "German Bundesliga League"},
    "nel": {"id": 88, "name": "Netherlands Eredivisie League"},
    "sll": {"id": 140, "name": "Spain Laliga League"},
    "fl": {"id": 61, "name": "French League 1"},
}


class FootballAPI(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    async def warn_and_exit_if_no_api_keys(self, ctx):
        rapidapi_keys = await self.bot.get_shared_api_tokens("rapidapi")
        if rapidapi_keys.get("api_key") is None:
            return await ctx.send("The RapidAPI API Key has not been set.")
        if rapidapi_keys.get("api_host") is None:
            return await ctx.send("The RapidAPI API Host has not been set.")

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff2223!")

    @commands.command()
    async def rapidapi(self, ctx):
        self.warn_and_exit_if_no_api_keys(ctx)

    @commands.command()
    async def football(self, ctx: commands.Context, league: str, games: positive_int):
        await self.warn_and_exit_if_no_api_keys(ctx)
        rapidapi_keys = await self.bot.get_shared_api_tokens("rapidapi")

        if league not in LEAGUE_ID_MAP.keys():
            out_str = f"League must be one of: \n\n"
            for x, y in LEAGUE_ID_MAP.items():
                out_str += f"{y.get('name')}: `{x}`\n"
            return await ctx.send(out_str)

        league_id = LEAGUE_ID_MAP.get(league).get('id')

        if not games:
            games = 10

        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

        querystring = {"league": str(league_id), "season": "2022", "next": str(games), "timezone": "America/Chicago"}

        headers = {
            "X-RapidAPI-Key": rapidapi_keys.get("api_key"),
            "X-RapidAPI-Host": rapidapi_keys.get("api_host")
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()

        fixtures = data.get("response")

        out_str = ""
        await ctx.send(f"**{DotMap(fixtures[0]).league.name}**")
        for x in fixtures:
            x = DotMap(x)
            await ctx.send(f'''
            __{x.teams.home.name}__ vs __{x.teams.away.name}__
*{datetime.datetime.fromisoformat(x.fixture.date).strftime("%Y-%m-%d %I:%M %p")}*
''')
