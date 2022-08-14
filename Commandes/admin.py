#Importations
from copy import deepcopy
import json
import random
import sys
import typing
from discord.ext import commands
import discord
import checks
import os
from guildWriter import dataGuild, modele
import emoji
import config


#Groupe général
@commands.group(name = "administrateur", aliases = ["admin", "ad", "a"])
@commands.check_any(
    commands.check(lambda ctx: ctx.author.guild_permissions.administrator),
    commands.check(lambda ctx: checks.hasRolePerm(ctx, ctx.guild.id, ctx.author.id, "Admin"))
)
async def administrateurGroup(ctx: commands.Context):
    """Commandes réservées aux administrateurs"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(administrateurGroup)



#Modification des rôles
@commands.group(name = "rôles", aliases = ["r"])
async def rôlesGroupAdministrateur(ctx: commands.Context):
    """Commandes des rôles de permission du serveur"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(rôlesGroupAdministrateur)

#Rôle à modifier
@commands.group(name = "membre", aliases = ["m"])
async def membreGroupRole(ctx: commands.Context):
    """Rôle de membre"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(membreGroupRole)

@commands.group(name = "modération", aliases = ["modo", "staff", "s"])
async def modérationGroupRôle(ctx: commands.Context):
    """Rôle de modération"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(modérationGroupRôle)

@commands.group(name = "admininistrateur", aliases = ["admin", "ad", "a"])
async def administrateurGroupRôle(ctx: commands.Context):
    """Rôle d'administrateur"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(administrateurGroupRôle)

@commands.group(name = "muet", aliases = ["mu"])
async def muetGroupRôle(ctx: commands.Context):
    """Rôle de personne muette"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(muetGroupRôle)

@commands.group(name = "valorant", aliases = ["calo"])
async def valorantGroupRôle(ctx: commands.Context):
    """Rôle des joueurs de Valorant"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(valorantGroupRôle)

@commands.group(name = "entraîneurs", aliases = ["e"])
async def entraîneursGroupRole(ctx: commands.Context):
    """Rôle des entraîneurs valo"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(entraîneursGroupRole)


#Type de modification
@commands.command(name = "ajouter", aliases = ["a", "+"])
async def addCmdRoles(ctx: commands.Context, *rôles: discord.Role):
    """Ajoute le rôle indiqué dans la liste des rôles correspondant au parent dans le fichier de données des serveurs"""
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        if not str(ctx.guild.id) in data:
            dataGuild(ctx.guild.id, ctx)
        for rôle in rôles:
            if rôle.id in data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]]:
                return await ctx.reply("Le rôle <" + rôle.name + "> est déjà assigné au grade [" + ctx.invoked_parents[2] + "].")
            data[str(ctx.guild.id)]["rôles"][ctx.invoked_parents[2]].append(rôle.id)
            await ctx.reply("Le rôle <" + rôle.name + "> est maintenant ajouté en tant que rôle pour [" + ctx.invoked_parents[2] + "].")
            with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json", "w") as fileWritable:
                fileWritable.write(json.dumps(data, indent=4))


@commands.command(name = "enlever", aliases = ["e", "-"])
async def enleverCmdRôles(ctx: commands.Context, *rôles: discord.Role):
    """Supprime le rôle indiqué dans la liste des rôles correspondant au parent dans le fichier de données des serveurs"""
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        if not str(ctx.guild.id) in data:
            return dataGuild(ctx.guild.id, ctx)
        for role in rôles:
            if not role.id in data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]]:
                return await ctx.reply("Le rôle <" + role.name + "> n'est déjà pas assigné au grade [" + ctx.invoked_parents[2] + "].")
            data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]].pop(data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]].index(role.id))
            await ctx.reply("Le rôle <" + role.name + "> est maintenant retiré de la liste de rôles pour le grade [" + ctx.invoked_parents[2] + "].")
            with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json", "w") as fileWritable:
                fileWritable.write(json.dumps(data, indent=4))


@commands.command(name = "liste", aliases = ["l"])
async def listeCmdRoleORRoles(ctx: commands.Context):
    """Envoie la liste des rôles assignés aux permissions du serveur (une seule si le rôle de permission en question est précisée avant le liste)"""
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        if ctx.invoked_parents[-1] == "role":
            embed = discord.Embed(title = "Liste des rôles assignés")
            for roleName in data[str(ctx.guild.id)]["roles"]:
                rolesID = data[str(ctx.guild.id)]["roles"][roleName]
                message = []
                for roleID in rolesID:
                    message.append("<@&" + str(roleID) + ">")
                message = ", ".join(message)
                if len(message) == 0:
                    message = "Aucun rôle assigné"
                embed.add_field(name = roleName, value = message, inline = False)
            await ctx.reply(embed = embed)
        #Ne renvoie que celle du rôle demandé si la commande est après un rôle
        else:
            embed = discord.Embed(title = "Liste des rôles assignés")
            rolesID = data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[-1]]
            message = []
            for roleID in rolesID:
                message.append("<@&" + str(roleID) + ">")
            message = ", ".join(message)
            if len(message) == 0:
                message = "Aucun rôle assigné"
            embed.add_field(name = ctx.invoked_parents[-1], value = message, inline = False)
            await ctx.reply(embed = embed)



