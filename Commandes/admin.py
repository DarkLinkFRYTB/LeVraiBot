#Importations
import json
from discord.ext import commands
import discord
import checks
import os
from guildWriter import dataGuild


#Groupe général
@commands.group(name = "admin", aliases = ["ad"])
@commands.check_any(commands.check(lambda ctx: checks.hasRolePerm(ctx, ctx.guild.id, ctx.author.id, "Admin")), commands.check(lambda ctx: ctx.author.guild_permissions.administrator))
async def adminGroup(ctx: commands.Context):
    """Commandes réservée aux administrateurs"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(adminGroup)



#Modification des rôles
@commands.group(name = "role", aliases = ["r"])
async def roleGroupAdmin(ctx: commands.Context):
    """Commandes des rôles de permission du serveur"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(roleGroupAdmin)

#Rôle à modifier
@commands.group(name = "membre", aliases = ["m"])
async def membreGroupRole(ctx: commands.Context):
    """Rôle de membre"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(membreGroupRole)

@commands.group(name = "staff", aliases = ["s"])
async def staffGroupRole(ctx: commands.Context):
    """Rôle de Staff"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(staffGroupRole)

@commands.group(name = "admin", aliases = ["a"])
async def adminGroupRole(ctx: commands.Context):
    """Rôle d'administrateur"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(adminGroupRole)

@commands.group(name = "mute", aliases = ["mu"])
async def muteGroupRole(ctx: commands.Context):
    """Rôle de personne mute"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(muteGroupRole)

@commands.group(name = "valorant", aliases = ["calo"])
async def valorantGroupRole(ctx: commands.Context):
    """Rôle des joueurs Valo"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(valorantGroupRole)

@commands.group(name = "coach", aliases = ["c"])
async def coachGroupRole(ctx: commands.Context):
    """Rôle des coach valo"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(coachGroupRole)


#Type de modification
@commands.command(name = "add", aliases = ["a", "+"])
async def addCmdRoles(ctx: commands.Context, *roles: discord.Role):
    """Ajoute le rôle indiqué dans la liste des rôles correspondant au parent dans le fichier guild.json"""
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        if not str(ctx.guild.id) in data:
            dataGuild(ctx.guild.id, ctx)
        for role in roles:
            if role.id in data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]]:
                return await ctx.reply("Le rôle <" + role.name + "> est déjà assigné au grade [" + ctx.invoked_parents[2] + "].")
            data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]].append(role.id)
            await ctx.reply("Le rôle <" + role.name + "> est maintenant ajouté en tant que rôle pour [" + ctx.invoked_parents[2] + "].")
            with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json", "w") as fileWritable:
                fileWritable.write(json.dumps(data, indent=4))


@commands.command(name = "remove", aliases = ["r", "-"])
async def removeCmdRoles(ctx: commands.Context, *roles: discord.Role):
    """Supprime le rôle indiqué dans la liste des rôles correspondant au parent dans le fichier guild.json"""
    with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json") as file:
        data = json.load(file)
        if not str(ctx.guild.id) in data:
            return dataGuild(ctx.guild.id, ctx)
        for role in roles:
            if not role.id in data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]]:
                return await ctx.reply("Le rôle <" + role.name + "> n'est déjà pas assigné au grade [" + ctx.invoked_parents[2] + "].")
            data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]].pop(data[str(ctx.guild.id)]["roles"][ctx.invoked_parents[2]].index(role.id))
            await ctx.reply("Le rôle <" + role.name + "> est maintenant retiré de la liste de rôles pour le grade [" + ctx.invoked_parents[2] + "].")
            with open(os.path.abspath(os.path.dirname(__file__)) + "/../guilds.json", "w") as fileWritable:
                fileWritable.write(json.dumps(data, indent=4))


#Liste des rôles
@commands.command(name = "list", aliases = ["l"])
async def list_rolesCmdRoleORRoles(ctx: commands.Context):
    """Envoie la liste des rôles assignés aux permissions du serveur (une seule si la permission en question est précisée avant le list)"""
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
@commands.command(name = "giveaway", aliases = ["ga", "g"])
async def giveawayGroupAdmin(ctx: commands.Context):
    """Commandes des giveaway niveau administrateur"""
    if not ctx.invoked_subcommand:
        await ctx.reply("Cette commande nécessite d'être appelée avec une sous-commande")
        await ctx.send_help(giveawayGroupAdmin)

@commands.command(name = "create", aliases = ["c", "+"])
async def createCmdGiveaway(ctx: commands.Context, name: str, description: str):
    pass


#Ajout des groupes aux catégories
adminGroup.add_command(roleGroupAdmin)
roleGroupAdmin.add_command(membreGroupRole)
roleGroupAdmin.add_command(staffGroupRole)
roleGroupAdmin.add_command(adminGroupRole)
roleGroupAdmin.add_command(muteGroupRole)
roleGroupAdmin.add_command(valorantGroupRole)
roleGroupAdmin.add_command(coachGroupRole)

adminGroup.add_command(giveawayGroupAdmin)


#Ajout des commandes aux catégories
membreGroupRole.add_command(addCmdRoles)
staffGroupRole.add_command(addCmdRoles)
adminGroupRole.add_command(addCmdRoles)
muteGroupRole.add_command(addCmdRoles)
valorantGroupRole.add_command(addCmdRoles)
coachGroupRole.add_command(addCmdRoles)

membreGroupRole.add_command(removeCmdRoles)
staffGroupRole.add_command(removeCmdRoles)
adminGroupRole.add_command(removeCmdRoles)
muteGroupRole.add_command(removeCmdRoles)
valorantGroupRole.add_command(removeCmdRoles)
coachGroupRole.add_command(removeCmdRoles)

roleGroupAdmin.add_command(list_rolesCmdRoleORRoles)
membreGroupRole.add_command(list_rolesCmdRoleORRoles)
staffGroupRole.add_command(list_rolesCmdRoleORRoles)
adminGroupRole.add_command(list_rolesCmdRoleORRoles)
muteGroupRole.add_command(list_rolesCmdRoleORRoles)
valorantGroupRole.add_command(list_rolesCmdRoleORRoles)
coachGroupRole.add_command(list_rolesCmdRoleORRoles)


#Commande setup pour l'importation du module
def setup(bot: commands.Bot):
    """Rajoute la catégorie admin au bot"""
    bot.add_command(adminGroup)