#Importations
import json
import typing
from discord.ext import commands
from guildWriter import dataGuild
import time


def hasRolePerm(arg: typing.Union[commands.Bot, commands.Context], guildID: typing.Union[str, int], memberID: typing.Union[str, int], *rolesNames: str):
    """Vérifie si l'utilisateur à le rôle de permission fourni dans le serveur. rolesNames doit être "Membre" or "Staff" or "Admin" or "Mute" or "Valorant" or "Coach" """
    with open("guilds.json") as file:
        data = json.load(file)
        #Vérifie si le serveur existe dans le fichier
        if not str(guildID) in data:
            dataGuild(guildID, arg)
            return
        for role in rolesNames:
            #Récupère les rôles de permissions du serveur demandé
            roles = data[str(guildID)]["roles"][role.lower()]
            if len(roles) == 0:
                raise commands.CommandError(f"Rôle {role} non assigné dans le fichier")
            guild = 0
            if isinstance(arg, commands.Bot):
                guild = arg.get_guild(int(guildID))
            else:
                guild = arg.guild
            member = [m for m in guild.members if m.id == int(memberID)]
            if len(member) == 0:
                raise commands.CommandError("Utilisateur non trouvé dans le fichier")
            member = member[0]
            roleList = [r for r in member.roles if r.id in roles]
            if len(roleList) != 0:
                return True
        raise commands.CommandError("Rôle(s) manquant(s)")


def isValidDate(date_text: str, format = "%d/%m/%Y"):
    """Vérifie le format date"""
    try:
        time.strptime(date_text, format)
        return True
    except ValueError:
        return False
