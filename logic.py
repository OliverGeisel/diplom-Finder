# -*- coding: utf-8 -*-

import PySimpleGUI as gui

from spiel import DiplomaType, Spiel120, DiplomaAnswers
from spiel.Diploma import DiplomaFrameValue, DiplomaFrameRepeatMin, DiplomaFrameValueR, Diploma, DiplomaSpiel, \
    DiplomaResultExact, \
    DiplomaFrameSequenzR
from spiel.Negative import Negative, NegativeFrameValue, NegativeFrameValueR, NegativeFrameRepeatMin, \
    NegativeFrameSequenzR, NegativeFrameSequenz, NegativeSpiel
from spiel.NegativeAnswers import NegativeAnswers


def eval_spiel_einzel(spiel: Spiel120, diplomas: set, name: str = "", find_negative: bool = False,
                      negatives=None) -> tuple[DiplomaAnswers, NegativeAnswers]:
    """
    Evaluate a Spiel120 and diplomas and return the results.
    :param find_negative:
    :type find_negative:
    :param negatives:
    :type negatives:
    :param spiel: Spiel zum auswerten
    :type spiel: Spiel120
    :param diplomas: Diplome zum auswerten
    :type diplomas: set
    :param name: Name des Spielers
    :type name:  str
    :return: Ergebnisse in einem Tuple (DiplomaAnswers, NegativeAnswers)
    :rtype: tuple[DiplomaAnswers, NegativeAnswers]
    """
    if negatives is None:
        negatives = set()
    diploma_results = DiplomaAnswers(name)
    for diploma in diplomas:
        if isinstance(diploma, DiplomaSpiel):  # check if diploma is a Spiel diploma
            result_temp = diploma.check(spiel)
            diploma_results += result_temp
        else:  # check if diploma is a normal diploma
            for satz in spiel.get_alle_sätze():
                result_temp = diploma.check(satz)
                diploma_results += result_temp
    negative_results = NegativeAnswers(name)
    if find_negative:
        for find_negative in negatives:
            if isinstance(find_negative, NegativeSpiel):
                result_temp = find_negative.check(spiel)
                negative_results += result_temp
            else:
                for satz in spiel.get_alle_sätze():
                    result_temp = find_negative.check(satz)
                    negative_results += result_temp
    return diploma_results, negative_results


def eval_spiel_print_in_window(spiel: Spiel120, window: gui.Window, diplomas: set, name: str = "",
                               find_negative: bool = False):
    """
    Evaluate a Spiel120 and diplomas and print the results to the window.
    :param spiel: Spiel zum auswerten
    :type spiel:
    :param window: Fenster zum Ausgeben
    :type window:
    :param diplomas: Diplome zum auswerten
    :type diplomas:
    :param name: Name des Spielers
    :type name:
    :return:
    :rtype:
    """
    diplomas, negatives = eval_spiel_einzel(spiel, diplomas, name, find_negative)
    diplomas.print()
    # for answer in result.answers:
    #     feld: gui.Spin = window[f"wurf-{answer.satz}-{answer.bereich}-{answer.bereich_wurf}"]
    diplome_layout = list()
    diploma_text = window["diplome-feld"].get()
    diploma_text = "" if diploma_text in ["Bisher KEINE DIPLOME!", "KEINE DIPLOME Gefunden!"] else diploma_text
    for answer in diplomas.answers:
        diploma_text += f"""{diplomas.player_name} - Diplom: {answer.name} in Satz {answer.satz} und ab Wurf {answer.absolut_wurf}
        {answer.folge}
"""
    negative_text = window["negative-feld"].get()
    negative_text = "" if negative_text in ["KEINE NEGATIVE!", "KEINE NEGATIVE Gefunden!"] else negative_text
    for answer in negatives.answers:
        negative_text += f"""{negatives.player_name} - Negative: {answer.name} in Satz {answer.satz} und ab Wurf {answer.absolut_wurf}
        {answer.folge}
"""
    diploma_text = "KEINE DIPLOME Gefunden!" if diploma_text == "" else diploma_text
    negative_text = "KEINE NEGATIVE Gefunden!" if negative_text == "" else negative_text
    window["diplome-feld"].update(value=diploma_text)
    window["negative-feld"].update(value=negative_text)
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
    eval_spiel_print_in_window(spiel, window, diplomas, name)


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
    name: str = diploma["name"]
    match dtype:
        case DiplomaType.FRAME:
            return DiplomaFrameValue(dtype, name, int(params["frame-size"]), int(params["value"]))
        case DiplomaType.FRAME_REPEAT_MIN:
            return DiplomaFrameRepeatMin(dtype, name, int(params["frame-size"]), int(params["number"]))
        case DiplomaType.FRAME_R:
            return DiplomaFrameValueR(dtype, name, int(params["frame-size"]), int(params["value"]))
        case DiplomaType.RESULT_EXACT:
            return DiplomaResultExact(dtype, name, params["count"], params["counting"], params["field"])
        case DiplomaType.FRAME_SEQUENCE_R:
            return DiplomaFrameSequenzR(dtype, name, int(params["frame-size"]), params["sequence"], params["strict"])
        case _:
            raise TypeError()


def parse_negative(negative: dict) -> Negative:
    """
    Parse a list of diplomas from a dict

    :param negative: loaded json as a dict
    :type negative: dict
    """

    name = negative["name"]
    n_type = negative["type"]
    parameters = negative["type-parameters"]
    match n_type:
        case "FRAME":
            return NegativeFrameValue(name, int(parameters["frame-size"]), int(parameters["value"]),
                                      bool(parameters["greater-equal"]))
        case "FRAME_R":
            return NegativeFrameValueR(name, int(parameters["frame-size"]), int(parameters["value"]),
                                       bool(parameters["greater-equal"]))
        case "FRAME_REPEAT_MIN":
            return NegativeFrameRepeatMin(name, int(parameters["frame-size"]), int(parameters["number"]))
        case "FRAME_SEQUENCE":
            return NegativeFrameSequenz(name, int(parameters["frame-size"]), parameters["sequence"])
        case "FRAME_SEQUENCE_R":
            return NegativeFrameSequenzR(name, int(negative["frame-size"]), negative["sequence"], negative["strict"])
        case _:
            raise TypeError()
