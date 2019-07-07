import discord

from settings import SECRET_TOKEN


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as : {} ({})'.format(client.user.name, client.user.id))


@client.event
async def on_message(message):
    if message.content.startswith('카린'):
        await message.channel.send('넵!')


if __name__ == '__main__':
    client.run(SECRET_TOKEN)
