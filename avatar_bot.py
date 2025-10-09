import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online! Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

  
    if (
        message.reference
        and message.reference.resolved
        and "avatar" in message.content.lower()
    ):
        original_message = message.reference.resolved
        target_user = original_message.author
        avatar_url = target_user.display_avatar.url

        await message.channel.send(
            f"🖼️ {target_user.name}'s avatar:\n{avatar_url}"
        )

  
    await bot.process_commands(message)

bot.run("MTM4ODI2MTgwNTY0NTYyNzQ0Mg.G444pA.qurBZIaP64unHG94lNqMK21Ls_nblW5CGZMu5Q")