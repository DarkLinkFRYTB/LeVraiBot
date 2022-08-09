#Importations
from copy import deepcopy
import json
import random
from discord.ext import commands
import discord
import valorant
import checks
import os
import guildWriter



#Variables nécessaires
import config
valoClient = 'valorant.Client(config.RiotAPIKey, "fr-FR", "eu", "europe")'


#Groupe général
@commands.group(name = "valorant", aliases = ["valo"])
@commands.check(lambda ctx: checks.hasRolePerm(ctx, ctx.guild.id, ctx.author.id, "Valorant"))
async def valoGroup(ctx: commands.Context):
    """Commandes pour les joueurs de Valorant"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(valoGroup)


@commands.command(name = "link", aliases = ["l"])
async def linkCmdValo(ctx: commands.Context, compte: str, serveur = "europe"):
    """Permet de lier son compte valo à celui de Discord, le serveur est optionnel (par défaut équivalent à europe)"""
    #Vérifie que le serveur est valide
    if serveur not in ["europe", "americas", "asia", "esports"]:
        return await ctx.reply("Serveur invalide, il doit être un de ceux-là : europe, americas, asia, esports")
    account = valoClient.get_user_by_name(compte, serveur)
    #Vérifie l'existence du compte
    if not account:
        return await ctx.reply("Compte introuvable")
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        membre = [i for g in data for i in data[g]["membres"] if i["ID"] == ctx.author.id]
        #Remplace chaque occurence du membre si il est dans plusieurs serveurs
        for instance in membre:
            instance["Compte riot"] = account.puuid
        await ctx.reply("Votre compte riot lié est désormais <" + account.gameName + ">.")
        #Réécrit le fichier
        with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json", "w") as fileWritable:
            fileWritable.write(json.dumps(data, indent = 4))


@commands.group(name = "practice", aliases = ["prac", "p"])
async def practiceGroupValo(ctx: commands.Context):
    """Commandes en rapport avec les practices du jeu et leur organisation"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(practiceGroupValo)


@commands.command(name = "create", aliases = ["c", "+"])
@commands.check_any(commands.check(
    lambda ctx: checks.hasRolePerm(ctx, ctx.guild.id, ctx.author.id, "Staff", "Coach", "Admin")
))
async def createCmdPrac(ctx: commands.Context):
    channel = await ctx.guild.create_channel(name = "Création practice")
    await channel.send("D'accord, procédons à la création de la practice (pas besoin de commande, répondez juste avec le format indiqué entre guillemets)")
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        rangs = ""
        await channel.send("Quels sont les rangs acceptés dans la practice ? (noms en français : \"Argent Or Platine\", vous devez indiquer tout les rangs)")
        while not rangs:
            try:
                message = await ctx.bot.wait_for("message", timeout = 60, check = lambda msg: msg.author == ctx.author)
                args = message.split()
                if len(args) == 0:
                    continue
                for rang in args:
                    if not rang.lower() in ["bronze", "argent", "or", "platine", "diamant", "ascendant", "immortel", "radiant"]:
                        message.reply("Au moins un rang donné est invalide, réessayez")
                        continue
                    args[args.index(rang)] = rang.lower()
                args.sort()
                rangs = " ".join(args)
            except:
                await channel.send("Temps écoulé, la practice n'a pas été créée", delete_after = 5)
                await channel.delete()
                return
        date = ""
        await channel.send("Quels est la date et l'heure de la practice ? (Au format : \"JJ/MM HH:MM\", avec JJ pour le jour, les 2 premiers M pour le mois, HH pour l'heure et les 2 derniers M pour les minutes)")
        while not date:
            try:
                message = await ctx.bot.wait_for("message", timeout = 60, check = lambda msg: msg.author == ctx.author)
                args = message.split()
                if not checks.isValidDate(" ".join(args), '%d/%m %H:%M'):
                    await ctx.send("Format de la date invalide, envoyez-bien uniquement la date et l'heure au format demandé")
                    continue
                date = " ".join(args)
            except:
                await channel.send("Temps écoulé, la practice n'a pas été créée", delete_after = 5)
                await channel.delete()
                return

        id = random.randint(1111, 9999)
        while len([i for i in data[str(ctx.guild.id)]["practices"] if i["ID"] == id]) != 0:
            id = random.randint(1111, 9999)
        temp = deepcopy(guildWriter.modele["practices"][0])
        temp["ID"] = id
        temp["joueurs"] = []
        temp["date"] = date
        temp["host"] = ctx.author.id
        temp["rangs"] = rangs
        data[str(ctx.guild.id)]["practices"].append(temp)
        del temp

#Ajout des groupes aux catégories


#Ajout des commandes aux catégories
valoGroup.add_command(linkCmdValo)




#Commande setup pour l'importation du module
def setup(bot: commands.Bot):
    """Rajoute la catégorie Valorant au bot"""
    bot.add_command(valoGroup)