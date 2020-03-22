import discord
import json
import re
import urllib

from discord.ext import commands

# Inputs
TOKEN = "YOUR TOKEN HERE"  # TODO
PREFIX = "!" # If you want you can change your Prefix here
bot = commands.Bot(command_prefix=PREFIX)


# Function to print news when !corona news or !corn or !coronanews is called
async def printnews(ctx):
    url = "https://covidapi.org/api/news_feed_html.php"
    response = urllib.request.urlopen(url)
    response = response.read()
    # parsing the respoonse for the news
    response = re.search("</html>.*<br>", str(response))
    response = response[0].replace("</html>\\n", "").replace("<br>", "\n")
    newsembed = discord.Embed(title="Corona-News", description=response, color=2263842)
    newsembed.set_footer(text="Niklas Fehde, https://covidapi.org/")
    await ctx.send(embed=newsembed)


@bot.command(aliases=["corn"])
async def coronanews(ctx):
    """Actual News"""
    await printnews(ctx)


@bot.command(aliases=["cor"])
async def corona(ctx, country="US"):  # specify your main-country here
    """Actual Cases !corona <country>"""
    # Catching input-country news
    if country == "news":
        await printnews(ctx)
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
    description = f"Infected: {confirmed}\nDeaths: {dead}\nRecovered:" \
                  f" {recovered}\nLast Update: {data['items'][0]['last_update']}"
    coronaembed = discord.Embed(title=f"Actual Data from {data['items'][0]['country']}",
                                description=description,
                                color=2263842)
    coronaembed.set_footer(text="Niklas Fehde, https://covidapi.org/")
    await ctx.send(embed=coronaembed)

bot.run(TOKEN)
