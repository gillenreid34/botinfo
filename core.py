import random

import discord
import xml.etree.cElementTree as ET

TOKEN = 'NTEyNjgyMjU4NDU3NDI3OTc5.Ds9BEw.3a-VXDubmMjtSLRwrY4MuzTjt1E'

client = discord.Client()

commands = []
responses = []


def parse_xml():
    tree = ET.parse('knowledge.xml')
    root = tree.getroot()

    for item in root.findall('./cmdgroup'):
        command = [item.attrib['id']]
        for child in item:
            command.append(child.text)
            print('imported command ( ' + command[0] + ' ) : ' + child.text)
        commands.append(command)

    for item in root.findall('./rpnsgroup'):
        response = [item.attrib['id']]
        for child in item:
            response.append(child.text)
            print('imported response ( ' + response[0] + ' ) : ' + child.text)
        responses.append(response)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message.content = message.content[1::]

    for command in commands:
        for ver in command:
            if message.content == ver:
                for response in responses:
                    if response[0] == command[0]:
                        await client.send_message(message.channel, response[random.randrange(1, len(response))])


@client.event
async def on_ready():
    print()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)

parse_xml()

client.run(TOKEN)
