
import discord

TOKEN = 'NTEyNjgyMjU4NDU3NDI3OTc5.Ds9BEw.3a-VXDubmMjtSLRwrY4MuzTjt1E'

client = discord.Client()



@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    client.co

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hey {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content == '!Where am I?':
        msg = 'Idk, {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)