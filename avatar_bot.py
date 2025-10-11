import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "Avatar Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

auto_reply_enabled = True  

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    """Manual command for avatars"""
    member = member or ctx.author
    await ctx.send(member.avatar.url)

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return

    if message.reference and message.content.lower().strip() == "avatar":
        try:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            user = ref_msg.author
            await message.channel.send(user.avatar.url)
        except Exception as e:
            print(f"⚠️ Error sending avatar: {e}")

    await bot.process_commands(message)

keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)


