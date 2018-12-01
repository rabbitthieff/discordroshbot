import asyncio
import datetime
import random
import time
from itertools import cycle
from random import randint

import discord
from discord.ext import commands

TOKEN = 'NTEwMTUyNzM4OTUzMjMyMzk1.DscaPw.MO3lREq9-fdSUWohpzYDxIVggTc'

client = commands.Bot(command_prefix='rosh ')
client.remove_command('help')

# custom bot status messages-----------------------------------------
status = ['Wazzzzzuppp', 'Lets dotes?', 'Cheese any 1?']


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(5)  # sleep timer before changing status


@client.event
async def on_ready():
    # await client.change_presence(game=discord.Game(name='Rosh'))
    print('Rosh is up!')


@client.command()
async def logout():
    await client.logout()


@client.command()
async def ping():
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = time.time() - pingtime
    await client.say(pingms, ":ping_pong:  time is `%.01f seconds`" % ping)


@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


# clear text-----------------------------------------------------
@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted!')


# nuke text-----------------------------------------------------
@client.command(pass_context=True)
async def nuke(ctx, amount=100):
    amount = int(amount)
    channel = ctx.message.channel
    counter = 0
    async for x in client.logs_from(ctx.message.channel, limit=amount):
        if counter < amount:
            await client.delete_message(x)
            counter += 1
            await asyncio.sleep(0.1)
    await client.say('You asked for a nuke we gave u a nuke!')


# custom formatting--------------------------------------------
@client.command()
async def displayembed():
    embed = discord.Embed(
        title='Title',
        description='This is a description.',
        colour=discord.Colour.blue()
    )
    embed.set_footer(text='This is a footer.')
    embed.set_image(
        url='https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/thumb/6/6e/Roshan_model.png/250px-Roshan_model.png'
            '?version=e75b27f61eb357ae3462a31bdcfd48dd')
    embed.set_thumbnail(
        url='https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/thumb/6/6e/Roshan_model.png/250px-Roshan_model.png'
            '?version=e75b27f61eb357ae3462a31bdcfd48dd')
    embed.set_author(name='Aurthor name',
                     icon_url='https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/thumb/6/6e/Roshan_model.png'
                              '/250px-Roshan_model.png?version=e75b27f61eb357ae3462a31bdcfd48dd')
    embed.add_field(name='Feild name', value='Feild Value', inline=True)

    await client.say(embed=embed)


# --------------------------------------------------------------------------------------------

# help commands-------------------------------------------------------------------------------
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed.set_author(name='Roshan',
                     icon_url='https://d1u5p3l4wpay3k.cloudfront.net/dota2_gamepedia/thumb/6/6e/Roshan_model.png/250px-Roshan_model.png?version=e75b27f61eb357ae3462a31bdcfd48dd')
    embed.add_field(name='rosh', value='is the key phrase that you should type before a command ex. rosh ping',
                    inline=False)
    embed.add_field(name='help', value='displays commands', inline=False)
    embed.add_field(name='echo', value='repeat the shit u said', inline=False)
    embed.add_field(name='roll',
                    value='roll a 6 sided die 1 time, input numbers after roll for sides and number of rolls',
                    inline=False)
    embed.add_field(name='flip', value='flips a coin', inline=False)
    embed.add_field(name='clear', value='clears most recent chats (less than 14 days)', inline=False)
    embed.add_field(name='nuke', value='clears the shit outta your chats', inline=False)
    embed.add_field(name='join', value='join the voice channel', inline=False)
    embed.add_field(name='leave', value='what do you think?', inline=False)
    embed.add_field(name='serverinfo', value='Shows how shit your server is', inline=False)
    embed.add_field(name='ping', value='show sucky your net is', inline=False)
    embed.add_field(name='poll', value='so you type poll <title> <game1> <game2>, final results can be gotten by the command tally <poll id>', inline=False)
    embed.add_field(name='time', value='Current times at ur pit', inline=False)

    await client.send_message(author, embed=embed)
    await client.say("HA noob asking for help :wink:", embed=embed)


# join and leave--------------------------------------------------------------------------------------------
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


# dice roll-----------------------------------------------------------
@client.command(name='roll')
async def roll_command(sides=6, num=1):
    """Roll dice
    :param sides: Number of sides to the dice
    :param num: Number of rolls to make
    """
    try:
        int(sides)
    except ValueError:
        await client.say("Invalid Value in arguments.")
        return
    if num > 20:
        await client.say("20 is the max number of rolls at once that I "
                         "will handle!")
        return
    rolls = []
    for i in range(num):
        rolls.append(randint(1, int(sides)))
    await client.say(
        "Your dice with {0} sides and {1} rolls are: {2} Next time get your own bloody dice!!".format(sides, num,
                                                                                                      rolls))


# server info----------------------------------------------------------

