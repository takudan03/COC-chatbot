import coc, discord, traceback
from discord.ext import commands
from discord import client, channel
from coc import utils

'''
Store auth info in separate file: "./coc_bot_food.txt"
line0: COC dev username
line1: COC dev password
line2: DC Info channel ID
line3: DC Oauth2 token
line4: COC clan tag
line5: DC server ID
'''

with open("coc_bot_food.txt") as f:
    auth = f.readlines()
auth = [x.strip() for x in auth]

coc_client = coc.login(auth[0], auth[1], key_count=5, key_names="Bot key", client=coc.EventsClient)

try:
    clan_tag = auth[4]
    coc_client.add_clan_updates(clan_tag)
except:
    print("No Clan tag provided in credential files!")
    clan_tag = "#0000000"
INFO_CHANNEL_ID = int(auth[2])
INFO_SERVER_ID = int(auth[5])

bot = commands.Bot(command_prefix='!')
# mchannel = bot.get_channel(INFO_SERVER_ID)


@bot.event
async def on_ready():
    print("BOT is up and running!")  # lets you know the bot is online and ready
    global mchannel
    mchannel = bot.get_channel(INFO_SERVER_ID)

    await bot.wait_until_ready()



@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I am up and running!")


@bot.command()
async def all_commands(ctx):
    to_send = "I accept the following commands:\n"
    to_send += "!hello : To check bot status\n"
    to_send += "!player_info <Player Tag>: Displays account info for the player with the provided player tag\n"
    to_send += "!clan_members <Clan Tag>: Displays list of members in the clan with the provided clan tag\n"
    to_send += "!my_clan_members : Displays list of members in the clan with the clan tag in the credential file\n"
    to_send += "!home_troops <Player Tag>: Displays Home Base troops and levels for the player with provided player tag\n"
    to_send += "!builder_troops <Player Tag>: Displays Builder Base troops and levels for the player with provided player tag\n"
    to_send += "!heroes <Player Tag>: Displays Hero info for player with provided tag\n"
    to_send += "!my_clan_info : Displays Clan info for default clan provided in credential file\n"
    to_send += "!clan_info <Player Tag>: Displays Clan info for clan with provided tag\n"
    to_send += "!watch_player <Player Tag>: Add provided player to list of players who recieve Bot updates regarding their account\n"
    to_send += "!uwatch_player <Player Tag>: Add provided player to list of players who recieve Bot updates regarding their account\n"

    await ctx.send(to_send)


@bot.command()
async def heroes(ctx, player_tag):
    player = await coc_client.get_player(player_tag)
    to_send = "HEROES: \n"
    for hero in player.heroes:
        to_send += "{}: Level {}/{}\n".format(str(hero), hero.level, hero.max_level)
    await ctx.send(to_send)


@bot.command()
async def home_troops(ctx, player_tag):
    player = await coc_client.get_player(player_tag)
    to_send = "🏠HOME BASE TROOPS:\n"
    for troop in player.home_troops:
        to_send += "☞{}: Level {}/{}\n".format(str(troop.name), str(troop.level), str(troop.max_level))
    await ctx.send(to_send)


@bot.command()
async def builder_troops(ctx, player_tag):
    player = await coc_client.get_player(player_tag)
    to_send = "⚔️BUILDER BASE Troops:\n"
    for troop in player.builder_troops:
        to_send += "☞{}: Level {}/{}\n".format(str(troop.name), str(troop.level), str(troop.max_level))
    await ctx.send(to_send)


@bot.command()
async def player_info(ctx, player_tag):
    player = await coc_client.get_player(player_tag)
    to_send = "⚜️️{} ({}), XP LVL: {}\n".format(player.name, player_tag, player.exp_level)
    to_send += "🏠TOWN HALL LVL: {} (🏆 {})\n".format(player.town_hall, player.trophies)
    to_send += "⚔️BUILDER BASE HALL LVL: {} (🏆 {})\n".format(player.builder_hall, player.versus_trophies)

    await ctx.send(to_send)


