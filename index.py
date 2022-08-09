#Importation
from datetime import datetime
from discord.ext import commands
import discord 
import typing
import guildWriter
import os
import checks
import json
import config



#Variables nécessaires globale
intents = discord.Intents.all()
helpCmd = commands.DefaultHelpCommand(no_category = "Catégories", 
    ending_note = "Pour avoir plus d'informations sur une commande/catégorie, faîtes \"!help <commande>\".\n\n\
                    Si cette commande possède elle-même des sous-commandes, pour avoir de l'aide sur comment l'utiliser, \
                    faîtes par exemple \"!help <commande> <sous-commande 1> <sous-commande 2 qui est dans sous-commande 1>\".")
bot = commands.Bot(command_prefix = "!", help_command = helpCmd, intents = intents)
excludesModules = ["membre", "modération"]

bot.check(commands.guild_only())


@bot.event
async def on_ready():
    for g in bot.guilds:
        guildWriter.dataGuild(g.id, bot)
    print(datetime.now())

#Lancement du bot
bot.run(config.token[0])

for i in os.listdir("./Commandes"):
    if ".py" in i and i[:-3] not in excludesModules:
        bot.load_extension("Commandes." + i[:-3])