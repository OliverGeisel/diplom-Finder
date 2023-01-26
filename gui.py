# -*- coding: utf-8 -*-

import json
import pathlib
from typing import List

import PySimpleGUI as gui

import csv_parse
from logic import parse_diploma, eval_spiel, eval_spiel_from_input
from spiel import Spiel120

diplomas = set()


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
            volle_lane.append(gui.Spin(values=[i for i in range(11)], key=f"wurf-{i}-volle-{wurf}", size=(2, 1)))
        satz_layout.append(volle_lane)
        räumer_lane = [gui.T("Räumer"), gui.HSeparator()]
        for wurf in range(1, 16):
            räumer_lane.append(gui.Spin(values=[i for i in range(11)], key=f"wurf-{i}-räumer-{wurf}", size=(2, 1)))
        satz_layout.append(räumer_lane)
        back.append([gui.Frame(f"Satz {i}", key=f"frame-satz-{i}", layout=satz_layout, expand_x=True, expand_y=True)])
    return back


def create_new_window() -> gui.Window:
    meta_layout = [[gui.Text("Spieler Name: "), gui.Input("", key="spieler-name")]]
    spiel_frame = create_spiel_frame()
    layout = [[gui.Column([[gui.Frame("Infos", layout=meta_layout, key="frame-meta")],
                           [gui.Frame("Spiel", layout=spiel_frame, key="frame-spiel")],
                           [gui.B("AUSWERTEN", key="AUSWERTEN")]], expand_x=True, expand_y=True, size=(1000, 500),
                          scrollable=True, vertical_scroll_only=True),
               gui.Frame("Diplome", key="frame-diplome", layout=[[gui.Text("", key="diplome-feld")]])]]
    return gui.Window("Neuer Spielbericht", layout=layout, size=(1220, 550), resizable=True,
                      auto_size_text=True,
                      auto_size_buttons=True, font="14", scaling=1.5)


def run_new_window(window: gui.Window):
    global diplomas
    load_diplomas(diplomas)
    # main loop
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            eval_spiel_from_input(values, window, diplomas)
        else:
            return


def load_diplomas(diplomas: set):
    diploma_path = pathlib.Path("diplomas.json")
    with diploma_path.open("r", encoding="utf-8-sig") as diploma_file:
        diploma_json = json.loads(diploma_file.read())
    for diploma in diploma_json:
        # todo enable all types
        try:
            diplomas.add(parse_diploma(diploma))
        except:
            pass


def create_start_window() -> gui.Window:
    layout = [[gui.Button("Neues Spiel analysieren", key="NEU")], [gui.B("Aus CSV", key="CSV")],
              [gui.Button("Info", key="INFO")]]
    return gui.Window("Diplom-Finder", layout=layout, size=(300, 200))


def display_spiel(spiel: Spiel120, window: gui.Window):
    for satz_num, satz in enumerate([spiel.satz1, spiel.satz2, spiel.satz3, spiel.satz4], 1):
        for wurf_num, wurf in enumerate(satz.volle, 1):
            window[f"wurf-{satz_num}-volle-{wurf_num}"].update(wurf)
        for wurf_num, wurf in enumerate(satz.abräumer, 1):
            window[f"wurf-{satz_num}-räumer-{wurf_num}"].update(wurf)


def create_csv_window() -> gui.Window:
    global diplomas
    load_diplomas(diplomas)
    window = gui.Window("Spielbericht aus CSV",
                        layout=[[create_spiel_frame()], [gui.B("Aktualisieren", key="AUSWERTEN")], [
                            gui.Frame("Diplome", key="frame-diplome",
                                      layout=[[gui.Text("KEINE DIPLOME!", key="diplome-feld")]])]])
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
    eval_spiel(spiel, window, diplomas)
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            eval_spiel_from_input(values, window, diplomas)
        else:
            return


def run_start(window: gui.Window):
    while True:
        event, values = window.read()
        command = None
        new_window = None
        if event == "NEU":
            new_window = create_new_window()
            command = run_new_window
            window.close()
        elif event == "CSV":
            new_window = create_csv_window()
            command = run_csv_window
            window.close()
        elif event == "INFO":
            gui.Popup(f"""
Hier ist leider nix besonderes! 🤨🫡
Version 1.0!
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
