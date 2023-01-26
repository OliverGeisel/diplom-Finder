# -*- coding: utf-8 -*-

from pathlib import Path

import pandas

from spiel import Spiel120, Satz


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
