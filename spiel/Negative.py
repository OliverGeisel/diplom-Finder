import enum
from abc import ABC
from typing import Self

from spiel import Satz
from spiel.Answer import Answers
from spiel.Hit import Hit, VOLLE, RÄUMER
from spiel.NegativeAnswers import NegativeAnswers, NegativeAnswer
from spiel.Spiel_120 import Spiel


class NegativeType(enum.IntEnum):
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
                return NegativeType.FRAME
            case "FRAME_R":
                return NegativeType.FRAME_R
            case "FRAME_REPEAT_MIN":
                return NegativeType.FRAME_REPEAT_MIN
            case "RESULT_EXACT":
                return NegativeType.RESULT_EXACT
            case "FRAME_SEQUENCE":
                return NegativeType.FRAME_SEQUENCE
            case "FRAME_SEQUENCE_R":
                return NegativeType.FRAME_SEQUENCE_R
            case _:
                return None


class Negative(Hit, ABC):

    def __init__(self, name: str, negative_type: NegativeType):
        super().__init__(name, negative_type)


class NegativeSpiel(Negative, ABC):
    def check(self, element: Spiel) -> Answers:
        raise NotImplementedError("Class has no Implementation")


class NegativeSatz(Negative, ABC):

    def check(self, element: Satz) -> Answers:
        raise NotImplementedError("Class has no Implementation")


class NegativeFrameValue(NegativeSatz):

    def __init__(self, name: str, frame_size: int, value: int, greater_equal: bool = True):
        super().__init__(name, NegativeType.FRAME)
        self.frame_size = frame_size
        self.value = value
        self.greater_equal = greater_equal

    def check(self, satz: Satz) -> Answers:
        würfe = satz.volle + satz.abräumer
        back = NegativeAnswers()
        for i in range(len(würfe) - self.frame_size):
            folge = würfe[i:i + self.frame_size]
            sum_folge = sum(folge)
            if (self.greater_equal and sum_folge >= self.value) or (not self.greater_equal and sum_folge < self.value):
                absolut_wurf = i + 1
                bereich = VOLLE if absolut_wurf <= 15 else RÄUMER
                back.add(NegativeAnswer(self.name, satz.number, absolut_wurf, bereich, folge))
        return back


class NegativeFrameValueR(NegativeSatz):

    def __init__(self, name: str, frame_size: int, value: int, greater_equal: bool = True):
        super().__init__(name, NegativeType.FRAME_R)
        self.frame_size = frame_size
        self.value = value
        self.greater_equal = greater_equal

    def check(self, satz: Satz) -> Answers:
        würfe = satz.abräumer
        back = NegativeAnswers()
        for i in range(len(würfe) - self.frame_size):
            folge = würfe[i:i + self.frame_size]
            sum_folge = sum(folge)
            if (self.greater_equal and sum_folge >= self.value
                    or not self.greater_equal and sum_folge < self.value):
                absolut_wurf = i + 16
                bereich = RÄUMER
                back.add(NegativeAnswer(self.name, satz.number, absolut_wurf, bereich, folge))

        return back


class NegativeFrameRepeatMin(NegativeSatz):

    def __init__(self, name: str, frame_size: int, number: int):
        super().__init__(name, NegativeType.FRAME_REPEAT_MIN)
        self.frame_size = frame_size
        self.number = number

    def check(self, satz: Satz) -> Answers:
        würfe = satz.volle + satz.abräumer
        back = NegativeAnswers()
        max_index = len(würfe) - 1
        if max_index < self.frame_size - 1:
            return back
        i = 0
        while i < 30 - self.frame_size:
            # check if number is the selected
            if würfe[i] == self.number:
                # count repeating's
                j = 1
                count = 1
                while i + j <= max_index and würfe[i + j] == self.number:
                    count += 1
                    j += 1
                if count >= self.frame_size:
                    absolut_wurf = i + 1
                    bereich = VOLLE if absolut_wurf < 16 else RÄUMER
                    back.add(NegativeAnswer(self.name, satz.number, absolut_wurf, bereich=bereich,
                                            folge=[self.number] * j))
                i += j
            i += 1
        return back


class NegativeFrameSequenz(NegativeSatz):

    def __init__(self, name: str, frame_size: int, sequenz: list[int]):
        super().__init__(name, NegativeType.FRAME_SEQUENCE)
        self.frame_size = frame_size
        self.sequenz = sequenz

    def check(self, satz: Satz) -> Answers:
        würfe = satz.volle + satz.abräumer
        back = NegativeAnswers()
        for i in range(0, len(würfe) - self.frame_size):
            folge_davor = würfe[0:max(i - 1, 1)]
            if (((sum(folge_davor) % 9) == 0 and würfe[i:i + self.frame_size] == self.sequenz)
                    or würfe[i:i + self.frame_size] == self.sequenz):
                absolut_wurf = 1 + i
                bereich = RÄUMER if absolut_wurf > 15 else VOLLE
                back.add(NegativeAnswer(self.name, satz.number, absolut_wurf, bereich, self.sequenz))

        return back


class NegativeFrameSequenzR(NegativeSatz):

    def __init__(self, name: str, frame_size: int, sequenz: list[int], strict: bool):
        super().__init__(name, NegativeType.FRAME_SEQUENCE_R)
        self.frame_size = frame_size
        self.sequenz = sequenz
        self.strict = strict

    def check(self, element: Satz) -> NegativeAnswers:
        würfe = element.abräumer
        back = NegativeAnswers()
        for i in range(0, len(würfe) - self.frame_size):
            folge_davor = würfe[0:max(i - 1, 1)]
            if ((self.strict and (sum(folge_davor) % 9) == 0 and würfe[i:i + self.frame_size] == self.sequenz)
                    or (not self.strict and würfe[i:i + self.frame_size] == self.sequenz)):
                absolut_wurf = 16 + i
                bereich = RÄUMER
                back.add(NegativeAnswer(self.name, element.number, absolut_wurf, bereich, self.sequenz))
        return back
