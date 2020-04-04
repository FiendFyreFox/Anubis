import discord
import random
import json
from discord.ext import commands, tasks
from itertools import cycle
import elo

client = commands.Bot(command_prefix = "!")
status = cycle(['Munching on crackers', 'Taking notes', 'Hacking the mainframe', 'Turning the knobs', 'Learning kung-fu'])

@client.event
async def on_ready():
    #id = client.get_guild(692428597951987813)
    change_status.start()
    #member = id.get_member_named('Nightmare')
    #channel = await member.create_dm()
    #await channel.send('What is happening?')
    print('Bot is ready.\n')

# --- JSON Management ---
@client.command()
async def register(ctx, user):
    with open('users.json', 'r') as f:
        users = json.load(f)
    if user == 0:
        await update_data(users, ctx.message.author)
    else:
        Guild = ctx.guild
        newUser = Guild.get_member_named(user)
        await update_data(users, newUser)
    #await change_elo(users, ctx.message.author, amount)
    #await level_up()

    with open('users.json', 'w') as f:
        json.dump(users, f)

@client.command()
async def game(ctx, P1Name, P2Name, outcome : float):
    with open('users.json', 'r') as f:
        users = json.load(f)
    try:
        Guild = ctx.guild
        Player1 = Guild.get_member_named(P1Name)
        Player2 = Guild.get_member_named(P2Name)
        await ctx.send(f'{Guild} | {Player1.id} | {Player2.id}')
        #if (users.count(Player1) < 1) or (users.count(Player2) < 1):
        #    await ctx.send('One or more of the provided players has not registered. Please do so before executing this command.')
        #else:
        try:
            print(f"Updating elo of {Player1}, who is at {users[str(Player1.id)]['rating']} and {Player2}, who is at {users[str(Player2.id)]['rating']}.")
        except:
            print('Unable to print the thing')
        
        newElos = elo.calcElo(int(users[str(Player1.id)]['rating']), int(users[str(Player2.id)]['rating']), outcome)
        print(newElos)
        users[str(Player1.id)]['rating'] = newElos[0]
        await level_up(users, Player1, ctx.channel, 0)
        
        users[str(Player2.id)]['rating'] = newElos[1]
        await level_up(users, Player2, ctx.channel, 0)
        try:
            await Player1.edit(nick = '[{}] {}'.format(users[str(Player1.id)]['rating'], Player1.name))
        except: 
            await ctx.send(f'I do not have permission to edit {Player1}\'s nickname')
        try: 
            await Player2.edit(nick = '[{}] {}'.format(users[str(Player2.id)]['rating'], Player2.name))
        except:
            await ctx.send(f'I do not have permission to edit {Player2}\'s nickname')
        await ctx.send(f'successfully updated elo of {Player1} and {Player2}.')
    except:
        await ctx.send('An error has occured.')

    with open('users.json', 'w') as f:
        json.dump(users, f)

    

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['rating'] = 0
        users[user.id]['level'] = 1

@client.command()
async def name(ctx, arg):
    user = ctx.message.author
    await user.edit(nick = arg)

@client.command(aliases = ['changeElo'])
async def change_elo(ctx, amount : int):
    with open('users.json', 'r') as f:
        users = json.load(f)
    user = str(ctx.message.author.id)
    points = int(amount)
    print(f"changing elo of {ctx.message.author.id} by {amount}. It is currently {users[user]['rating']}")
    users[user]['rating'] += points
    print('boop')
    await level_up(users, ctx.message.author, ctx.channel, points)

    with open('users.json', 'w') as f:
        print('dumping')
        json.dump(users, f)

async def level_up(users, user, channel, amount):
    id = str(user.id)
    #trueUser = user.id
    print(f"Updating level of user {user}. It is currently {users[id]['level']}")
    rating = (users[id]['rating'] + amount)
    lvl_start = users[id]['level']
    lvl_end = int(rating ** (1/4))

    if lvl_start < lvl_end:
        print('Leveling up')
        try:
            await user.edit(nick = '[{}] {}'.format(users[id]['rating'], user.name))
        except:
            pass
        #.format(str(lvl_end))
        users[id]['level'] = lvl_end
    else:
        print('Level up was uneccessary')

