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


def special_command(message):

    response = ''

    if getcommandgroup(message) == 'whatcanyoudo':
        response = 'I understand these commands: \n'
        for command in commands:
            for ver in command:
                if ver != command[0]:
                    response += '!' + ver + '\n'

    if getcommandgroup(message) == 'greeting':
        for response in responses:
            if response[0] == 'greeting':
                return response[random.randrange(1, len(response))] + ' ' + message.author.name + ' !'

    if getcommandgroup(message) == 'newcommand':
        stage = 0
        commandlist = []
        responselist = []
        index = message.content.index('[') + 1
        while True:

            while message.content[index] != ']':
                temp = ''

                while (message.content[index] != ',') and (message.content[index] != ']'):
                    temp += message.content[index]
                    index += 1

                if stage == 0:
                    commandlist.append(temp)
                    responselist.append(temp)
                    break
                elif stage == 1:
                    commandlist.append(temp)
                elif stage == 2:
                    responselist.append(temp)

                if (index == len(message.content)) or (message.content[index] == ']'):
                    break

                index += 1

            try:
                index = message.content.index('[', (index + 1)) + 1
            except:
                break

            stage += 1

        commands.append(commandlist)
        responses.append(responselist)
        return 'Got it'

    return response


def getcommandgroup(message):
    commandgroup = 'unknown'
    for command in commands:
        for ver in command:
            if message.content.startswith(ver):
                commandgroup = command[0]
    return commandgroup


@client.event
async def on_message(message):

    channel = message.channel

    if message.author == client.user or message.content[0] != '!':
        return

    message.content = message.content[1::]

    if special_command(message) != '':
        await client.send_message(channel, special_command(message))
        return

    commandgroup = getcommandgroup(message)

    if commandgroup == 'unknown':
        await client.send_message(channel, 'just read the help page for god\'s sake I\'m begging you')

    for response in responses:
        if response[0] == commandgroup:
            await client.send_message(channel, response[random.randrange(1, len(response))])
            return


@client.event
async def on_ready():
    print()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)

parse_xml()

client.run(TOKEN)
