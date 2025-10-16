import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# --- Flask keep-alive server ---
app = Flask('')

@app.route('/')
def home():
    return "Avatar Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


# --- Discord bot setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

auto_reply_enabled = False


# --- On ready event ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


# --- Command: toggle auto reply ---
@bot.command()
async def toggle(ctx):
    """Toggles the automatic avatar reply feature."""
    global auto_reply_enabled
    auto_reply_enabled = not auto_reply_enabled
    status = "enabled ✅" if auto_reply_enabled else "disabled ❌"
    await ctx.send(f"Avatar auto-reply has been {status}.")


# --- Command: manual avatar lookup ---
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    """Manually get a user's avatar."""
    member = member or ctx.author
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=discord.Color.blue())
    embed.set_image(url=avatar_url)
    await ctx.send(embed=embed)


# --- Auto reply on message ---
@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Debug log
    print(f"[DEBUG] Message from {message.author}: {message.content} | Ref: {message.reference}")

    # Only reply if message is replying to someone and contains "avatar"
    if message.reference and "avatar" in message.content.lower():
        try:
            ref = message.reference

            # Try to get the original message that was replied to
            if ref.resolved:
                replied_user = ref.resolved.author
            else:
                replied_msg = await message.channel.fetch_message(ref.message_id)
                replied_user = replied_msg.author

            # Get avatar
            avatar_url = replied_user.avatar.url if replied_user.avatar else replied_user.default_avatar.url

            # Send embed with avatar
            embed = discord.Embed(title=f"{replied_user.display_name}'s Avatar", color=discord.Color.blue())
            embed.set_image(url=avatar_url)
            await message.channel.send(embed=embed)

            print(f"[DEBUG] Sent avatar for {replied_user.display_name}")

        except Exception as e:
            print(f"⚠️ Error fetching avatar: {e}")

    await bot.process_commands(message)


# --- Start bot ---
keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)








