import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    sworeAnswer = [
        'no fuck you',
        'oh no thats a swore!',
        (
            'swear bad we dont do that here.'
        ),
    ]

    if message.content == 'fuck':
        response = random.choice(sworeAnswer)
        await message.channel.send(response)

client.run(TOKEN)
