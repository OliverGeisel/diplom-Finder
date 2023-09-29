from typing import List


class DiplomaAnswer:

    def __init__(self, satz: int, absolut_wurf: int, bereich: str, title, folge: list[int]):
        """
        Ein Diplom mit allen Informationen in einem Spiel.

        :param satz: Satznummer im Spiel
        :type satz: int
        :param absolut_wurf: absoluter Wurf im Satz
        :type absolut_wurf: int
        :param bereich: Bereich des Wurfes (VOLLE oder RÄUMER)
        :type bereich: str
        :param title: Titel des Diploms
        :type title: str
        :param folge: Folge der Würfe.
        :type folge: list[int]
        """
        self.satz = satz
        self.bereich = bereich
        self.absolut_wurf = absolut_wurf
        self.bereich_wurf = absolut_wurf - 15 if absolut_wurf > 15 else absolut_wurf
        self.title = title
        self.folge = folge

    def is_leer(self):
        return self.satz == 0 and self.absolut_wurf == 0 and self.bereich == "" and self.title == "" and self.folge == []

    def __str__(self):
        return f"Satz:{self.satz}-{self.absolut_wurf}-{self.title}\n\t{self.folge}"

    def print(self, name: str = ""):
        print(f"{name}{' ' if name != '' else ''}Satz:{self.satz}-{self.absolut_wurf}-{self.title}\n\t{self.folge}")


class DiplomaAnswerSpiel(DiplomaAnswer):
    """
    Ein Diplom, das auf ein gesamtes Spiel angewendet wird. Es werden also Gesamtholz oder ähnliches ausgewertet.
    """

    def __init__(self, title):
        super().__init__(0, 0, "ALLES", title, [])

    def print(self, name: str = ""):
        print(f"{name}{' ' if name != '' else ''}Spiel-{self.title}")


class DiplomaAnswers:
    def __init__(self, name: str = ""):
        """
        Erzeugt neue DiplomeAntworten für einen Spieler
        :param name: Name des Spielers
        :type name: str
        """
        self.answers: List[DiplomaAnswer] = list()  # Liste der Antworten
        self.name = name  # Name des Spielers

    def add(self, diploma_answer: DiplomaAnswer):
        """
        Fügt eine Antwort hinzu
        :param diploma_answer:
        :type diploma_answer:
        :return:
        :rtype:
        """
        self.answers.append(diploma_answer)

    def is_leer(self) -> bool:
        return len(self.answers) == 0

    def __add__(self, other) -> "DiplomaAnswers":
        """
        Fügt zwei Diplome(sammlungen) zusammen und gibt ein neues DiplomaAnswers zurück
        :param other: andere Diplome
        :type other:
        :return:
        :rtype:
        """
        if not isinstance(other, DiplomaAnswers):  # todo enable type
            raise Exception("Type Missmatch")
        back = DiplomaAnswers(self.name)
        for i in self.answers:
            back.add(i)
        for i in other.answers:
            back.add(i)
        return back

    def __iadd__(self, other):
        """
        Fügt die rechte Diplome(sammlungen) der linken hinzu.
        :param other: andere Diplome
        :type other:
        :return:
        :rtype:
        """
        if not isinstance(other, DiplomaAnswers):
            raise Exception("Type Missmatch")
        for i in other.answers:
            self.add(i)
        return self

    def print(self):
        for i in self.answers:
            i.print(self.name)
