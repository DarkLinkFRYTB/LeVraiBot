#Immportations
from copy import deepcopy
import json
import time
import typing
from discord.ext import commands


#Modèle d'un serveur dans le fichier JSON
modele = {
    "roles": {
        "mute": [0],
        "membre": [0],
        "staff": [0],
        "admin": [0],
        "valorant": [0],
        "coach": [0]
    },
    "membres": [
        {
            "ID": 0,
            "Compte riot": ""
        }
    ],
    "practices": [
        {
            "ID": 0,
            "joueurs": [0],
            "date": "",
            "host": 0,
            "rangs": ""
        }
    ],
    "giveaway": [
        {
            "nom": "",
            "description": "",
            "participants": [0],
            "reaction": [],
            "messageID": 0,
            "gagnants": [0]
        }
    ]
}


def findUser(userID: int, guildID: typing.Union[int, str]) -> dict or None:
    """Cherche un utilisateur dans la liste et le renvoie si il le trouve, sinon renvoie None"""
    with open("./guilds.json") as file:
        data = json.load(file)
        indice = [i for i, elem in enumerate(data[str(guildID)]["membres"]) if elem["ID"] == userID]
        #Vérifie si aucun membre de la liste n'a cet ID
        if len(indice) == 0:
            return None
        #Supprime ceux en trop si il y en a plusieurs
        elif len(indice) > 1:
            print(guildID)
            while len(indice) > 1:
                data[str(guildID)]["membres"].pop(indice[-1])
                indice.pop(-1)
                print(indice)
        #Réécris le fichier des membres
        with open("./guilds.json", "w") as fileWritable:
            fileWritable.write(json.dumps(data, indent=4))
        #Renvoie les données du membre
        return data[str(guildID)]["membres"][indice[0]]


def checkPractice(guildID: int):
    """Vérifie si les practices d'un serveur ne sont pas dépassées"""
    with open("./guilds.json") as file:
        data = json.load(file)
        for prac in data[str(guildID)]["practices"]:
            if time.mktime(time.strptime(prac["date"], format)) - time.mktime(time.localtime()) < 0:
                data[str(guildID)]["practices"].pop(data[str(guildID)]["practices"].index(prac))
        with open("./guilds.json", "w") as fileWritable:
            fileWritable.write(json.dumps(data, indent = 4))




def dataGuild(guildID: int, arg: typing.Union[commands.Bot, commands.Context]):
    """Vérifie et réécris certaines données du serveur dans le fichier JSON si elles sont incorrectes"""
    with open("./guilds.json") as file:
        def verifyRecursive(data: typing.Union[dict, list], base: typing.Union[dict, list], sendDel: bool = False) -> bool or None:
            """Fonction récursive pour vérifier un élément déjà existant dans le fichier JSON afin d'accéder à chaque sous élément des données"""
            #Sépare le code si il s'agit d'un dictionnaire ou d'une liste
            if isinstance(data, dict):
                #Crée un élément si il est dans le modèle mais pas dans les données si ce n'est pas le modèle d'une liste
                for element in base:
                    if element not in data:
                        if not isinstance(base[element], list):
                            data[element] = base[element]
                        else:
                            data[element] = []
                        if sendDel:
                            return True

                for element in list(data):
                    #Supprime un élément des données si il n'est pas dans le modèle
                    if element not in base:
                        del data[element]
                    else:
                        #Réinitialise une valeur si elle n'est pas du même type que celle du modèle
                        if not isinstance(data[element], type(base[element])):
                            data[element] = base[element]
                        #Effectue la fonction récursive plus loin dans l'arborescence si l'élément est un objet ou une liste
                        if isinstance(data[element], dict) or isinstance(data[element], list):
                            verifyRecursive(data[element], base[element])
            else:
                for element in data:
                    #Autorise n'importe quel type de valeurs si la liste du modèle est vide
                    if len(base) == 0:
                        continue
                    #Supprime une valeur si elle n'est pas du même type que celle du modèle (les listes ne doivent contenir qu'un seul type de données)
                    if not isinstance(element, type(base[0])):
                        data.pop(data.index(element))
                    #Effectue la fonction récursive plus loin dans l'arborescence si l'élément est un objet ou une liste
                    if isinstance(element, dict) or isinstance(element, list):
                        mustDel = verifyRecursive(element, base[0], True)
                        #Supprime l'élément si il ne correspond pas au modèle
                        if mustDel:
                            data.pop(data.index(element))

        def newRecursive(data: dict, base: dict) -> None:
            """Fonction récursive qui crée un dictionnaire du fichier JSON selon le modèle (avec les listes vides car elles ne contiennent qu'un modèle de ce que doit contenir la liste)"""
            for element in base:
                data[element] = type(base[element])()
                if isinstance(data[element], dict):
                    newRecursive(data[element], base[element])

        data = json.load(file)

        #Vérifie si le bot est dans le serveur en question
        if isinstance(arg, commands.Bot):
            if not arg.get_guild(int(guildID)):
                return print(Exception("Le bot n'est pas dans un serveur avec cet ID"))

        #Vérifie si le serveur existe dans le fichier JSON
        if not str(guildID) in data:
            data[str(guildID)] = {}
            newRecursive(data[str(guildID)], modele)
        else:
            #Effectue la fonction récursive de vérification pour le serveur
            verifyRecursive(data[str(guildID)], modele)

        #Réécris le fichier une première fois afin d'avoir bien toutes les informations actuelles dans le fichier car findUser le réouvre
        with open("./guilds.json", "w") as fileWritable:
            fileWritable.write(json.dumps(data, indent=4))
        
        #Vérification si tout les membres sont dans le fichier
        members = []
        if isinstance(arg, commands.Bot):
            members = arg.get_guild(guildID).members
        elif isinstance(arg, commands.Context):
            members = arg.guild.members
        for membre in members:
            #Si il n'y est pas, il est rajouté au fichier suivant le modèle en modifiant l'ID
            if not findUser(membre.id, guildID):
                temp = deepcopy(modele["membres"][0])
                temp["ID"] = membre.id
                data[str(guildID)]["membres"].append(temp)
                del temp

        #Réécris le fichier une seconde fois pour mettre les informations des membres
        with open("./guilds.json", "w") as fileWritable:
            fileWritable.write(json.dumps(data, indent=4))