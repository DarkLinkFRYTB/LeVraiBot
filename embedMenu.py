#Importations
import discord
from discord.ext import commands
from index import bot


#Classe des menus
class EmbedMenu:
    def __init__(self, pages: list[discord.Embed], ctx: commands.Context):
        """Crée un menu en donnant une liste des pages de base et le contexte"""
        self.pages = pages
        self.message = ctx.message
        self.user = ctx.author
        self.page = 0

    def addPage(self, content: discord.Embed, index: int = -1):
        """Ajoute une page au menu (par défaut à la fin)"""
        if index > len(self.pages):
            index = len(self.pages)
        elif index < 0:
            index = len(self.pages) - index + 1
        self.pages.insert(index, content)

    def removePage(self, index: int):
        """Supprime une page à l'index indiqué"""
        if index <= len(self.pages) & index > 0:
            self.pages.pop(index)
    
    async def toPage(self, index: int):
        """Le menu va à la page à l'index indiqué et modifie le contenu de son message"""
        if index <= len(self.pages) & index > 0:
            self.page = index
            await self.editMessage()

    async def nextPage(self, amount: int = 1):
        """Le menu va à une page plus tard indiquée par amount (par défaut la page juste après)"""
        if self.page + amount < len(self.pages) & self.page + amount > 0:
            self.page += amount
            await self.editMessage()

    async def prevPage(self, amount: int = 1):
        """Le menu va à une page plus tôt indiquée par amount (par défaut la page juste avant)"""
        if self.page - amount < len(self.pages) & self.page - amount > 0:
            self.page -= amount
            await self.editMessage()

    async def editMessage(self):
        """Modifie le message du menu et rajoute au cas où ses réactions"""
        await self.message.edit(content = None, embed = self.pages[self.page])
        await self.message.add_reaction('◀️')
        await self.message.add_reaction('▶️')
        await self.message.add_reaction('❌')
        return self
    
    async def delMenu(self):
        """Supprime le menu"""
        await self.message.edit(embed = None, content = "Délai atteint ou menu arrêté, suppression du message de menu", delete_after = 5)
        del self

    async def check_reac(self, reaction: discord.Reaction):
        """Vérifie la réaction que l'utilisateur a mis"""
        if reaction.emoji == "◀️":
            await self.prevPage()
        elif reaction.emoji == "▶️":
            await self.nextPage()
        elif reaction.emoji == "❌":
            await self.delMenu()

    async def start(self):
        """Commence le menu en le faisant se modifier lui-même et créer une boucle infinie tant que l'utilisateur n'atteint pas le timeout"""
        await self.editMessage()
        while True:
            try:
                #Attend la reaction de l'utilisateur
                reaction, user = await bot.wait_for(event = "reaction_add", timeout = 30.0, check = lambda reaction, user: user.id == self.user.id)
                await self.message.remove_reaction(reaction, user)
                await self.check_reac(reaction)

            #Si le timeout est dépassé ou qu'il y a une erreur
            except Exception as err:
                print(err)
                await self.delMenu()
                break