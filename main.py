import discord
import os
from dotenv import load_dotenv
import random
import vrcpy
import json
import youtube_dl
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = int(os.getenv("DISCORD_GUILD"))
MODCHANNEL = int(os.getenv("MOD_CHANNEL"))
WELCOME = int(os.getenv("WELCOME_CHANNEL"))
VRC_USERNAME = os.getenv("VRC_USERNAME")
VRC_PASSWORD = os.getenv("VRC_PASSWORD")


offensive_words = [
    "slut",
    "nigger",
    "nigga",
    "faggot",
    "cunt",
    "queer",
    "binter",
    "pog"
]


vrc_client = vrcpy.Client()
vrc_client.login(VRC_USERNAME, VRC_PASSWORD)
intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix = '!', intents=intents)



@client.event
async def on_ready():
    global guild
    guild = client.get_guild(GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('VRChatting'))

@client.event
async def on_message(message):
    if message.author == client.user or message.guild is None or message.guild.id != GUILD:
        return
    is_badword = await on_badwords(message)
    if is_badword:
        return
    if message.content.startswith("echo"):
        await on_echo(message)
    await on_kawaii(message)
    if message.content.startswith("!q"):
        await on_questions(message)
    elif message.content.startswith("!link"):
        await on_link(message)
    elif message.content.startswith("!profile"):
        await on_profile(message)
    elif message.content.startswith("!join"):
        await join
    elif message.content.startswith("!play"):
        await play
    elif message.content.startswith("!leave"):
        await on_leave


async def on_catchup(message):
    message.
    dm_channel = message.author.dm_channel
    if dm_channel is None:
        dm_channel = await message.author.create_dm()
    mbed = discord.Embed(
        colour=(discord.Colour.red()),
        title='Welcome message!',
        description=f'Welcome {member.mention}, to the Canadian VRChat discord group 🍁 ! \n '
                    f'To ensure that you have a wonderful time,  Ill ask you to check out these few channels before starting: \n'
                    f' 1) #rules-info \n'
                    f' 2) #vrc-introduction \n'
                    f' 3) #events \n'
                    f' Once you checked out all of these go ahead and have fun OwO ill see you in VRChat!'
    )
    await dm_channel.send(mbed)




async def on_badwords(message):
    for word in offensive_words:
        if word in message.content.lower():
            await message.delete()
            dm_channel = message.author.dm_channel
            mod_channel = guild.get_channel(MODCHANNEL)
            if dm_channel is None:
                dm_channel = await message.author.create_dm()
            await dm_channel.send("Please refrain from using bad words :)")
            await mod_channel.send(f"{message.author.name} said the following in {message.channel.name} \n> {message.content}")
            return True
    return False


async def on_echo(message):
    txt = "\"message\""
    x = txt.split("\"")
    print(x)



async def on_kawaii(message):
    x = message.content.lower()
    if "uwu" in x and "owo" in x:
        if x.index("uwu") <  x.index("owo"):
            await message.channel.send("X3 nuzzles you~ \n you're so warm.")
        else:
            await message.channel.send("What's this?")
    elif "uwu" in x:
        await message.channel.send("X3 nuzzles you~ \n you're so warm.")
    elif "owo" in x:
        await message.channel.send("What's this?")



@client.event
async def on_member_join(member):
    mbed = discord.Embed(
        colour = (discord.Colour.red()),
        title = 'Welcome message!',
        description = f'Welcome {member.mention}, to the Canadian VRChat discord group 🍁 ! \n '
                      f'To ensure that you have a wonderful time,  Ill ask you to check out these few channels before starting: \n'
                      f' 1) #rules-info \n'
                      f' 2) #vrc-introduction \n'
                      f' 3) #events \n'
                      f' Once you checked out all of these go ahead and have fun OwO ill see you in VRChat!'
    )
    dm_channel = member.dm_channel
    if dm_channel is None:
        dm_channel = await member.create_dm()
    await dm_channel.send(embed=mbed)

    welcome_channel = guild.get_channel(WELCOME)
    await welcome_channel.send(f"Welcome <@{member.id}> to the Canadian VRChat discord group 🍁 ! You are the {member_number()} member!")


def member_number():
    number = str(len(guild.members))
    if number[-1] == "1":
        return number + "st"
    elif number[-1] == "2":
        return number + "nd"
    elif number[-1] == "3":
        return number + "rd"
    else:
        return number + "th"


async def on_questions(message):
    responses = ['Of course.',
                 'It is certain.',
                 'Yes, actually wait; no...',
                 'NOOOOOO.',
                 'I cannot predict now.',
                 'Yes.',
                 'Better not tell you now.',
                 'Very doubtful.',
                 'Dont count on it.',
                 'Ask the person who replies next.',
                 'Idk.',
                 'Yes, Binter is still banned.',
                 'Bot is offline, please try again later.',
                 "It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful.",
                 'No you.']
    await message.channel.send(random.choice(responses))


async def on_link(message):
    vrchat_id = message.content.split()[1]

    try:
        vrchat_user = vrc_client.fetch_user_by_id(vrchat_id)
    except vrcpy.errors.NotFoundError:
        await message.channel.send("The id provided is not valid, please make sure you typed your id correctly.")
        return

    discord_id = message.author.id
    dictionary_id = {discord_id:vrchat_id}

    with open("info.json","r+") as file:
        json_dict = json.load(file)
        json_dict.update(dictionary_id)
        file.seek(0)
        json.dump(json_dict, file)

    await message.channel.send(f"{message.author.mention} succesfully linked to **{vrchat_user.displayName}**")


async def on_profile(message):
    with open("info.json") as file:
        dict_user = json.load(file)
        vrchat_id = dict_user.get(str(message.author.id), "Notfound")

    if vrchat_id == "Notfound":
        await message.channel.send("Please link your id using the !link command")
        return

    vrchat_user = vrc_client.fetch_user_by_id(vrchat_id)


    vrc_mbed = discord.Embed(
        colour = (discord.Colour.magenta()),
        title = vrchat_user.displayName,
        description = vrchat_user.bio,
        url = f"https://vrchat.com/home/user/{vrchat_id}")

    vrc_mbed.set_thumbnail(url = vrchat_user.currentAvatarImageUrl)

    vrc_mbed.add_field(name="Description", value=str(vrchat_user.statusDescription), inline=False)

    await message.channel.send(embed=vrc_mbed)



players = {}


@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def on_leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

client.run(TOKEN)