@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_member_join(member):
    print(f'Wow! {member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'Oh dear, {member} has left a server.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'The command \"{ctx.command}\" requires a specific number of parameters. Please specify all of them.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms \n monkey says:{ctx.channel}')
    await ctx.send((elo.calcElo(1500, 200, 1)))

@client.command()
async def setmessagelocation(ctx, arg):
    arg.replace('#', "")
    print('boop')
    id = ctx.guild
    #client.get_guild(692428597951987813)
    channel = discord.utils.get(id.text_channels, name = arg)
    print(arg.replace("#", ""))
    await channel.send('hello')

@client.command()
async def polly(ctx, arg):
    await ctx.send(arg)

@client.command()
async def senddm(ctx, arg):
    str(arg)
    arg.replace('@', '')
    print(arg)
    Guild = ctx.guild
    user = Guild.get_member_named(arg)
    if user == 'None':
        await ctx.send(f'No user named {arg} was found. Please try again.')
    else:
        print(user)
        await user.send('This is a wonderful message, sent directly to you through the Discord ether.')

@client.command(aliases = ['8ball', 'fortune'])
async def _8ball(ctx):
    responses = ['As I see it, yes.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                'Don’t count on it.',
                'It is certain.',
                'It is decidedly so.',
                'Most likely.',
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Outlook good.',
                'Reply hazy, try again.',
                'Signs point to yes.',
                'Very doubtful.',
                'Without a doubt.',
                'Yes.',
                'Yes – definitely.',
                'You may rely on it.'
                ]
    await ctx.send(random.choice(responses))

# --- ADMIN COMMANDS ---

@client.command()
@commands.has_role('Administrator')
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

@client.command()
@commands.has_role('Administrator')
async def setelo(ctx, player, amount : int):
    with open('users.json', 'r') as f:
        users = json.load(f)

    Guild = ctx.guild
    user = Guild.get_member_named(player)
    if str(user.id) in users:
        users[str(user.id)]['rating'] = amount
        await level_up(users, user, ctx.channel, 0)
        await user.edit(nick = '[{}] {}'.format(users[str(user.id)]['rating'], user.name))
        await ctx.send(f'Successfully set elo of {user} to {amount}')
    else:
        await ctx.send('That user is not registered.')

    with open('users.json', 'w') as f:
        json.dump(users, f)
    
# --------


@client.command()
async def banana(ctx):
    author = ctx.message.author
    await author.send('Don\'t say that!!!!!!!')

@client.command()
async def hpy_elo(ctx, R1, R2, Scr):
    Rating1 = int(R1)
    Rating2 = int(R2)
    Score = float(Scr)
    await ctx.send(f'Calculating... {Rating1}, {Rating2}, {Score}')
    results = elo.calcElo(Rating1, Rating2, Score)
    if (Score == 1):
        await ctx.send(f'Player 1 won, and their elo increased from {Rating1} to {results[0]}. \nPlayer 2 lost, and their elo decreased from {Rating2} to {results[1]}.')
    elif (Score == 0):
         await ctx.send(f'Player 2 won, and their elo increased from {Rating2} to {results[1]}. \nPlayer 1 lost, and their elo decreased from {Rating1} to {results[0]}.')
    elif (Score == 0.5):
         await ctx.send(f'The game ended in a draw. Player 1\'s elo changed from {Rating1} to {results[0]}, \nwhile Player 2\'s elo changed from {Rating2} to {results[1]}.')
    else:
         await ctx.send('something is wrong.')
    
    #await ctx.send(results)





client.run('NjkyNDM0NzUyMDQ4OTg4MTkw.XoPYxw.eux-cgfqQMVY0dxtfAyeHtcIX8Q')