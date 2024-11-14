'''
    Console.py : formate la sortie affichage sur ecran
'''

import datetime
import msvcrt
import os
import re
import sys
import termios
import unicodedata

from .Singleton import Singleton

class Console(Singleton):
    '''
        classe Console
    '''

    _COLORS:dict
    _STYLE_COLORS:dict
    _STYLE_INDENTS:dict
    _colorize: bool
    _debug_mode: str
    _prefix_mode: bool

    #
    # Private methods
    #
    def __init__(self, debug_mode: str=""):
        self._colorize = True
        self._debug_mode = debug_mode
        self._prefix_mode = True

        self._COLORS = {
            "BOLD": "\033[1m",
            "BLACK": "\033[30m",
            "RED": "\033[31m",
            "GREEN": "\033[32m",
            "YELLOW": "\033[33m",
            "MAUVE": "\033[34m",
            "PURPLE": "\033[35m",
            "CYAN": "\033[36m",
            "WHITE": "\033[37m",
            "BK_BLACK": "\033[40m",
            "BK_RED": "\033[41m",
            "BK_GREEN": "\033[42m",
            "BK_YELLOW": "\033[43m",
            "BK_MAUVE": "\033[44m",
            "BK_PURPLE": "\033[45m",
            "BK_CYAN": "\033[46m",
            "BK_WHITE": "\033[47m",
            "RESET": "\033[0m",
        }

        self._STYLE_COLORS = {
            "COMMAND": self._COLORS["BLACK"] + self._COLORS["BK_WHITE"],
            "TITRE1": self._COLORS["BOLD"] + self._COLORS["MAUVE"],
            "TITRE2": self._COLORS["BOLD"] + self._COLORS["MAUVE"],
            "TITRE3": self._COLORS["BOLD"] + self._COLORS["MAUVE"],
            "MENU": self._COLORS["BOLD"] + self._COLORS["MAUVE"],
            "OK": self._COLORS["BOLD"] + self._COLORS["GREEN"],
            "WARNING": self._COLORS["BOLD"] + self._COLORS["YELLOW"],
            "ERROR": self._COLORS["BOLD"] + self._COLORS["RED"]
        }

        self._STYLE_INDENTS = {
            "TITRE1": 8,
            "TITRE2": 4,
            "TITRE3": 2,
        }


    #
    # Protected methods
    #

    def _flush_input(self):
        try:
            while msvcrt.kbhit(): # type: ignore
                msvcrt.getch() # type: ignore
        except ImportError:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)

    def _flush_output(self):
        try:
            sys.stdout.flush()
        except Exception as e:
            console.Print(str(e))

    def _remove_accents(self, text: str=''):
        try:
            text = text.encode('utf-8') # type: ignore
        except (TypeError, NameError):  # unicode is a default on python 3
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore') # type: ignore
        text = text.decode('utf-8') # type: ignore
        return str(text)

    def _remove_colors(self, text: str=''):
        for my_color_key, my_color in self._COLORS.items():
            text = text.replace(my_color, '')
        return text

    def _print(self, *args, **kwargs):
        text = args[0]
        if self._colorize:
            print(*args, **kwargs)
        else:
            print(self._remove_colors(text), **kwargs)

    #
    # Public methods
    #

    def ClearScreen(self):
        if os.name == 'posix':
            # Pour macOS et Linux
            _ = os.system('clear')
        else:
            # Pour Windows
            _ = os.system('cls')

    def Debug(self, text: str="", newline: bool=True):
        if self._debug_mode == "DEBUG":
            timestamp = datetime.datetime.now()
            if self._prefix_mode:
                self._print(f"[{timestamp}] DEBUG: ", end="")
            self._print(f"{text}", end="")
            if newline:
                self._print("")
                self._prefix_mode = True
            else:
                self._flush_output()
                self._prefix_mode = False

    def SetColorize(self, colorize: bool=True):
        self._colorize = colorize

    def SetDebugMode(self, debug_mode: str="DEBUG"):
        self._debug_mode = debug_mode
        if self._debug_mode:
            self._print(f"DEBUG_MODE={self._debug_mode}")

    def Print(self, text: str="", text_format: str="", indent: int=0, newline: bool=True):
        #
        # Propose un affichage formate.
        #
        # Il est possible de cumuler plusieurs formats. Par exemple :
        #     self.Print("Texte à afficher", text_format=["BLUE", "BOLD"], indent=4)
        # Affiche "Texte à afficher" en bleu gras, et indente de 4 espaces
        #
        # Les valeurs de text_format peuvent être les suivantes :
        #     TITRE1, TITRE2, TITRE3 : Formats de titre
        #     OK, WARNING, ERROR : Formats standards en couleur (respectivement vert, jaune, rouge)
        #     COMMAND : Utilise pour afficher une commande linux exécutée par un script (inverse video)
        #     BOLD, RED, GREEN, YELLOW, MAUVE, CYAN, PURPLE : Affiche le texte dans la couleur demandée
        #     (ou en gras pour BOLD)
        #
        # La valeur de 'indent' indique le nombre d'espaces à afficher avant la chaine (pour indenter)
        #     <valeur numérique> : Nombre d'espaces à afficher avant la chaine (pour l'indenter)
        #

        # screen_heigth, screen_width = os.popen('stty size', 'r').read().split()

        my_text = str(text).rstrip()
        my_indent = 0
        if indent == 0:
            if text_format in self._STYLE_INDENTS:
                my_indent = self._STYLE_INDENTS[text_format]
        else:
            my_indent = indent

        my_color = ""
        if text_format in self._STYLE_COLORS:
            my_color = self._STYLE_COLORS[text_format]
        else:
            if text_format in self._COLORS:
                my_color = self._COLORS[text_format]

        if text_format == "TITRE1":
            self._print("")
            self._print(' ' * my_indent + my_color + "╔═" + "═" * len(my_text) + "═╗" + self._COLORS["RESET"])
            self._print(' ' * my_indent + my_color + "║ " + my_text + " ║▒" + self._COLORS["RESET"])
            self._print(' ' * my_indent + my_color + "╚═" + "═" * len(my_text) + "═╝▒" + self._COLORS["RESET"])
            self._print(' ' * my_indent + my_color + " ▒" + "▒" * len(my_text) + "▒▒▒" + self._COLORS["RESET"])
            self._print("", end="")
        elif text_format == "TITRE2":
            self._print("")
            self._print(' ' * my_indent + my_color + my_text + self._COLORS["RESET"])
            self._print(' ' * my_indent + my_color + "―" * len(my_text) + self._COLORS["RESET"])
            self._print("", end="")
        elif text_format == "TITRE3":
            self._print("")
            self._print(' ' * my_indent + my_color + my_text + self._COLORS["RESET"])
            self._print("", end="")
        elif text_format == "COMMAND":
            self._print(' ' * my_indent + my_color + my_text + self._COLORS["RESET"], end="")
        elif text_format == "OK":
            self._print(' ' * my_indent + my_color + "[OK] " + my_text + self._COLORS["RESET"], end="")
        elif text_format == "WARNING":
            self._print(' ' * my_indent + my_color + "[WARNING] " + my_text + self._COLORS["RESET"], end="")
        elif text_format == "ERROR":
            self._print(' ' * my_indent + my_color + "[ERROR] " + my_text + self._COLORS["RESET"], end="")
        else:
            self._print(' ' * my_indent + my_color + my_text + self._COLORS["RESET"], end="")
        if newline:
            self._print("")

    def PrintTab(self, title: str="", headers: list=None, datas: list=None, footer: str=None, text_format: str="", indent: int=0, separator: str="┃"): # type: ignore
        if headers is None:
            headers = []
        if datas is None:
            datas = []

        column_separator = " " + separator + " "

        # Calcul des longueurs de champs pour ajuster la taille des colonnes du tableau
        # Le tableau $LongueurChamps contient une valeur pour chaque colonne
        field_lengths = []  # Longueurs totales des champs
        field_lengths_printable = []  # Longueurs des champs sans les codes couleur

        # Initialiser les largeurs de colonnes en parcourant les entêtes et les datas
        i_col = 0
        for my_header in headers:
            field_lengths_printable.append(len(my_header.split("|")[0].strip()))
            field_lengths.append(len(my_header.split("|")[0].strip()))
            i_col = i_col + 1
        for my_data_line in datas:
            # Pour chaque ligne, ajuster les largeurs de colonnes si besoin
            i_col = 0
            if type(my_data_line) is list:
                for my_data in my_data_line:
                    my_data_printable = my_data.split("|")[0].strip()
                    for my_color in self._COLORS:
                        my_data_printable = my_data_printable.replace(self._COLORS[my_color], "")

                    if (i_col + 1) > len(field_lengths):
                        field_lengths.append(len(my_data.split("|")[0]))
                    if len(my_data.split("|")[0]) > field_lengths[i_col]:
                        field_lengths[i_col] = len(my_data.split("|")[0])

                    if (i_col + 1) > len(field_lengths_printable):
                        field_lengths_printable.append(len(my_data_printable))
                    if len(my_data_printable) > field_lengths_printable[i_col]:
                        field_lengths_printable[i_col] = len(my_data_printable)
                    i_col = i_col + 1
            else:
                my_data_printable = my_data_line.split("|")[0].strip()
                for my_color in self._COLORS:
                    my_data_printable = my_data_printable.replace(self._COLORS[my_color], "")

                if (i_col + 1) > len(field_lengths):
                    field_lengths.append(len(my_data_line.split("|")[0]))
                if len(my_data_line.split("|")[0]) > field_lengths[i_col]:
                    field_lengths[i_col] = len(my_data_line.split("|")[0])

                if (i_col + 1) > len(field_lengths_printable):
                    field_lengths_printable.append(len(my_data_printable))
                if len(my_data_printable) > field_lengths_printable[i_col]:
                    field_lengths_printable[i_col] = len(my_data_printable)

        # Définir une ligne de pied de tableau par défaut
        if footer is None:
            footer = str(len(datas)) + " element(s)"

        # Calcule la longueur de la ligne complete (avec tous les champs), et cré la ligne de séparation avec des '-'
        line_length = 0
        separator_line = ""
        for MyLength in field_lengths_printable:
            if line_length != 0:
                line_length = line_length + len(column_separator)
                separator_line = separator_line + re.sub(r"\s", "-", re.sub(r"\S", "+", column_separator)) # type: ignore
            line_length = line_length + MyLength
            separator_line = separator_line + "-" * MyLength
        # Agrandir la longueur de ligne et la ligne de separation si nécessaire pour que le titre passe dedans
        if len(title) > line_length:
            separator_line = separator_line + "-" * (len(title) - line_length)
            line_length = len(title)
        # Agrandir la longueur de ligne et la ligne de separation si nécessaire pour que le pied passe dedans
        if len(footer) > line_length:
            separator_line = separator_line + "-" * (len(footer) - line_length)
            line_length = len(footer)
        first_separator_line_title = "┏━" + separator_line.replace("-", "━").replace("+", "━") + "━┓"
        if separator == "┃":
            first_separator_line_data = "┏━" + separator_line.replace("-", "━").replace("+", "┳") + "━┓"
        else:
            first_separator_line_data = "┏━" + separator_line.replace("-", "━").replace("+", "━") + "━┓"
        inter_top_separator_line = "┣━" + separator_line.replace("-", "━").replace("+", "┳") + "━┫"
        inter_middle_separator_line = "┣━" + separator_line.replace("-", "━").replace("+", "╋") + "━┫"
        inter_bottom_separator_line = "┣━" + separator_line.replace("-", "━").replace("+", "┻") + "━┫"
        if separator == "┃":
            last_separator_line_data = "┗━" + separator_line.replace("-", "━").replace("+", "┻") + "━┛"
        else:
            last_separator_line_data = "┗━" + separator_line.replace("-", "━").replace("+", "━") + "━┛"
        last_separator_line_footer = "┗━" + separator_line.replace("-", "━").replace("+", "━") + "━┛"

        # Titre
        if len(title) > 0:
            self.Print(first_separator_line_title, text_format=text_format, indent=indent)
            centered_title = ("{:^" + str(line_length) + "}").format(title)
            self.Print("┃ " + centered_title + " ┃", text_format=text_format, indent=indent)
            self.Print(inter_top_separator_line, text_format=text_format, indent=indent)
        else:
            self.Print(first_separator_line_data, text_format=text_format, indent=indent)

        # Entêtes
        if len(headers) > 0:
            header_line = ""
            i_col = 0

            for my_header in headers:
                length = field_lengths_printable[i_col]
                if len(header_line) > 0:
                    header_line = header_line + column_separator

                if "|" in my_header:
                    my_header_array = my_header.split("|")
                    my_header = my_header_array[0].strip()
                    for MyCommand in my_header_array[1].split(","):
                        key = MyCommand.split("=")[0]
                        value = MyCommand.split("=")[1]
                        if key == "align":
                            if value == "right":
                                header_line = header_line + ("{:>" + str(length) + "}").format(my_header)
                            elif value == "center":
                                header_line = header_line + ("{:^" + str(length) + "}").format(my_header)
                            elif value == "left":
                                header_line = header_line + ("{:<" + str(length) + "}").format(my_header)
                            else:
                                header_line = header_line + ("{:<" + str(length) + "}").format(my_header)
                else:
                    header_line = header_line + ("{:<" + str(length) + "}").format(my_header)
                i_col = i_col + 1
            self.Print("┃ " + ("{:<" + str(line_length) + "}").format(header_line) + " ┃", text_format=text_format,
                    indent=indent)
            self.Print(inter_middle_separator_line, text_format=text_format, indent=indent)

        # datas
        if len(datas) > 0:
            for my_data_line in datas:
                data_line = ""
                i_col = 0
                if type(my_data_line) is list:
                    # Tableau a 2 dimensions
                    for my_data in my_data_line:
                        length = field_lengths[i_col]
                        if len(data_line) > 0:
                            data_line = data_line + column_separator

                        if "|" in my_data:
                            tab_my_data = my_data.split("|")
                            my_data = tab_my_data[0].strip()
                            for MyCommand in tab_my_data[1].split(","):
                                key = MyCommand.split("=")[0]
                                value = MyCommand.split("=")[1]
                                if key == "align":
                                    if value == "right":
                                        data_line = data_line + ("{:>" + str(length) + "}").format(my_data)
                                    elif value == "center":
                                        data_line = data_line + ("{:^" + str(length) + "}").format(my_data)
                                    elif value == "left":
                                        data_line = data_line + ("{:<" + str(length) + "}").format(my_data)
                                    else:
                                        data_line = data_line + ("{:<" + str(length) + "}").format(my_data)
                        else:
                            data_line = data_line + ("{:<" + str(length) + "}").format(my_data)
                        i_col = i_col + 1
                else:
                    # Tableau a 1 dimension
                    length = field_lengths_printable[i_col]
                    if "|" in my_data_line:
                        tab_my_data = my_data_line.split("|")
                        my_data_line = tab_my_data[0].strip()
                        for MyCommand in tab_my_data[1].split(","):
                            key = MyCommand.split("=")[0]
                            value = MyCommand.split("=")[1]
                            if key == "align":
                                if value == "right":
                                    data_line = data_line + ("{:>" + str(length) + "}").format(my_data_line)
                                elif value == "center":
                                    data_line = data_line + ("{:^" + str(length) + "}").format(my_data_line)
                                elif value == "left":
                                    data_line = data_line + ("{:<" + str(length) + "}").format(my_data_line)
                                else:
                                    data_line = data_line + ("{:<" + str(length) + "}").format(my_data_line)
                    else:
                        data_line = data_line + ("{:<" + str(length) + "}").format(my_data_line)

                my_color = ""
                if text_format in self._STYLE_COLORS:
                    my_color = self._STYLE_COLORS[text_format]
                else:
                    if text_format in self._COLORS:
                        my_color = self._COLORS[text_format]

                self.Print("┃ " + ("{:<" + str(line_length) + "}").format(data_line) + my_color + " ┃",
                        text_format=text_format,
                        indent=indent)

        # Pied
        if len(footer) > 0:
            self.Print(inter_bottom_separator_line, text_format=text_format, indent=indent)
            self.Print("┃ " + ("{:>" + str(line_length) + "}").format(footer) + " ┃", text_format=text_format, indent=indent)
            self.Print(last_separator_line_footer, text_format=text_format, indent=indent)
        else:
            self.Print(last_separator_line_data, text_format=text_format, indent=indent)


    def Read(self, question: str, default: str="", text_format: str="CYAN", indent: int=0, newline: bool=False):
        if default != "":
            question = question + " [" + default + "]"
        question = question + " :"
        self.Print(text=question, text_format=text_format, indent=indent, newline=newline)
        response = input()
        if response == "":
            response = default
        return response


    def ReadChoice(self, title: str="", choices: list=[], question: str="", text_format: str="CYAN", indent: int=0):
        options = ""
        if len(choices) == 1:
            # S'il n'y a qu'un choix possible, on le selectionne automatiquement
            retour = choices[0]['value']
        else:
            if title != "":
                self.Print(text=title, text_format=text_format, indent=indent)

            i = 1
            for my_item in choices:
                self.Print(str(i) + " : " + str(my_item['text']), text_format, indent + 2)
                if options == "":
                    options = str(i)
                else:
                    options = options + " " + str(i)
                i = i + 1

            choix_ok = False
            response = ""
            while not choix_ok:
                if question == "":
                    question = "Faites un choix parmi (" + options + ") ou 'Entree'  pour sortir : "

                response = self.Read(question=question, text_format=text_format, indent=indent)
                if response == "" or (response.isnumeric() and int(response) in range(1, i)):
                    choix_ok = True
                else:
                    self.Print("Choisissez parmi les valeurs proposées (" + options + ")", "ERROR")

            if response == "":
                self.Print("==> Abandon.", "BOLD")
                sys.exit(255)
            else:
                retour = choices[int(response) - 1]['value']

        return retour

console = Console()