@client.command(pass_context=True)
async def serverinfo(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50:  # Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles' % len(roles))

    roles = ', '.join(roles)
    channelz = len(server.channels)
    time = str(server.created_at)
    time = time.split(' ')
    time = time[0]

    join = discord.Embed(description='%s ' % (str(server)), title='Server Name', colour=0xFFFF)
    join.set_thumbnail(url=server.icon_url)
    join.add_field(name='__Owner__', value=str(server.owner) + '\n' + server.owner.id)
    join.add_field(name='__ID__', value=str(server.id))
    join.add_field(name='__Member Count__', value=str(server.member_count))
    join.add_field(name='__Text/Voice Channels__', value=str(channelz))
    join.add_field(name='__Roles (%s)__' % str(role_length), value=roles)
    join.set_footer(text='Created: %s' % time)

    return await client.say(embed=join)


# -----------------------------------------------------------
@client.command()
async def flip():
    await client.say('Rosh flips ' + random.choice(['Heads', 'Tails.']))


# poll-----------------------------------------------------------

@client.command(pass_context=True)
async def poll(ctx, question, *options: str):
    if len(options) <= 1:
        await client.say('You need more than one option to make a poll!')
        return
    if len(options) > 10:
        await client.say('You cannot make a poll for more than 10 things!')
        return
    if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
        reactions = ['✅', '❌']
    else:
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)
    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await client.say(embed=embed)
    for reaction in reactions[:len(options)]:
        await client.add_reaction(react_message, reaction)
    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await client.edit_message(react_message, embed=embed)


@client.command(pass_context=True)
async def tally(ctx, id):
    poll_message = await client.get_message(ctx.message.channel, id)
    if not poll_message.embeds:
        return
    embed = poll_message.embeds[0]
    if poll_message.author != ctx.message.server.me:
        return
    if not embed['footer']['text'].startswith('Poll ID:'):
        return
    unformatted_options = [x.strip() for x in embed['description'].split('\n')]
    opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
        else {x[:1]: x[2:] for x in unformatted_options}
    # check if we're using numbers for the poll, or x/checkmark, parse accordingly
    voters = [ctx.message.server.me.id]  # add the bot's ID to the list of voters to exclude it's votes

    tally = {x: 0 for x in opt_dict.keys()}
    for reaction in poll_message.reactions:
        if reaction.emoji in opt_dict.keys():
            reactors = await client.get_reaction_users(reaction)
            for reactor in reactors:
                if reactor.id not in voters:
                    tally[reaction.emoji] += 1
                    voters.append(reactor.id)

    output = 'Results of the poll for "{}":\n'.format(embed['title']) + \
             '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
    await client.say(output)
# -------------------------------------------------
@client.command()
async def time():

    # UTC
    tmp1 = datetime.datetime.now()
    utcnow = datetime.time(hour=tmp1.hour, minute=tmp1.minute, second=tmp1.second)
    del tmp1
    utcfulltime = "{}:{}:{}".format(utcnow.hour, utcnow.minute, utcnow.second)

    hour = utcnow.hour 
    minu = utcnow.minute
    sec = utcnow.second
    #bahrain time
    bhour = hour
    bminu = minu
    bsec = sec
    #london
    lhour = hour
    lminu = minu
    lsec = sec
    
    if hour < 12:
        srilanka = ("{}:{}:{} AM".format(hour, minu, sec))
        bahrain = ("{}:{}:{} AM".format(bhour, bminu, bsec))
        london = ("{}:{}:{} AM".format(lhour, lminu, lsec))
        await client.say("```Sri Lanka : {}\nBahrain : {}\nLondon : {}```".format(srilanka, bahrain, london))
    else:
        hour = hour - 12
        bhour = hour - 2
        lhour = hour - 5
        if hour < 5:
            lhour = hour + 7
        if minu > 30:
            bminu = minu - 30
            lminu = lminu - 30
        else:
            bminu = minu + 30
            bhour = bhour - 1
            if bminu == 60:
                bhour = bhour + 1
                bminu = 00
            else:
                lminu = lminu + 30

        srilanka = ("{}:{}:{} PM".format(hour, minu, sec))
        bahrain = ("{}:{}:{} PM".format(bhour, bminu, bsec))
        if minu > 30:
            lminu = minu - 30
        else:
            lminu = minu + 30
            lhour = lhour - 1
        if lhour == 0:
            lhour = 12
        london = ("{}:{}:{} PM".format(lhour, lminu, lsec))
        await client.say("```\nSri Lanka : {}\nBahrain : {}\nLondon : {}```".format(srilanka, bahrain, london))
    # cleaning up
    del utcnow
    del bhour
    del hour
    del lhour
    del minu
    del bminu
    del lminu
    del sec
    del bsec
    del lsec
    del srilanka
    del bahrain
    del london

#--------------------------------------------------

client.loop.create_task(change_status())
client.run(TOKEN)
