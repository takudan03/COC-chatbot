import coc, discord, traceback
from riotwatcher import LolWatcher, ApiError
from discord.ext import commands
from coc import utils

'''
Store auth info in separate file:
line0: COC dev username
line1: COC dev password
line2: DC Info channel ID
line3: DC Oauth2 token
line4: COC clan tag
'''

with open("esportbot_food.txt") as f:
    auth = f.readlines()

auth = [x.strip() for x in auth]

clan_tag = auth[4]

coc_client=coc.login(auth[0], auth[1], key_count=5, key_names="Bot key", client=coc.EventsClient)

bot=commands.Bot(command_prefix='!')
INFO_CHANNEL_ID=int(auth[2])

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def members(ctx):
    members=await coc_client.get_members(clan_tag)
    to_send="Members:\n"
    for player in members:
        to_send+="{0} ({1})\n".format(player.name, player.tag)

    await ctx.send(to_send)

@bot.command()
async def heroes(ctx, player_tag):
    player=await coc_client.get_player(player_tag)
    to_send="HEROES: \n"
    for hero in player.heroes:
        to_send+="{}: Level {}/{}\n".format(str(hero), hero.level, hero.max_level)
    await ctx.send(to_send)

@bot.command()
async def home_troops(ctx, player_tag):
    player=await coc_client.get_player(player_tag)
    to_send="⚔️HOME BASE TROOPSD:\n"
    for troop in player.home_troops:
        to_send+="{}: Level {}/{}\n".format(str(troop.name), str(troop.level), str(troop.max_level))
    await ctx.send(to_send)

@bot.command()
async def builder_troops(ctx, player_tag):
    player=await coc_client.get_player(player_tag)
    to_send="⚔️BUILDER BASE Troops:\n"
    for troop in player.builder_troops:
        to_send+="{}: Level {}/{}\n".format(str(troop.name), str(troop.level), str(troop.max_level))
    await ctx.send(to_send)

@bot.command()
async def getPlayerInfo(ctx, player_tag):
    player = await coc_client.get_player(player_tag)
    to_send = "{} ({}), XP LVL: {}\n".format(player.name, player_tag, player.exp_level)
    to_send += "TOWN HALL LVL: {} (🏆 {})\n".format(player.town_hall, player.trophies)
    to_send += "BUILDER BASE HALL LVL: {} (🏆 {})\n".format(player.builder_hall, player.versus_trophies)

    await ctx.send(to_send)

bot.run(auth[3])