@bot.command()
async def my_clan_info(ctx):
    if clan_tag == "#0000000":
        to_send = "❌You have not provided your clan tag in the credential file. EIther do so, or use command !clan_info <clan_tag>"
    else:
        clan = await coc_client.get_clan(clan_tag)
        to_send = "CLAN INFO:\n"
        to_send += "{} ({}): Level {}\n".format(clan.name, clan_tag, clan.level)
        to_send += "Description: {}\n".format(clan.description)
        to_send += "Location: {}\n".format(clan.location)
        to_send += "Required Trophies: 🏆{}\n".format(clan.required_trophies)
        to_send += "War Wins: {}\n".format(clan.war_wins)

    await ctx.send(to_send)


@bot.command()
async def clan_info(ctx, tag):
    clan = await coc_client.get_clan(tag)
    to_send = "CLAN INFO:\n"
    to_send += "{} ({}): Level {}\n".format(clan.name, tag, clan.level)
    to_send += "Description: {}\n".format(clan.description)
    to_send += "Location: {}\n".format(clan.location)
    to_send += "Required Trophies: 🏆{}\n".format(clan.required_trophies)
    to_send += "War Wins: {}\n".format(clan.war_wins)


@coc_client.event
@coc.ClanEvents.description()
@coc.ClanEvents.level()
async def clan_update(old_clan, new_clan):
    if old_clan.level != new_clan.level:
        to_send = "❕UPDATE❕\n"
        to_send += "THE CLAN HAS GONE UP A LEVEL! NEW LEVEL: {}".format(new_clan.level)
        await mchannel.send(to_send)
    elif old_clan.description != new_clan.description:
        to_send = "❕UPDATE❕\n"
        to_send += "THE CLAN DESCRIPTION HAS BEEN CHANGED. NEW DESCRIPTION: \n"
        to_send += new_clan.description
        await mchannel.send(to_send)


@coc_client.event
@coc.PlayerEvents.trophies()
@coc.PlayerEvents.versus_trophies()
async def player_trophy_change(old_player, new_player):
    if old_player.trophies != new_player.trophies:
        if old_player.trophies > new_player.trophies:
            to_send = "❕🏆⬇ {} has lost some trophies in the home base. Now has {}".format(new_player.name, new_player.trophies)
            print(to_send)
            await mchannel.send(to_send)
        else:
            to_send = "❕🏆⬆ {} has gained some trophies in the home base. Now has {}".format(new_player.name, new_player.trophies)
            print(to_send)
            await mchannel.send(to_send)
    if old_player.versus_trophies != new_player.versus_trophies:
        if old_player.versus_trophies > new_player.versus_trophies:
            to_send = "❕🏆⬇ {} has lost wasn't so lucky in a versus match in the builder base. Now has {} trophies".format(new_player.name, new_player.trophies)
            print(to_send)
            await mchannel.send(to_send)
        else:
            to_send = "❕🏆⬆ {} has won a versus match in the builder base. New trophy count:  {}. Player now has {} versus attack wins ".format(new_player.name, new_player.trophies, new_player.versus_attack_wins)
            print(to_send)
            await mchannel.send(to_send)

@bot.command()
async def watch_player(ctx, tag):
    p = await coc_client.get_player(tag)
    if p is not None:
        coc_client.add_player_updates(tag)
        await ctx.send("You will now receive updates regarding the specified player: {} ({})".format(p.name, tag))
    else:
        await ctx.send("No player found with the specified player tag: {}".format(tag))


@bot.command()
async def unwatch_player(ctx, tag):
    if coc_client.get_player(tag) is not None:
        p = await coc_client.get_player(tag)
        coc_client.remove_player_updates(tag)
        await ctx.send(
            "You will no longer receive updates regarding the specified player: {} ({})".format(p.name, tag))
    else:
        await ctx.send("No player found with the specified player tag: {}".format(tag))

bot.run(auth[3])
