import discord
from discord import app_commands
from discord.ext import commands

class HelloWorld(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @app_commands.command(name="helloworld", description="HelloWorldコマンド")
    async def helloworld(self, interaction: discord.Interaction):
        await interaction.channel.send("HelloWorld")

async def setup(client: commands.Bot):
    await client.add_cog(HelloWorld(client))