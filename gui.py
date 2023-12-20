# -*- coding: utf-8 -*-

import json
import pathlib
from datetime import datetime
from typing import List

import PySimpleGUI as gui

import csv_parse
from logic import parse_diploma, eval_spiel_print_in_window, eval_spiel_from_input, eval_spiel_einzel
from spiel import Spiel120
from spiel.DiplomaBig import DiplomaBig

with pathlib.Path("settings.json").open() as settings_file:
    settings = json.loads(settings_file.read())
DIPLOMAS = set()


def create_spiel_frame() -> List[List]:
    back = list()
    for i in range(1, 5):
        satz_layout = list()
        number_lane = [gui.T("Wurf"), gui.HSeparator()]
        number_lane.extend([gui.T(f"{x}", size=(3,)) for x in range(1, 16)])
        satz_layout.append(number_lane)
        # volle
        volle_lane = [gui.T("Volle"), gui.HSeparator()]
        for wurf in range(1, 16):
            volle_lane.append(gui.Spin(values=[v for v in range(10)], key=f"wurf-{i}-volle-{wurf}", size=(2, 1)))
        satz_layout.append(volle_lane)
        räumer_lane = [gui.T("Räumer"), gui.HSeparator()]
        for wurf in range(1, 16):
            räumer_lane.append(gui.Spin(values=[v for v in range(10)], key=f"wurf-{i}-räumer-{wurf}", size=(2, 1)))
        satz_layout.append(räumer_lane)
        back.append([gui.Frame(f"Satz {i}", key=f"frame-satz-{i}", layout=satz_layout, expand_x=True, expand_y=True)])
    return back