#Giveaway
@commands.group(name = "concours", aliases = ["co", "giveaway", "g"])
async def tombolaGroupAdmin(ctx: commands.Context):
    """Commandes des tombola niveau administrateur"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(tombolaGroupAdmin)

@commands.command(name = "créer", aliases = ["c", "+"])
async def créerCmdTombola(ctx: commands.Context, nom: str, description: str, salon: discord.TextChannel = "Salon du message", emote: typing.Union[discord.Emoji, str] = "🎉"):
    """Crée une tombola"""
    if not isinstance(emote, discord.Emoji) and len(emoji.emoji_list(str(emote))) == 0:
        return await ctx.send("Émoji invalide")
    if salon == "Salon du message":
        salon = ctx.channel
    embed = discord.Embed(title = nom, description = description)
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        giveawayName = [g for g in data[str(ctx.guild.id)]["giveaway"] if g["nom"] == nom]
        if len(giveawayName) != 0:
            return await ctx.reply("Un giveaway avec ce nom existe déjà.")
        message = await salon.send(embed = embed)
        await message.add_reaction(emote)
        giveaway = deepcopy(modele["giveaway"][0])
        giveaway["nom"] = nom
        giveaway["description"] = description
        giveaway["participants"] = []
        if isinstance(emote, discord.Emoji):
            giveaway["reaction"].append(emote.name)
        else:
            giveaway["reaction"].append(emote)
        giveaway["messageID"] = message.id
        giveaway["gagnants"] = []
        data[str(ctx.guild.id)]["giveaway"].append(giveaway)
        await ctx.message.delete()
        with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json", "w") as fileWritable:
            fileWritable.write(json.dumps(data, indent = 4))


@commands.command(name = "terminer", aliases = ["ter", "-"])
async def terminerCmdTombola(ctx: commands.Context, nom: str):
    """Supprime une tombola par son nom"""
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        await ctx.message.delete()
        data = json.load(file)
        giveawayName = [g for g in data[str(ctx.guild.id)]["giveaway"] if g["nom"] == nom]
        if len(giveawayName) == 0:
            return await ctx.reply("Aucun giveaway n'a ce nom.")
        if len(giveawayName[0]["gagnants"]) == 0:
            embed = discord.Embed(title = giveawayName[0]["nom"], description = giveawayName[0]["description"])
            embed.add_field(name = "Erreur ❌", value = "Giveaway annulé")
            msg = await ctx.channel.fetch_message(giveawayName[0]["messageID"])
            await msg.edit(embed = embed)
        await msg.clear_reactions()
        data[str(ctx.guild.id)]["giveaway"].pop(data[str(ctx.guild.id)]["giveaway"].index(giveawayName[0]))
        for id in giveawayName[0]["gagnants"]:
            user = await ctx.bot.fetch_user(id)
            channel = await user.create_dm()
            channel.send("Félicitations, vous avez gagné le giveaway \"" + giveawayName[0]["nom"] + "\".")
        with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json", "w") as fileWritable:
            fileWritable.write(json.dumps(data, indent = 4))


@commands.command(name = "tirer", aliases = ["t"])
async def tirerCmdTombola(ctx: commands.Context, nom: str, nombreGagnants: int = 1):
    """Choisit au hasard un gagnant parmi les participants d'une tombola"""
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        giveawayName = [g for g in data[str(ctx.guild.id)]["giveaway"] if g["nom"] == nom]
        if len(giveawayName) == 0:
            return await ctx.reply("Aucun giveaway n'a ce nom.")
        if len(giveawayName[0]["participants"]) == 0:
            return await ctx.reply("Il faut au moins un participant pour tirer un membre au hasard")
        if nombreGagnants > len(giveawayName[0]["participants"]):
            return await ctx.reply("Pas assez de participants au concours pour ce nombre de gagnants")
        ids = random.sample(giveawayName[0]["participants"], k=nombreGagnants)
        giveawayName[0]["gagnants"] = [ctx.bot.get_user(i).mention for i in ids if ctx.bot.get_user(i).bot == False]
        embed = discord.Embed(title = giveawayName[0]["nom"], description = giveawayName[0]["description"]).add_field(name = "Gagnant(s) ✅", value = ", ".join(giveawayName[0]["gagnants"]))
        msg = await ctx.channel.fetch_message(giveawayName[0]["messageID"])
        await msg.edit(embed = embed)
        await msg.clear_reactions()
        await ctx.message.delete()



