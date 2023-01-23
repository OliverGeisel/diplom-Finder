from __future__ import annotations

import enum
from abc import ABC
from typing import Self, List

from .Satz import Satz

VOLLE = "volle"
RÄUMER = "räumer"


class DiplomaAnswer:

    def __init__(self, satz: int, absolut_wurf: int, bereich: str, title):
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
        self.title = title

    def print(self):
        print(f"Satz:{self.satz}-{self.absolut_wurf}-{self.title}")


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
    FRAME_REPEAT_MIN = 3
    RESULT_EXACT = 4

    @staticmethod
    def value_of(name: str) -> Self | None:
        match name.upper().replace("-", "_"):
            case "FRAME":
                return DiplomaType.FRAME
            case "FRAME_R":
                return DiplomaType.FRAME_R
            case "FRAME_REPEAT_MIN":
                return DiplomaType.FRAME_REPEAT_MIN
            case "RESULT_EXACT":
                return DiplomaType.RESULT_EXACT
            case _:
                return None


class Diploma(ABC):

    def __init__(self, diploma_type: DiplomaType, title: str):
        self.type: DiplomaType = diploma_type
        self.title = title

    def check(self, element) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaSpiel(Diploma, ABC):
    def check(self, element) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaSatz(Diploma, ABC):

    def check(self, element: Satz) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaFRAME(DiplomaSatz):

    def __init__(self, diploma_type: DiplomaType, title: str, size: int, value: int):
        super().__init__(diploma_type, title)
        self.size = size
        self.value = value

    def check(self, satz: Satz) -> DiplomaAnswers:
        würfe = satz.volle + satz.abräumer
        back = DiplomaAnswers()
        for i in range(len(würfe) - self.size):
            if sum(würfe[i:i + self.size]) >= self.value:
                absolut_wurf = i + 1
                bereich = VOLLE if absolut_wurf <= 15 else RÄUMER
                back.add(DiplomaAnswer(satz.number, absolut_wurf, bereich, self.title))
        return back


class DiplomaFrameR(DiplomaSatz):

    def __init__(self, diploma_type: DiplomaType, title: str, size: int, value: int):
        super().__init__(diploma_type, title)
        self.size = size
        self.value = value

    def check(self, element: Satz) -> DiplomaAnswers:
        würfe = element.abräumer
        back = DiplomaAnswers()
        for i in range(len(würfe) - self.size):
            if sum(würfe[i:i + self.size]) >= self.value:
                absolut_wurf = i + 1
                bereich = RÄUMER
                back.add(DiplomaAnswer(element.number, absolut_wurf, bereich, self.title))
        return back


class DiplomaFrameRepeatMin(DiplomaSatz):

    def __init__(self, diploma_type: DiplomaType, title: str, size: int, number: int):
        super().__init__(diploma_type, title)
        self.size = size
        self.number = number

    def check(self, element: Satz) -> DiplomaAnswers:
        würfe = element.volle + element.abräumer
        back = DiplomaAnswers()
        max_index = len(würfe) - 1
        i = 0
        while i < 30 - self.size:
            # check if number is the selected
            if würfe[i] == self.number:
                # count repeating's
                j = 1
                count = 1
                while i + j <= max_index and würfe[i + j] == self.number:
                    count += 1
                    j += 1
                if count >= self.size:
                    absolut_wurf = i + 1
                    bereich = VOLLE if absolut_wurf < 16 else RÄUMER
                    back.add(DiplomaAnswer(element.number, absolut_wurf, bereich=bereich, title=self.title))
                i += j
            i += 1
        return back