def create_new_window() -> gui.Window:
    menu_def = [
        ['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
        ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo', 'Options::this_is_a_menu_key'], ],
        ['&Toolbar', ['---', 'Command &1', 'Command &2',
                      '---', 'Command &3', 'Command &4']],
        ['&Help', ['&About...']]
    ]
    [gui.Menubar(menu_def)]
    meta_layout = [[gui.Text("Spieler Name: "), gui.Input("", key="spieler-name")]]
    spiel_frame = create_spiel_frame()
    layout = [[gui.Column([[gui.Frame("Infos", layout=meta_layout, key="frame-meta")],
                           [gui.Frame("Spiel", layout=spiel_frame, key="frame-spiel")],
                           [gui.B("AUSWERTEN", key="AUSWERTEN")]], expand_x=True, expand_y=True, size=(900, 500),
                          scrollable=True, vertical_scroll_only=True),
               gui.Column([[gui.Frame("Diplome", key="frame-diplome",
                                      size=(600, 500), expand_x=True, expand_y=True,
                                      layout=[[gui.Text("", key="diplome-feld")]])
                            ], [gui.Button("Leeren", key="DIPLOME-LEEREN")]
                           ],
                          expand_x=True, expand_y=True, size=(600, 500), scrollable=True),
               ]]
    return gui.Window("Neuer Spielbericht", layout=layout, size=(1220, 550), resizable=True,
                      auto_size_text=True,
                      auto_size_buttons=True, font="14", scaling=1.3)


def run_new_window(window: gui.Window):
    # main loop
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            eval_spiel_from_input(values, window, DIPLOMAS, values["spieler-name"])
        elif event == "DIPLOME-LEEREN":
            window["diplome-feld"].update("")
        else:
            return


def load_diplomas(diplomas_set: set):
    diploma_path = pathlib.Path("diplomas.json")
    with diploma_path.open("r", encoding="utf-8-sig") as diploma_file:
        diploma_json = json.loads(diploma_file.read())
    for diploma in diploma_json:
        try:
            diplomas_set.add(parse_diploma(diploma))
        except TypeError:
            pass


def create_start_window() -> gui.Window:
    layout = [[gui.Button("Neues Spiel analysieren", key="NEU")], [gui.B("Aus CSV", key="CSV")],
              [gui.Button("Team CSV", key="TEAM")],
              [gui.Button("Komplettauswertung", key="KOMPLETTAUSWERTUNG")],
              [gui.Button("Info", key="INFO")]]
    return gui.Window("Diplom-Finder", layout=layout, size=(300, 200))


def display_spiel(spiel: Spiel120, window: gui.Window):
    for satz_num, satz in enumerate([spiel.satz1, spiel.satz2, spiel.satz3, spiel.satz4], 1):
        for wurf_num, wurf in enumerate(satz.volle, 1):
            window[f"wurf-{satz_num}-volle-{wurf_num}"].update(wurf)
        for wurf_num, wurf in enumerate(satz.abräumer, 1):
            window[f"wurf-{satz_num}-räumer-{wurf_num}"].update(wurf)


def create_csv_window() -> gui.Window:
    window = gui.Window("Spielbericht aus CSV", resizable=True,
                        layout=[[create_spiel_frame()], [gui.B("Aktualisieren", key="AUSWERTEN")], [
                            gui.Frame("Diplome", key="frame-diplome", expand_x=True, expand_y=True,
                                      layout=[[gui.Text("Bisher KEINE DIPLOME!", key="diplome-feld")]])
                        ]])
    window.finalize()
    return window


def run_csv_window(window: gui.Window):
    path = gui.PopupGetFile("Welches File soll gewählt werden?")
    file = pathlib.Path(path)
    if file is None:
        return
    while not (file.is_file() or file.suffix == ".csv"):
        if file is None:
            return
        path = gui.PopupGetFile("Welches File soll gewählt werden?")
        file = pathlib.Path(path)
    spiel = csv_parse.parse_csv(file)
    display_spiel(spiel, window)
    eval_spiel_print_in_window(spiel, window, DIPLOMAS)
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            window["diplome-feld"].update("")
            eval_spiel_from_input(values, window, DIPLOMAS)
        else:
            return


def create_team_window() -> gui.Window:
    layout = [[gui.FolderBrowse("Ordner", key="folder", initial_folder=settings["start_path"]),
               gui.B("Auswerten", key="AUSWERTEN"), gui.B("Leeren", key="LEEREN")],
              [gui.Frame("Diplome", key="frame-diplome", expand_y=True, expand_x=True,
                         layout=[[
                             gui.Col(scrollable=True, size=(400, 50), expand_x=True, expand_y=True,
                                     vertical_scroll_only=True,
                                     layout=[[gui.Text("Bisher KEINE DIPLOME!", key="diplome-feld")]])]])]
              ]
    window = gui.Window("Team auswerten - CSV", resizable=True,
                        layout=layout)
    window.finalize()
    return window


def run_team_window(window: gui.Window):
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            folder = pathlib.Path(values["folder"])
            if not folder.exists() or pathlib.Path() == folder:
                gui.popup_error("Es gab keinen gültigen Ordner bitte neu wählen!", title="Fehler - Fehlender Ordner!")
                continue
            players = [x.name.replace(",", " ") for x in folder.iterdir()]
            player_folders = [x for x in folder.iterdir()]
            for index, folder in enumerate(player_folders):
                name = players[index]
                game_file_path: pathlib.Path = folder.joinpath("werte.csv")
                if not game_file_path.exists():
                    print(f"Die Datei {game_file_path} existiert nicht!")
                    continue
                spiel = csv_parse.parse_csv(game_file_path)
                eval_spiel_print_in_window(spiel, window, DIPLOMAS, name)
        elif event == "LEEREN":
            window["diplome-feld"].update("Bisher KEINE DIPLOME!")
        else:
            return


def create_complete_window() -> gui.Window:
    layout = [
        [
            gui.Text("Mannschaft-Pattern:"),
            gui.Input(
                tooltip="Hier ist der Name der Mannschaft zum Auswerten. Der angegebene String wird geprüft, ob er in der Mannschaft enthaltene ist.",
                key="team-pattern")],
        [gui.FolderBrowse("Ordner", key="folder", initial_folder=settings["start_path"])],
        [gui.Button("Auswerten", key="AUSWERTEN")]
    ]
    return gui.Window("Komplettauswertung", layout=layout)
    pass


def auswerten_all(pattern: str, folder: pathlib.Path):
    date_format = "%d.%m.%Y"
    diplome_pro_spieler: dict[str, list[DiplomaBig]] = dict()
    pattern_clean = pattern.upper().strip()
    if pattern_clean is None or pattern_clean in ["", " "] or len(pattern_clean) < 3:
        gui.popup_error("Es gab keinen gültigen Pattern bitte neu wählen!", title="Fehler - Fehlender Pattern!")
        return
    folder = pathlib.Path(folder)
    if not folder.exists() or pathlib.Path() == folder:
        gui.popup_error("Es gab keinen gültigen Ordner bitte neu wählen!", title="Fehler - Fehlender Ordner!")
        return
    for date in folder.iterdir():
        date_string = date.name
        try:
            parsed_date = datetime.strptime(date_string, date_format).date()
        except ValueError as e:
            print("Error:", e)
            continue
        for game in date.iterdir():  # check each game at the date
            if not game.is_dir():
                continue
            for team in game.iterdir():
                if not team.is_dir() or team.name == "Backup-Daten" or pattern_clean not in team.name.upper():
                    continue
                for player in team.iterdir():
                    if not player.is_dir():
                        continue
                    game_file_path: pathlib.Path = player.joinpath("werte.csv")
                    if not game_file_path.exists():
                        print(f"Die Datei {game_file_path} existiert nicht!")
                        continue
                    spiel = csv_parse.parse_csv(game_file_path)
                    if not spiel.is_valid():
                        continue
                    spieler = player.name
                    diplome = eval_spiel_einzel(spiel, DIPLOMAS, spieler)
                    if diplome.is_leer():
                        continue
                    if spieler not in diplome_pro_spieler.keys():
                        diplome_pro_spieler[spieler] = list()
                    diplome_pro_spieler[spieler].append(DiplomaBig(parsed_date, team.name, diplome))
    csv_parse.export_to_csv(diplome_pro_spieler, "komplett")
    gui.popup_ok("Die Auswertung ist abgeschlossen!", title="Auswertung abgeschlossen!")
    order = dict()
    for key, value in diplome_pro_spieler.items():
        i = 0
        for diploma in value:
            i += diploma.get_diplome_anzahl()
        order[key] = i
    res = sorted(order.items(), key=lambda x: x[1], reverse=True)
    for i in res:
        print(i)
    # export_docx(list(diplome_pro_spieler.keys())[0], list(diplome_pro_spieler.values())[0][0])


def run_complete_window(window: gui.Window):
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            pattern: str = values["team-pattern"]
            auswerten_all(pattern, values["folder"])
        else:
            return


def run_start(window: gui.Window):
    global DIPLOMAS
    load_diplomas(DIPLOMAS)
    while True:
        event, values = window.read()
        command: callable
        new_window: gui.Window
        if event == "NEU":
            new_window = create_new_window()
            command = run_new_window
            window.close()
        elif event == "CSV":
            new_window = create_csv_window()
            command = run_csv_window
            window.close()
        elif event == "KOMPLETTAUSWERTUNG":
            new_window = create_complete_window()
            command = run_complete_window
            window.close()
        elif event == "TEAM":
            new_window = create_team_window()
            command = run_team_window
            window.close()
        elif event == "INFO":
            gui.Popup(f"""
Hier ist leider nix besonderes! 🤨🫡
Version 1.1!
©️Oliver Geisel
""")
            continue
        else:
            return
        if command is not None and new_window is not None:
            command(new_window)
        else:
            gui.Popup("Upps! Hier ist was schief gegangen. Die Aktion ist nicht ausführbar")
        continue