@commands.group(name = "contrôle", aliases = ["c"])
async def contrôleGroupAdmin(ctx: commands.Context):
    """Rôle des joueurs Valo"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(valorantGroupRôle)


@commands.command(name = "arrêter", aliases = ["stop"])
async def arrêterCmdContrôle(ctx: commands.Context):
    """Stop le bot"""
    msg = await ctx.reply("Voulez-vous vraiment arrêter le bot ?")
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    try:
        #Attend la reaction de l'utilisateur
        reaction, user = await ctx.bot.wait_for(event = "reaction_add", timeout = 30.0, check = lambda reaction, user: user.id == ctx.author.id and reaction.message.id == msg.id)
        if reaction.emoji == "❌":
            await msg.clear_reactions()
            await ctx.reply("Annulation de l'arrêt")
            raise Exception("Annulation de l'arrêt")
        elif reaction.emoji == "✅":
            await msg.clear_reactions()
            await ctx.reply("Arrêt du bot")
            await ctx.bot.close()
    #Si le timeout est dépassé ou qu'il y a une erreur
    except Exception as err:
        print(err)


@commands.command(name = "relancer", aliases = ["reboot"])
async def relancerCmdContrôle(ctx: commands.Context):
    msg = await ctx.reply("Voulez-vous vraiment relancer le bot ?")
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    try:
        #Attend la reaction de l'utilisateur
        reaction, user = await ctx.bot.wait_for(event = "reaction_add", timeout = 30.0, check = lambda reaction, user: user.id == ctx.author.id and reaction.message.id == msg.id)
        if reaction.emoji == "❌":
            await msg.clear_reactions()
            await ctx.reply("Annulation du relancement")
            raise Exception("Annulation du relancement")
        elif reaction.emoji == "✅":
            await msg.clear_reactions()
            await ctx.reply("Relancement du bot")
            await ctx.bot.close()
            os.system("python " + os.path.abspath(os.path.dirname(__file__)) + "/../index.py")
    #Si le timeout est dépassé ou qu'il y a une erreur
    except Exception as err:
        print(err)


#Ajout des groupes aux catégories
administrateurGroup.add_command(rôlesGroupAdministrateur)
rôlesGroupAdministrateur.add_command(membreGroupRole)
rôlesGroupAdministrateur.add_command(modérationGroupRôle)
rôlesGroupAdministrateur.add_command(administrateurGroupRôle)
rôlesGroupAdministrateur.add_command(muetGroupRôle)
rôlesGroupAdministrateur.add_command(valorantGroupRôle)
rôlesGroupAdministrateur.add_command(entraîneursGroupRole)

administrateurGroup.add_command(tombolaGroupAdmin)

administrateurGroup.add_command(contrôleGroupAdmin)


#Ajout des commandes aux catégories
membreGroupRole.add_command(addCmdRoles)
modérationGroupRôle.add_command(addCmdRoles)
administrateurGroupRôle.add_command(addCmdRoles)
muetGroupRôle.add_command(addCmdRoles)
valorantGroupRôle.add_command(addCmdRoles)
entraîneursGroupRole.add_command(addCmdRoles)

membreGroupRole.add_command(enleverCmdRôles)
modérationGroupRôle.add_command(enleverCmdRôles)
administrateurGroupRôle.add_command(enleverCmdRôles)
muetGroupRôle.add_command(enleverCmdRôles)
valorantGroupRôle.add_command(enleverCmdRôles)
entraîneursGroupRole.add_command(enleverCmdRôles)

rôlesGroupAdministrateur.add_command(listeCmdRoleORRoles)
membreGroupRole.add_command(listeCmdRoleORRoles)
modérationGroupRôle.add_command(listeCmdRoleORRoles)
administrateurGroupRôle.add_command(listeCmdRoleORRoles)
muetGroupRôle.add_command(listeCmdRoleORRoles)
valorantGroupRôle.add_command(listeCmdRoleORRoles)
entraîneursGroupRole.add_command(listeCmdRoleORRoles)


tombolaGroupAdmin.add_command(créerCmdTombola)
tombolaGroupAdmin.add_command(terminerCmdTombola)
tombolaGroupAdmin.add_command(tirerCmdTombola)

contrôleGroupAdmin.add_command(arrêterCmdContrôle)
contrôleGroupAdmin.add_command(relancerCmdContrôle)



#Commande setup pour l'importation du module
def setup(bot: commands.Bot):
    """Rajoute la catégorie admin au bot"""
    bot.add_command(administrateurGroup)