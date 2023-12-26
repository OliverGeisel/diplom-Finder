# -*- coding: utf-8 -*-

from __future__ import annotations

import enum
from abc import ABC
from typing import Self

from .DiplomaAnswer import DiplomaAnswers, DiplomaAnswer, DiplomaAnswerSpiel
from .Hit import Hit, VOLLE, RÄUMER
from .Satz import Satz
from .Spiel_120 import Spiel


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


class Diploma(Hit):

    def __init__(self, diploma_type: DiplomaType, name: str):
        super().__init__(name, diploma_type)
        self.type: DiplomaType = diploma_type


class DiplomaSpiel(Diploma, ABC):
    """
    Ein Diplom, das auf ein gesamtes Spiel angewendet wird. Es werden also Gesamtholz oder ähnliches ausgewertet.
    """

    def check(self, element: Spiel) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaSatz(Diploma, ABC):
    """
    Ein Diplom, das auf einen Satz angewendet wird. Es werden also nur die Würfe in einem Satz ausgewertet.
    """

    def check(self, element: Satz) -> DiplomaAnswers:
        raise NotImplementedError("Class has no Implementation")


class DiplomaFrameValue(DiplomaSatz):
    """ Ein Frame-Diplom ist ein Diplom, das eine Summe in einer bestimmten Anzahl von Würfen erreicht wird.
    Dabei gibt die size, die Anzahl der Würfe und value den Wert, der mindestens erreicht werden muss.
    Beispiel: size=3; value = 26
    ▶️ 9,9,8
    ▶️ 9,9,9
    """

    def __init__(self, diploma_type: DiplomaType, name: str, size: int, value: int, greater_equal: bool = True):
        super().__init__(diploma_type, name)
        self.frame_size = size
        self.value = value
        self.greater_equal = greater_equal

    def check(self, satz: Satz) -> DiplomaAnswers:
        würfe = satz.volle + satz.abräumer
        back = DiplomaAnswers()
        for i in range(len(würfe) - self.frame_size):
            folge = würfe[i:i + self.frame_size]
            sum_folge = sum(folge)
            if (self.greater_equal and sum_folge >= self.value) or (not self.greater_equal and sum_folge == self.value):
                absolut_wurf = i + 1
                bereich = VOLLE if absolut_wurf <= 15 else RÄUMER
                back.add(DiplomaAnswer(satz.number, absolut_wurf, bereich, self.name, folge))
        return back


class DiplomaFrameSequenz(DiplomaSatz):
    """Diplom, das eine genaue Abfolge von Würfen benötigt.
    Beispiel: size = 3; sequenz = [9,9,8]
    ▶️ |9,9,8|,9
    ❌ 9,8,9,9
    """

    def __init__(self, diploma_type: DiplomaType, name: str, size, sequenz: list[int]):
        super().__init__(diploma_type, name)
        self.frame_size = size
        self.sequenz = sequenz

    def check(self, satz: Satz) -> DiplomaAnswers:
        würfe = satz.volle + satz.abräumer
        back = DiplomaAnswers()
        for i in range(0, len(würfe) - self.frame_size):
            folge_davor = würfe[0:max(i - 1, 1)]
            if (((sum(folge_davor) % 9) == 0 and würfe[i:i + self.frame_size] == self.sequenz)
                    or würfe[i:i + self.frame_size] == self.sequenz):
                absolut_wurf = 1 + i
                bereich = RÄUMER if absolut_wurf > 15 else VOLLE
                back.add(DiplomaAnswer(satz.number, absolut_wurf, bereich, self.name, self.sequenz))

        return back


class DiplomaFrameSequenzR(DiplomaSatz):
    """Diplom, das eine genaue Abfolge von Würfen benötigt. Dieses Diplom ist nur in Räumer gültig"""

    def __init__(self, diploma_type: DiplomaType, name: str, size, sequenz, strict: bool):
        super().__init__(diploma_type, name)
        self.size = size
        self.sequenz = sequenz
        self.strict = strict

    def check(self, element: Satz) -> DiplomaAnswers:
        würfe = element.abräumer
        back = DiplomaAnswers()
        for i in range(0, len(würfe) - self.size):
            folge_davor = würfe[0:max(i - 1, 1)]
            if ((self.strict and (sum(folge_davor) % 9) == 0 and würfe[i:i + self.size] == self.sequenz)
                    or (not self.strict and würfe[i:i + self.size] == self.sequenz)):
                absolut_wurf = 16 + i
                bereich = RÄUMER
                back.add(DiplomaAnswer(element.number, absolut_wurf, bereich, self.name, self.sequenz))
        return back


class DiplomaFrameValueR(DiplomaSatz):
    """
    Ein Frame-Diplom, das aber nur in Räumern gilt. Sonst gilt alle was für ein normales Frame-Value gilt.
    Siehe DiplomaFrame

    """

    def __init__(self, diploma_type: DiplomaType, name: str, size: int, value: int):
        super().__init__(diploma_type, name)
        self.size = size
        self.value = value

    def check(self, satz: Satz) -> DiplomaAnswers:
        würfe = satz.abräumer
        back = DiplomaAnswers()
        for i in range(len(würfe) - self.size):
            folge = würfe[i:i + self.size]
            if sum(folge) >= self.value:
                absolut_wurf = i + 16
                bereich = RÄUMER
                back.add(DiplomaAnswer(satz.number, absolut_wurf, bereich, self.name, folge))
        return back


class DiplomaFrameRepeatMin(DiplomaSatz):
    """
    Ein Diplom, bei dem eine bestimmte Zahl bei jedem Wurf erreicht werden muss.
    Beispiel: size =3; number = 7;
    ▶️ 7,7,7,7
    ▶️ 7,7,7
    """

    def __init__(self, diploma_type: DiplomaType, name: str, size: int, number: int):
        super().__init__(diploma_type, name)
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
                    back.add(DiplomaAnswer(element.number, absolut_wurf, bereich=bereich, name=self.name,
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

    def __init__(self, diploma_type: DiplomaType, name: str, count: int, counting: str, field: str):
        super().__init__(diploma_type, name)
        self.count = count
        self.counting = counting
        self.field = field

    def check(self, spiel: Spiel) -> DiplomaAnswers:
        back = DiplomaAnswers()
        match self.field:
            case "VOLLE":
                if spiel.get_volle() == self.count:
                    back.add(DiplomaAnswerSpiel(self.name))
            case "RÄUMER":
                if spiel.get_räumer() == self.count:
                    back.add(DiplomaAnswerSpiel(self.name))
            case "ALLES":
                if spiel.get_sum() == self.count:
                    back.add(DiplomaAnswerSpiel(self.name))
            case "FEHLER":
                if spiel.get_fehlwürfe() == 0:
                    back.add(DiplomaAnswerSpiel(self.name))
            case "VOLLE-ZAHL":
                if spiel.get_anzahl_holz(int(self.counting)) == self.count:
                    back.add(DiplomaAnswerSpiel(self.name))
        return back
