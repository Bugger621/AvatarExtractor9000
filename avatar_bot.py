import discord
import os
from flask import Flask
from threading import Thread

# --- Flask keep-alive server for UptimeRobot ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# --- Discord bot setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Check if it's a reply with "avatar"
    if message.reference and message.content.lower().strip() == "avatar":
        try:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            target_user = replied_message.author

            embed = discord.Embed(
                title=f"{target_user.name}'s Avatar",
                color=discord.Color.blue()
            )
            embed.set_image(url=target_user.avatar.url if target_user.avatar else target_user.default_avatar.url)

            await message.reply(embed=embed)
        except Exception as e:
            print(f"⚠️ Error fetching replied message: {e}")

# --- Run everything ---
if __name__ == "__main__":
    keep_alive()  # Start Flask server for uptime pings

    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("❌ ERROR: DISCORD_TOKEN environment variable not found!")
    else:
        print("🚀 Starting Discord bot...")
        bot.run(TOKEN)








