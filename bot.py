import os
import re
from datetime import timedelta

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="", intents=intents)


@bot.event
async def on_ready():
    print(f"تم تشغيل البوت: {bot.user}")


@bot.command(name="انقلع")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member):
    await member.ban()
    await ctx.send(f"🔨 {member.mention} انحظر من السيرفر.")


@bot.command(name="برا")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(f"👢 {member.mention} انطرد من السيرفر.")


@bot.command(name="سد حلقك")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration="10m"):
    match = re.fullmatch(r"(\d+)([smhd])", duration.lower())

    if not match:
        await ctx.send("❌ استخدم مدة مثل: 10m أو 1h أو 1d")
        return

    amount = int(match.group(1))
    unit = match.group(2)

    multipliers = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400
    }

    seconds = amount * multipliers[unit]

    if seconds > 28 * 86400:
        await ctx.send("❌ أقصى مدة للتايم أوت هي 28 يوم.")
        return

    await member.timeout(
        timedelta(seconds=seconds),
        reason=f"تايم أوت بواسطة {ctx.author}"
    )

    await ctx.send(
        f"🔇 {member.mention} أخذ تايم أوت لمدة {duration}."
    )


@bot.command(name="تحذير")
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member):
    await ctx.send(f"⚠️ {member.mention} أخذ تحذير.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ ما عندك الصلاحية لهذا الأمر.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ ما لقيت هذا العضو.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ لازم تحدد العضو.")


TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN غير موجود في GitHub Secrets")

bot.run(TOKEN)
