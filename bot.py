import discord
import os
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تشغيل البوت: {bot.user}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def انقلع(ctx, member: discord.Member):
    await member.ban()
    await ctx.send(f"تم حظر {member.mention}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def برا(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(f"تم طرد {member.mention}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def سد_فمك(ctx, member: discord.Member):
    await member.timeout(timedelta(minutes=10))
    await ctx.send(f"تم إعطاء تايم أوت لـ {member.mention}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def إنذار(ctx, member: discord.Member):
    await ctx.send(f"⚠️ إنذار لـ {member.mention}")

bot.run(os.getenv("TOKEN"))

