import json
import os
import sys

import discord
from discord.ext import commands
from discord import app_commands
import asyncio

filename = "data.json"
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

if not os.path.exists(filename) or os.path.getsize(filename) == 0:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"bot_token": "" }, f, ensure_ascii=False, indent=4)
        print(f"{filename} を新しく作成しました。")

with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

if not data["bot_token"]:
    print("Tokenが設定されていません")
    sys.exit(0)

@client.event
async def on_ready():
    print("ログインしました")
    await client.tree.sync()

async def main():
    await client.load_extension("mochineko.discord_bot.command.TestCommand")
    await client.start(data["bot_token"])

if __name__ == "__main__":
    asyncio.run(main())