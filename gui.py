import json
import pathlib
from typing import List

import PySimpleGUI as gui

import csv_parse
from logic import parse_diploma, eval_spiel, eval_spiel_from_input
from spiel import Spiel120

diplomas = []


def create_spiel_frame() -> List[List]:
    back = list()
    for i in range(1, 5):
        satz_layout = list()
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
                           [gui.B("AUSWERTEN", key="AUSWERTEN")]]),
               gui.Frame("Diplome", key="frame-diplome", layout=[[gui.Text("", key="diplome-feld")]])]]
    return gui.Window("Neuer Spielbericht", layout=layout, size=(1220, 550), resizable=True,
                      auto_size_text=True,
                      auto_size_buttons=True, font="14")


def run_new_window(window: gui.Window):
    global diplomas
    diploma_path = pathlib.Path("diplomas.json")
    with diploma_path.open("r") as diploma_file:
        diploma_json = json.loads(diploma_file.read())
    for diploma in diploma_json:
        # todo enable all types
        try:
            diplomas.append(parse_diploma(diploma))
        except:
            pass
    # main loop
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            eval_spiel_from_input(values, window, diplomas)
        else:
            return


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
    diploma_path = pathlib.Path("diplomas.json")
    with diploma_path.open("r") as diploma_file:
        diploma_json = json.loads(diploma_file.read())
    for diploma in diploma_json:
        # todo enable all types
        try:
            diplomas.append(parse_diploma(diploma))
        except:
            pass
    window = gui.Window("Spielbericht aus CSV", layout=[[create_spiel_frame()], [
        gui.Frame("Diplome", key="frame-diplome", layout=[[gui.Text("", key="diplome-feld")]])]])
    window.finalize()
    return window


def run_csv_window(window: gui.Window):
    spiel = csv_parse.parse_csv(pathlib.Path("werte.csv"))
    display_spiel(spiel, window)
    eval_spiel(spiel, window, diplomas)
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            eval_spiel(values, window, diplomas)
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
            gui.Popup("Hier ist leider nix besonderes! 🤨🫡")
            continue
        else:
            return
        if command is not None and new_window is not None:
            command(new_window)
        else:
            gui.Popup("Upps! Hier ist was schief gegangen. Die Aktion ist nicht ausführbar")
        continue
