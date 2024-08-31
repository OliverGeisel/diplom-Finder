# -*- coding: utf-8 -*-

from __future__ import annotations

import enum
from abc import ABC
from typing import Self

from .DiplomaAnswer import DiplomaAnswers, DiplomaAnswer, DiplomaAnswerSpiel
from .Satz import Satz
from .Spiel_120 import Spiel

VOLLE = "volle"
RÄUMER = "räumer"
ALLES = "alles"


class DiplomaType(enum.IntEnum):
    FRAME = 1
    FRAME_R = 2
    FRAME_REPEAT_MIN = 3
    RESULT_EXACT = 4
    FRAME_SEQUENCE = 5
    FRAME_SEQUENCE_R = 6

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
            case "FRAME_SEQUENCE":
                return DiplomaType.FRAME_SEQUENCE
            case "FRAME_SEQUENCE_R":
                return DiplomaType.FRAME_SEQUENCE_R
            case _:
                return None


def _is_block_free(satz: Satz, start: int, end: int) -> bool:
    """
    Check if a block is free in a Satz
    :param satz: Satz to check
    :type satz:  Satz
    :param start:  Startindex
    :type start:  int
    :param end: Endindex (exklusiv)
    :type end:  int
    :return:  True if block is free
    :rtype:  bool
    """
    return satz.blocked[start:end].count(True) == 0


class Diploma(ABC):

    def __init__(self, diploma_type: DiplomaType, title: str, priority: int = 0):
        self.type: DiplomaType = diploma_type
        self.title = title
        self.priority = priority

    def __eq__(self, other) -> bool:
        if other is None or not isinstance(other, Diploma):
            return False
        return self.title == other.title and self.type == other.type and self.priority == other.priority

    def __hash__(self) -> int:
        return super().__hash__() + hash(self.title) + hash(self.type)

    def check(self, element) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaSpiel(Diploma, ABC):
    def check(self, element: Spiel) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaSatz(Diploma, ABC):

    def check(self, element: Satz) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaFrame(DiplomaSatz):
    """ Ein Frame-Diplom ist ein Diplom, das eine Summe in einer bestimmten Anzahl von Würfen erreicht wird.
    Dabei gibt die size, die Anzahl der Würfe und value den Wert, der mindestens erreicht werden muss.
    Beispiel: size=3; value = 26
    ▶️ 9,9,8
    ▶️ 9,9,9
    """

    def __init__(self, diploma_type: DiplomaType, title: str, size: int, value: int, priority: int = 1):
        super().__init__(diploma_type, title, priority=priority)
        self.size = size
        self.value = value

    def check(self, satz: Satz) -> DiplomaAnswers:
        würfe = satz.volle + satz.abräumer
        back = DiplomaAnswers()
        for i in range(len(würfe) - self.size):
            start = i
            end = i + self.size
            if not _is_block_free(satz, start, end):
                continue
            folge = würfe[start:end]
            if sum(folge) >= self.value:
                absolut_wurf = start + 1
                bereich = VOLLE if absolut_wurf <= 15 else RÄUMER
                back.add(DiplomaAnswer(satz.number, absolut_wurf, bereich, self.title, folge))
                satz.block(start, end)
        return back


class DiplomaFrameSequenz(DiplomaSatz):
    """Diplom, das eine genaue Abfolge von Würfen benötigt.
    """

    def check(self, element: Satz) -> DiplomaAnswers:
        raise NotImplementedError("Nicht Implementiert")


class DiplomaFrameSequenzR(DiplomaSatz):
    """Diplom, das eine genaue Abfolge von Würfen benötigt. Dieses Diplom ist nur in Räumer gültig"""

    def __init__(self, diploma_type: DiplomaType, title: str, size, sequenz, strict: bool, priority: int = 1):
        super().__init__(diploma_type, title, priority=priority)
        self.size = size
        self.sequenz = sequenz
        self.strict = strict

    def check(self, element: Satz) -> DiplomaAnswers:
        würfe = element.abräumer
        back = DiplomaAnswers()
        for i in range(0, len(würfe) - self.size):
            start = i
            end = i + self.size
            if not _is_block_free(element, start + 15, end + 15):
                continue
            folge_davor = würfe[0:max(i - 1, 1)]
            if ((self.strict and (sum(folge_davor) % 9) == 0 and würfe[start:end] == self.sequenz)
                    or (not self.strict and würfe[start:end] == self.sequenz)):
                absolut_wurf = 16 + i
                bereich = RÄUMER
                back.add(DiplomaAnswer(element.number, absolut_wurf, bereich, self.title, self.sequenz))
                element.block(start + 15, end + 15)
        return back


