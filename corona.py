import json
import re
import urllib

import discord
from discord.ext import commands


class Corona(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def printnews(self, ctx):
        url = "https://covidapi.org/api/news_feed.php"
        response = urllib.request.urlopen(url)
        response = response.read()
        response = re.search("</html>.*<br>", str(response))
        response = response[0].replace("</html>\\n", "").replace("<br>", "\n")
        newsembed = discord.Embed(title="Corona-News", description=response, color=2263842)
        newsembed.set_footer(text="Niklas Fehde, https://covidapi.org/")
        await ctx.send(embed=newsembed)

    @commands.command(aliases=["corn"])
    async def coronanews(self, ctx):
        """Actual News"""
        await self.printnews(ctx)

    @commands.command(aliases=["cor"])
    async def corona(self, ctx, country="ger"):
        """Actual Cases !corona <country>"""
        if country == "news":
            await self.printnews(ctx)
            return
        url = f"https://covidapi.org/api/newest_report.php?search={country}"
        response = urllib.request.urlopen(url)
        response2 = str(response.read()).replace("\\n", "").replace("\\r", "")[2:-1]
        data = json.loads(response2)
        if len(data['items']) == 1:
            confirmed = data['items'][0]['confirmed']
            recovered = data['items'][0]['recovered']
            dead = data['items'][0]['deaths']
        else:
            country = data['items'][0]['country']
            confirmed = 0
            recovered = 0
            dead = 0
            for object in data['items']:
                if object['country'] == country:
                    confirmed += object['confirmed']
                    recovered += object['recovered']
                    dead += object['deaths']
        description = f"Infected: {confirmed}\nDeaths: {dead}\nRecovered:" \
                      f" {recovered}\nLast Update: {data['items'][0]['last_update']}"
        coronaembed = discord.Embed(title=f"Actual Data from {data['items'][0]['country']}",
                                    description=description,
                                    color=2263842)
        coronaembed.set_footer(text="Niklas Fehde, https://covidapi.org/")
        await ctx.send(embed=coronaembed)


def setup(bot):
    bot.add_cog(Corona(bot))
