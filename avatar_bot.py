import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # ignore the bot’s own messages
    if message.author == bot.user:
        return

    # check if message is a reply and contains the word "avatar"
    if message.reference and message.reference.resolved and "avatar" in message.content.lower():
        # get the message being replied to
        replied_message = message.reference.resolved
        user = replied_message.author

        # get avatar URL (static or animated)
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

        # send avatar embed
        embed = discord.Embed(
            title=f"{user.display_name}'s Avatar",
            color=discord.Color.blurple()
        )
        embed.set_image(url=avatar_url)
        await message.channel.send(embed=embed)

    # allow other commands to run
    await bot.process_commands(message)

import os
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)