class DiplomaFrameR(DiplomaSatz):
    """
    Ein Frame-Diplom, das aber nur in Räumern gilt. Sonst gilt alle was für ein normales Frame gilt.
    Siehe DiplomaFrame

    """

    def __init__(self, diploma_type: DiplomaType, title: str, size: int, value: int, priority: int = 1):
        super().__init__(diploma_type, title, priority=priority)
        self.size = size
        self.value = value

    def check(self, satz: Satz) -> DiplomaAnswers:
        würfe = satz.abräumer
        back = DiplomaAnswers()
        for i in range(len(würfe) - self.size):
            start = i
            end = i + self.size
            if not _is_block_free(satz, start + 15, end + 15):
                continue
            folge = würfe[start:end]
            if sum(folge) >= self.value:
                absolut_wurf = start + 16
                bereich = RÄUMER
                back.add(DiplomaAnswer(satz.number, absolut_wurf, bereich, self.title, folge))
                satz.block(start + 15, end + 15)
        return back


class DiplomaFrameRepeatMin(DiplomaSatz):
    """
    Ein Diplom, bei dem eine bestimmte Zahl bei jedem Wurf erreicht werden muss.
    Beispiel: size =3; number = 7;
    ▶️ 7,7,7,7
    ▶️ 7,7,7
    """

    def __init__(self, diploma_type: DiplomaType, title: str, size: int, number: int, priority: int = 1):
        super().__init__(diploma_type, title, priority=priority)
        self.size = size
        self.number = number

    def check(self, element: Satz) -> DiplomaAnswers:
        würfe = element.volle + element.abräumer
        back = DiplomaAnswers()
        max_index = len(würfe) - 1
        if max_index < self.size - 1:
            return back
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
                    back.add(DiplomaAnswer(element.number, absolut_wurf, bereich=bereich, title=self.title,
                                           folge=[self.number] * j))
                i += j
            i += 1
        return back


class DiplomaResultExact(DiplomaSpiel):
    """
    Ein Diplom, das ein ganzes Spiel auswertet.
    Es gibt verschiedene Felder die beobachtet werden können.
    Diese sind:
    - VOLLE: Die Summe aller Volle
    - RÄUMER: Die Summe aller Räumer
    - ALLES: Die Summe aller Würfe
    - FEHLER: Die Anzahl der Fehlwürfe
    - VOLLE-ZAHL: Es wurde eine bestimmte Holzzahl in einem Wurf in den Vollen geworfen (z.B. 9)
    Der count gibt an, wie oft etwas auftreten muss.
    Counting hingegen, was aufgezählt werden soll.

    Beispiel: 120 Wurf; count = 0; counting = 0; field = FEHLER
    Es darf keinen Fehlwurf geben.
    """

    def __init__(self, diploma_type: DiplomaType, title: str, count: int, counting: str, field: str, priority: int = 1):
        super().__init__(diploma_type, title, priority=priority)
        self.count = count
        self.counting = counting
        self.field = field

    def check(self, spiel: Spiel) -> DiplomaAnswers:
        back = DiplomaAnswers()
        match self.field:
            case "VOLLE":
                if spiel.get_volle() == self.count:
                    back.add(DiplomaAnswerSpiel(self.title))
            case "RÄUMER":
                if spiel.get_räumer() == self.count:
                    back.add(DiplomaAnswerSpiel(self.title))
            case "ALLES":
                if spiel.get_sum() == self.count:
                    back.add(DiplomaAnswerSpiel(self.title))
            case "FEHLER":
                if spiel.get_fehlwürfe() == 0:
                    back.add(DiplomaAnswerSpiel(self.title))
            case "VOLLE-ZAHL":
                if spiel.get_anzahl_holz(int(self.counting)) == self.count:
                    back.add(DiplomaAnswerSpiel(self.title))
        return back
