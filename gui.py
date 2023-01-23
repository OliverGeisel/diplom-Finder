import json
import pathlib
from typing import List

import PySimpleGUI as gui

from spiel import Spiel120, DiplomaAnswers, DiplomaType
from spiel.Diploma import DiplomaFRAME

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
    layout = [[gui.Frame("Infos", layout=meta_layout, key="frame-meta")],
              [gui.Frame("Spiel", layout=spiel_frame, key="frame-spiel")], [gui.B("AUSWERTEN", key="AUSWERTEN")]]
    return gui.Window("Neuer Spielbericht", layout=layout, size=(750, 400), resizable=True,
                      auto_size_text=True,
                      auto_size_buttons=True)


def eval_spiel(values: dict, window: gui.Window):
    global diplomas
    spiel = Spiel120()
    spiel.init(values)
    result = DiplomaAnswers()
    for diploma in diplomas:
        result_temp = spiel.analyze(diploma)
        result = result + result_temp
    result.print()
    for answer in result.answers:
        feld: gui.Spin = window[f"wurf-{answer.satz}-{answer.bereich}-{answer.bereich_wurf}"]


def parse_diploma(diploma: dict):
    dtype = DiplomaType.value_of(diploma["type"])
    params: dict = diploma["type-parameters"]
    match dtype:
        case DiplomaType.FRAME:
            return DiplomaFRAME(dtype, int(params["frame-size"]), int(params["value"]))
        case _:
            raise TypeError()


def run_new_window(window: gui.Window):
    global diplomas
    diploma_path = pathlib.Path("diplomas.json")
    with diploma_path.open("r") as diploma_file:
        diploma_json = json.loads(diploma_file.read())
    for diploma in diploma_json:
        # todo enable all types
        if diploma["type"] == "FRAME":
            diplomas.append(parse_diploma(diploma))
    while True:
        event, values = window.read()
        if event == "AUSWERTEN":
            eval_spiel(values, window)
        else:
            return


def create_start_window() -> gui.Window:
    layout = [[gui.Button("Neues Spiel analysieren", key="NEU")], [gui.Button("Info", key="INFO")]]
    return gui.Window("Diplom-Finder", layout=layout, size=(300, 200))


def run_start(window: gui.Window):
    while True:
        event, values = window.read()
        command = None
        new_window = None
        if event == "NEU":
            new_window = create_new_window()
            command = run_new_window
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
