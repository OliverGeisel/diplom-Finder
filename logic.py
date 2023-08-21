# -*- coding: utf-8 -*-

import PySimpleGUI as gui

from spiel import DiplomaType, Spiel120, DiplomaAnswers
from spiel.Diploma import DiplomaFrame, DiplomaFrameRepeatMin, DiplomaFrameR, Diploma, DiplomaSpiel, DiplomaResultExact


def eval_spiel(spiel: Spiel120, window: gui.Window, diplomas: set, name: str = ""):
    result = DiplomaAnswers(name)
    for diploma in diplomas:
        if isinstance(diploma, DiplomaSpiel):
            result_temp = diploma.check(spiel)
            result = result + result_temp
        else:
            for satz in spiel.get_alle_sätze():
                result_temp = diploma.check(satz)
                result = result + result_temp
    result.print()
    # for answer in result.answers:
    #     feld: gui.Spin = window[f"wurf-{answer.satz}-{answer.bereich}-{answer.bereich_wurf}"]
    diplome_layout = list()
    text = window["diplome-feld"].get()
    text = "" if text in ["Bisher KEINE DIPLOME!", "KEINE DIPLOME Gefunden!"] else text
    for answer in result.answers:
        text += f"""{result.name} - Diplom: {answer.title} in Satz {answer.satz} und ab Wurf {answer.absolut_wurf}
        {answer.folge}
"""
    text = "KEINE DIPLOME Gefunden!" if text == "" else text
    window["diplome-feld"].update(value=text)
    # todo clean by rerun or disable
    # window.extend_layout(window["frame-diplome"], diplome_layout)


def eval_spiel_from_input(values: dict, window: gui.Window, diplomas, name: str = ""):
    """

    :param name:
    :type name:
    :param values:
    :type values:
    :param window:
    :type window:
    :param diplomas:
    :type diplomas:
    :return:
    :rtype:
    """
    spiel = Spiel120()
    spiel.init(values)
    eval_spiel(spiel, window, diplomas, name)


def parse_diploma(diploma: dict) -> Diploma:
    """
    Parse a diploma with a specific type from a dict

    :param diploma: diploma dict
    :type diploma: dict
    :return: Diploma from dict
    :rtype: Diploma
    :exception: TypeError
    """
    dtype = DiplomaType.value_of(diploma["type"])
    params: dict = diploma["type-parameters"]
    title: str = diploma["name"]
    match dtype:
        case DiplomaType.FRAME:
            return DiplomaFrame(dtype, title, int(params["frame-size"]), int(params["value"]))
        case DiplomaType.FRAME_REPEAT_MIN:
            return DiplomaFrameRepeatMin(dtype, title, int(params["frame-size"]), int(params["number"]))
        case DiplomaType.FRAME_R:
            return DiplomaFrameR(dtype, title, int(params["frame-size"]), int(params["value"]))
        case DiplomaType.RESULT_EXACT:
            return DiplomaResultExact(dtype, title, params["count"], params["counting"], params["field"])
        case _:
            raise TypeError()
