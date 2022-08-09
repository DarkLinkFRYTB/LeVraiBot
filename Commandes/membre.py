"""#Importation
from discord.ext import commands
guilds = open("../guilds.json")
guildsWritable = open("../guilds.json", "w")

#Variables nécessaires
bot = commands.Bot()


#Catégorie
@bot.group(name = "membre", aliases = ["all"], help = "Cette catégorie regroupe toutes les commandes utilisables par l'ensemble des membres du discord")
@commands.guild_only()
@commands.check_any()
async def membre(ctx: commands.Context):
    \"""Commandes utilisables par tout les membres du serveur\"""
    if ctx.invoked_subcommand is None:
        await ctx.reply("Cette catégorie doit être utilisée avec une sous-commande. Pour voir les sous-commandes disponibles pour une catégorie ou pour une sous-commande : !help <caégorie ou sous-commande>")

@membre.command(name = "serverinfo", aliases = ["servinfo", "servinformation", "serveurinfo", "serveurinformation", "serverinfo", "serverinformation", "si"])
async def serverinfo(ctx: commands.Context):
    return;

guilds.close()
guildsWritable.close()"""