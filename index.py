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
helpCmd = commands.DefaultHelpCommand(commands_heading = "Sous-commandes :", no_category = "Catégories")
bot = commands.Bot(command_prefix = "!", help_command = helpCmd, intents = intents)
excludesModules = ["membre", "modération", "valo"]


#Vérification que toutes les commandes soient dans des serveurs
bot.check(commands.guild_only())


@bot.event
async def on_ready():
    for g in bot.guilds:
        guildWriter.dataGuild(g.id, bot)
    print(datetime.now())


@bot.event
async def on_raw_reaction_add(rawReaction: discord.RawReactionActionEvent):
    if rawReaction.member.bot:
        return
    with open(os.path.abspath(os.path.dirname(__file__)) + "/guilds.json") as file:
        data = json.load(file)
        giveaway = [i for i in data[str(rawReaction.guild_id)]["giveaway"] if i["messageID"] == rawReaction.message_id]
        if len(giveaway) != 0:
            if giveaway[0]["reaction"][0] == rawReaction.emoji.name:
                userList = [u for u in giveaway[0]["participants"] if u == rawReaction.user_id]
                if len(userList) != 0:
                    return await rawReaction.member.send("Vous êtes déjà inscrit au giveaway \"" + giveaway[0]["nom"] + "\".")
                data[str(rawReaction.guild_id)]["giveaway"][data[str(rawReaction.guild_id)]["giveaway"].index(giveaway[0])]["participants"].append(rawReaction.user_id)
                await rawReaction.member.send("Vous êtes désormais inscrit au giveaway \"" + giveaway[0]["nom"] + "\".")
                with open(os.path.abspath(os.path.dirname(__file__)) + "/guilds.json", "w") as fileWritable:
                    fileWritable.write(json.dumps(data, indent = 4))



@bot.event
async def on_raw_reaction_remove(rawReaction: discord.RawReactionActionEvent):
    if bot.get_user(rawReaction.user_id).bot:
        return
    with open(os.path.abspath(os.path.dirname(__file__)) + "/guilds.json") as file:
        data = json.load(file)
        giveaway = [i for i in data[str(rawReaction.guild_id)]["giveaway"] if i["messageID"] == rawReaction.message_id]
        if len(giveaway) != 0:
            if giveaway[0]["reaction"][0] == rawReaction.emoji.name:
                userList = [u for u in giveaway[0]["participants"] if u == rawReaction.user_id]
                if len(userList) == 0:
                    return await bot.get_user(rawReaction.user_id).send("Vous êtes déjà désinscrit du giveaway \"" + giveaway[0]["nom"] + "\".")
                data[str(rawReaction.guild_id)]["giveaway"][data[str(rawReaction.guild_id)]["giveaway"].index(giveaway[0])]["participants"].pop(data[str(rawReaction.guild_id)]["giveaway"][data[str(rawReaction.guild_id)]["giveaway"].index(giveaway[0])]["participants"].index(rawReaction.user_id))
                await bot.get_user(rawReaction.user_id).send("Vous êtes désormais désinscrit du giveaway \"" + giveaway[0]["nom"] + "\".")
                with open(os.path.abspath(os.path.dirname(__file__)) + "/guilds.json", "w") as fileWritable:
                    fileWritable.write(json.dumps(data, indent = 4))



for i in os.listdir("./Commandes"):
    if ".py" in i and i[:-3] not in excludesModules:
        bot.load_extension("Commandes." + i[:-3])

#Lancement du bot
bot.run(config.token)