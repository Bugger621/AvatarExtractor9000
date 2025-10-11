import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- Flask keep-alive server ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Avatar Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Discord bot setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == bot.user:
        return

    # Check if the message is a reply and contains "avatar"
    if message.reference and "avatar" in message.content.lower():
        try:
            # Safely fetch the replied-to message (works even if not cached)
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            user = replied_message.author

            avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

            embed = discord.Embed(
                title=f"{user.display_name}'s Avatar",
                color=discord.Color.blurple()
            )
            embed.set_image(url=avatar_url)
            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"⚠️ Error fetching message or sending avatar: {e}")

    await bot.process_commands(message)

# --- Keep alive and run the bot ---
keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")  # Make sure this is set in Render's environment
bot.run(TOKEN)




