from __future__ import annotations

import enum
from abc import ABC
from typing import Self, List

from .Satz import Satz


class DiplomaAnswer:

    def __init__(self, satz: int, absolut_wurf: int, bereich: str, ):
        """

        :param satz:
        :type satz:
        :param absolut_wurf:
        :type absolut_wurf:
        :param bereich:
        :type bereich:
        """
        self.satz = satz
        self.bereich = bereich
        self.absolut_wurf = absolut_wurf
        self.bereich_wurf = absolut_wurf - 15 if absolut_wurf > 15 else absolut_wurf

    def print(self):
        print(f"Satz:{self.satz}-{self.absolut_wurf}")


class DiplomaAnswers:
    def __init__(self):
        self.answers: List[DiplomaAnswer] = list()

    def add(self, diploma_answer: DiplomaAnswer):
        self.answers.append(diploma_answer)

    def __add__(self, other):
        if not isinstance(other, DiplomaAnswers):
            raise Exception("Type Missmatch")
        back = DiplomaAnswers()
        for i in self.answers:
            back.add(i)
        for i in other.answers:
            back.add(i)
        return back

    def print(self):
        for i in self.answers:
            i.print()


class DiplomaType(enum.IntEnum):
    FRAME = 1
    FRAME_R = 2
    FRAME_SEQUENZ_MIN = 3
    RESULT_EXACT = 4

    @staticmethod
    def value_of(name: str) -> Self | None:
        match name.upper().replace("-", "_"):
            case "FRAME":
                return DiplomaType.FRAME
            case "FRAME_R":
                return DiplomaType.FRAME_R
            case "FRAME_SEQUENZ_MIN":
                return DiplomaType.FRAME_SEQUENZ_MIN
            case "RESULT_EXACT":
                return DiplomaType.RESULT_EXACT
            case _:
                return None


class Diploma(ABC):

    def __init__(self, diploma_type: DiplomaType):
        self.type: DiplomaType = diploma_type

    def check(self, satz: Satz) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaFRAME(Diploma):

    def __init__(self, diploma_type: DiplomaType, size: int, value: int):
        super().__init__(diploma_type)
        self.size = size
        self.value = value

    def check(self, satz: Satz) -> DiplomaAnswers:
        würfe = satz.volle + satz.abräumer
        back = DiplomaAnswers()
        for i in range(len(würfe) - self.size):
            if sum(würfe[i:i + self.size]) >= self.value:
                absolut_wurf = i + 1
                bereich = "volle" if absolut_wurf <=15 else "räumer"
                back.add(DiplomaAnswer(satz.number, absolut_wurf, bereich))
        return back
