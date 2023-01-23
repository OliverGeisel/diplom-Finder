import PySimpleGUI as gui

from spiel import DiplomaType, Spiel120, DiplomaAnswers
from spiel.Diploma import DiplomaFRAME, DiplomaFrameRepeatMin


def eval_spiel(values: dict, window: gui.Window, diplomas):
    spiel = Spiel120()
    spiel.init(values)
    result = DiplomaAnswers()
    for diploma in diplomas:
        result_temp = spiel.analyze(diploma)
        result = result + result_temp
    result.print()
    for answer in result.answers:
        feld: gui.Spin = window[f"wurf-{answer.satz}-{answer.bereich}-{answer.bereich_wurf}"]
    diplome_layout = list()
    text=""
    for answer in result.answers:
        text += f"Diplom: {answer.title} in Satz {answer.satz} und Wurf {answer.absolut_wurf}\n"
    window["diplome-feld"].update(value=text)
    # todo clean by rerun or disable
    #window.extend_layout(window["frame-diplome"], diplome_layout)


def parse_diploma(diploma: dict):
    dtype = DiplomaType.value_of(diploma["type"])
    params: dict = diploma["type-parameters"]
    title: str = diploma["name"]
    match dtype:
        case DiplomaType.FRAME:
            return DiplomaFRAME(dtype, title, int(params["frame-size"]), int(params["value"]))
        case DiplomaType.FRAME_REPEAT_MIN:
            return DiplomaFrameRepeatMin(dtype, title, int(params["frame-size"]), int(params["number"]))
        case _:
            raise TypeError()
