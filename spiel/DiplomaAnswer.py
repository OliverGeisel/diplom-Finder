from typing import List


class DiplomaAnswer:

    def __init__(self, satz: int, absolut_wurf: int, bereich: str, title, folge: list[int]):
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
        self.folge = folge

    def print(self, name: str = ""):
        print(f"{name}{' ' if name != '' else ''}Satz:{self.satz}-{self.absolut_wurf}-{self.title}\n\t{self.folge}")


class DiplomaAnswerSpiel(DiplomaAnswer):

    def __init__(self, title):
        super().__init__(0, 0, "ALLES", title, [])

    def print(self, name: str = ""):
        print(f"{name}{' ' if name != '' else ''}Spiel-{self.title}")


class DiplomaAnswers:
    def __init__(self, name: str = ""):
        self.answers: List[DiplomaAnswer] = list()  # Liste der Antworten
        self.name = name  # Name des Spielers

    def add(self, diploma_answer: DiplomaAnswer):
        self.answers.append(diploma_answer)

    def __add__(self, other):
        if not isinstance(other, DiplomaAnswers):
            raise Exception("Type Missmatch")
        back = DiplomaAnswers(self.name)
        for i in self.answers:
            back.add(i)
        for i in other.answers:
            back.add(i)
        return back

    def print(self):
        for i in self.answers:
            i.print(self.name)
