# -*- coding: utf-8 -*-

from pathlib import Path

import pandas

from spiel import Spiel120, Satz
from spiel.DiplomaBig import DiplomaBig


def parse_csv(path: Path) -> Spiel120:
    csv_file = pandas.read_csv(path)
    würfe = csv_file["Anzahl"]
    spiel: Spiel120 = Spiel120()
    satz = Satz(1)
    satz.volle = [x for x in würfe[0:15]]
    satz.abräumer = [x for x in würfe[15:30]]
    spiel.satz1 = satz
    satz = Satz(2)
    satz.volle = [x for x in würfe[30:45]]
    satz.abräumer = [x for x in würfe[45:60]]
    spiel.satz2 = satz
    satz = Satz(3)
    satz.volle = [x for x in würfe[60:75]]
    satz.abräumer = [x for x in würfe[75:90]]
    spiel.satz3 = satz
    satz = Satz(4)
    satz.volle = [x for x in würfe[90:105]]
    satz.abräumer = [x for x in würfe[105:120]]
    spiel.satz4 = satz
    return spiel


def export_to_csv(data: dict[str, list[DiplomaBig]], file_name: str):
    with Path(f"csv/{file_name}.csv", index=False).open("w", encoding="UTF-8") as output:
        output.write("Name;Datum;Diplom;Satz;Absolut-Wurf;Bereich;Folge\n")
        for key, value in data.items():
            name = key.replace(" ", "_").replace(",", " ")
            for diploma in value:
                for answer in diploma.diplomas.answers:
                    output.write(
                        f"{name};{diploma.date};{answer.title};{answer.satz};{answer.absolut_wurf};{answer.bereich};" +
                        f"{str(answer.folge).replace(' ', '').replace(',', '-').removesuffix(']').removeprefix('[')}\n")
