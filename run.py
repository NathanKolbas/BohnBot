from create_gif import CreateGif, Gifs
import discord
import json
from run_helper import *

with open('config.json') as f:
    config = json.load(f)

TOKEN = config['BOT_TOKEN']

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.lower().startswith('bohnbot ') or client.user in message.mentions:
        helper = Helper(message.author)
        commands = message.content.split(' ', 2)
        del commands[0]
        if commands[0].lower() == 'execute':
            helper.increment_count()
            argument_data = commands[1]
            if message.mentions:
                mentioned_user = message.mentions[0]
                argument_data = mentioned_user.avatar_url

            file = CreateGif(argument_data).generate_gif(Gifs.AMONG_US_KILL)
            msg = f"Bohn has executed {commands[1]}"
            await message.channel.send(msg, file=discord.File(file.name, 'hello_is_anyone_there.gif'))
            # Close and delete the temp file
            file.close()
            os.unlink(file.name)
        elif commands[0].lower() in ['kd', 'kills', 'executions', 'kill-count']:
            kills = helper.get_count()
            msg = f"My current {commands[0]} is {kills} and I do not plan to stop."
            await message.channel.send(msg)
        elif commands[0].lower() in ['smash', 'challenger']:
            argument_data = commands[1]
            if message.mentions:
                mentioned_user = message.mentions[0]
                argument_data = mentioned_user.avatar_url

            file = CreateGif(argument_data).generate_gif(Gifs.CHALLENGER)
            msg = f"You dare to challenge me {commands[1]}?"
            await message.channel.send(msg, file=discord.File(file.name, 'please_send_help.gif'))
            # Close and delete the temp file
            file.close()
            os.unlink(file.name)
        elif commands[0].lower() == 'quote':
            del commands[0]
            if len(commands) > 0:
                line = int(commands[0])
                quotes = helper.get_quotes()
                if 0 < line <= len(quotes):
                    msg = quotes[line - 1]
                else:
                    msg = f"A quote at line {line} does not exist."
            else:
                msg = helper.random_quote()
            await message.channel.send(msg)
        elif commands[0].lower() == 'quote-all':
            msg = helper.show_all_quotes()
            # Messages can only be 2k in length. This will split the messages.
            while len(msg) > 0:
                await message.channel.send(msg[0:1999])
                msg = msg[1999:]
        elif commands[0].lower() == 'add':
            del commands[0]
            add_commands = commands[0].split(' ', 1)
            if add_commands[0].lower() == 'quote':
                argument_data = add_commands[1]
                line = helper.add_quote(argument_data)
                msg = f"The new quote was added at line {line}"
                await message.channel.send(msg)
        elif commands[0].lower() == 'remove-quote':
            del commands[0]
            if message.author.guild_permissions.administrator:
                line = int(commands[0])
                if 0 < line <= len(helper.get_quotes()):
                    helper.remove_quote(line)
                    msg = f"Successfully removed quote on line {line}."
                else:
                    msg = f"A quote at line {line} does not exist."
            else:
                msg = 'You do not have the permissions to delete a quote (Administrator permission needed).'
            await message.channel.send(msg)
        elif message.content[-1] == '?':
            msg = helper.random_quote()
            await message.channel.send(msg)
        elif commands[0].lower() == 'stretch-break':
            msg = ":rotating_light: Stretch Break :rotating_light:"
            file = helper.random_stretch_break()
            await message.channel.send(msg, file=discord.File(file, 'can_anyone_hear_me.gif'))
        elif commands[0].lower() == 'markov':
            msg = helper.markov()
            await message.channel.send(msg)
        elif commands[0].lower() == 'new':
            msg = """ 
New features/improvements/commands:\n
• BohnBot has been released into the wild.
"""
            await message.channel.send(msg)
        elif commands[0].lower() == 'help':
            msg = """ 
The current available BohnBot commands are:\n
• `BohnBot execute @UserName`
    - Creates a gif of that user getting killed in Among Us
    - Use the users @ in the command to use their icon in the gif
    - Type any text after to search for an image\n
• `BohnBot kd|kills|executions|kill-count`
    - Tells you how many people Bohn has executed\n
• `BohnBot smash|challenger @UserName`
    - Creates a gif of that user getting introduced in smash
    - Use the users @ in the command to use their icon in the gif
    - Type any text after to search for an image\n
• `BohnBot quote`
    - Sends a random quote from Bohn
    - Optionally you can specify the line of the quote (e.g. `BohnBot quote 1`)\n
• `BohnBot quote-all`
    - Shows all the quotes\n
• `BohnBot add quote the_quote_you_would_like_to_add`
    - Adds a new quote into Bohn's endless knowledge\n
• `BohnBot remove-quote quote_line`
    - Removes a quote by the line. Requires Administrator permission to do so.\n
• `BohnBot markov`
    - Creates a Markov chain using the quotes added to the BohnBot\n
• `BohnBot stretch-break`
    - Starts a stretch break\n
• `BohnBot quine`
    - One of Bohn's favorite puzzles\n
• `BohnBot new`
    - Tells you about what is new, features, improvements, and/or commands for the most recent update\n
Created by: Nathan Kolbas - <https://github.com/NathanKolbas/BohnBot>
"""
            await message.channel.send(msg)
        elif commands[0].lower() == 'quine':
            files = helper.quine()
            for file in files:
                await message.channel.send(file)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
