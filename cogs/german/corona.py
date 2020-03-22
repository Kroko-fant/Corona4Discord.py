import json
import re
import urllib

import discord
from discord.ext import commands


class Corona(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Function to print news when !corona news or !corn or !coronanews is called
    async def printnews(self, ctx):
        url = "https://covidapi.org/api/news_feed_html.php"
        response = urllib.request.urlopen(url)
        response = response.read()
        # parsing the respoonse for the news
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
        # Catching input-country news
        if country == "news":
            await self.printnews(ctx)
            return
        url = f"https://covidapi.org/api/newest_report.php?search={country}"
        # import the json as a dictionary
        response = urllib.request.urlopen(url)
        response2 = str(response.read()).replace("\\n", "").replace("\\r", "")[2:-1]
        data = json.loads(response2)
        # if just one result is shown print it!
        if len(data['items']) == 1:
            confirmed = data['items'][0]['confirmed']
            recovered = data['items'][0]['recovered']
            dead = data['items'][0]['deaths']
        # else add all countrys matching the first one espacially for China and US
        else:
            country = data['items'][0]['country']
            confirmed = 0
            recovered = 0
            dead = 0
            for entry in data['items']:
                if entry['country'] == country:
                    confirmed += entry['confirmed']
                    recovered += entry['recovered']
                    dead += entry['deaths']
        description = f"Infiziert: {confirmed}\nTode: {dead}\nGeheilt:" \
                      f" {recovered}\nLetztes Update: {data['items'][0]['last_update']}"
        coronaembed = discord.Embed(title=f"Akltuelle Daten aus {data['items'][0]['country']}",
                                    description=description,
                                    color=2263842)
        coronaembed.set_footer(text="Niklas Fehde, https://covidapi.org/")
        await ctx.send(embed=coronaembed)


def setup(bot):
    bot.add_cog(Corona(bot))
