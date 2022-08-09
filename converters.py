#Temps
def toMilliseconds(milliseconds: int = 0, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
    """Transforme les paramètres de temps donnés en paramètres en millisecondes"""
    hours += days * 24
    minutes += hours * 60
    seconds += minutes * 60
    milliseconds += seconds * 1000
    return milliseconds


def toSeconds(milliseconds: int = 0, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
    """Transforme les paramètres de temps donnés en paramètres en secondes"""
    hours += days * 24
    minutes += hours * 60
    seconds += minutes * 60
    seconds += milliseconds / 1000
    return seconds


def toMinutes(milliseconds: int = 0, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
    """Transforme les paramètres de temps donnés en paramètres en minutes"""
    hours += days * 24
    minutes += hours * 60
    seconds += milliseconds / 1000
    minutes += seconds / 60
    return minutes


def toHours(milliseconds: int = 0, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
    """Transforme les paramètres de temps donnés en paramètres en heures"""
    hours += days * 24
    seconds += milliseconds / 1000
    minutes += seconds / 60
    hours += minutes / 60
    return hours


def toDays(milliseconds: int = 0, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
    """Transforme les paramètres de temps donnés en paramètres en jours"""
    seconds += milliseconds / 1000
    minutes += seconds / 60
    hours += minutes / 60
    days += hours / 24
    return days




#Couleurs
fromHexa = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15
}
toHexa = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "F"
}

def RGB(number: list[int, int, int] = None) -> None | dict[str, list[int, int, int] | int | str]:
    """Renvoie la valeur du nombre RGB donné en paramètre sous forme de liste de longueur 3 (donnant dans l'ordre un nombre entre 0 et 255 pour la valeur de Rouge, puis Vert, puis Bleu) dans un dictionnaire avec sa valeur RVB, sa valeur décimale et sa valeur hexadécimale"""
    #Ne renvoie rien si la liste ne contient pas les 3 valeurs de couleur
    if not number or len(number) != 3:
        return None

    value = {
        "RGB": number,
        "decimal": 0,
        "hexadecimal": ""
    }

    #Rajoute les données à value pour chaque couleur de la liste
    for couleur in number:
        value["decimal"] += couleur * 255 ** (2 - number.index(couleur))
        seizaine = int(couleur / 16)
        unite = couleur % 16
        value["hexadecimal"] += toHexa[seizaine] + toHexa[unite]
    
    return value


def hexadecimal(number: str = None) -> None | dict[str, list[int, int, int] | int | str]:
    """Renvoie la valeur du nombre hexadécimal donné en paramètre (de longueur 3 pour lettres doubles ou 6 pour lettres simples) dans un dictionnaire avec sa valeur RVB, sa valeur décimale et sa valeur hexadéciamle"""
    if not number:
        return None
    value = {
        "RGB": [0, 0, 0],
        "decimal": 0,
        "hexadecimal": number
    }
    if len(number) == 3:
        for lettre in list(number):
            if not lettre in fromHexa:
                return None
            number = number[:number.index(lettre)] + lettre + number[number.index(lettre):]

    #Ne renvoie rien si le nombre n'a pas 3 ou 6 caractères
    elif len(number) != 6:
        return None

    #Ne renvoie rien si le nombre contient des caractères invalides
    for lettre in number:
        if not lettre in fromHexa:
            return None

    #Sépare le contenu pour chaque valeur de couleur
    splitted = [number[:2], number[2:4], number[4:]]

    for couleur in splitted:
        value["RGB"][splitted.index(couleur)] = fromHexa[couleur[0]]*16 + fromHexa[couleur[1]]
        value["decimal"] += fromHexa[couleur[0]]*16 + fromHexa[couleur[1]] * 255 ** (2 - splitted.index(couleur))

    #Renvoie le dictionnaire des valeurs 
    return value


def decimal(number: int = None) -> None | dict[str, list[int, int, int] | int | str]:
    """Renvoie la valeur du nombre décimal donné en paramètre dans un dictionnaire avec sa valeur RVB, sa valeur décimale et sa valeur hexadéciamle"""
    if not number: 
        return None

    rouge = (number // 255**2) - 1
    vert = ((number - rouge * 255**2) // 255) - 1
    bleu = number - rouge * 255**2 - vert * 255
    rouge1 = rouge // 16
    rouge2 = rouge % 16
    vert1 = vert // 16
    vert2 = vert % 16
    bleu1 = bleu // 16
    bleu2 = bleu % 16

    value = {
        "RGB": [rouge, vert, bleu],
        "decimal": number,
        "hexadecimal": toHexa[rouge1] + toHexa[rouge2] + toHexa[vert1] + toHexa[vert2] + toHexa[bleu1] + toHexa[bleu2]
    }

    return value