from abc import ABC


class Answer(ABC):
    """
    Informationen über ein Ereignis, das eine besondere Wertung erhält.
    """

    def __init__(self, name, satz, absolut_wurf, bereich, folge):
        self.name = name
        # game info
        self.bereich = bereich
        self.absolut_wurf = absolut_wurf
        self.bereich_wurf = absolut_wurf - 15 if absolut_wurf > 15 else absolut_wurf
        self.satz = satz
        self.folge = folge

    def __str__(self):
        return f"Satz:{self.satz}-{self.absolut_wurf}-{self.name}\n\t{self.folge}"

    def is_leer(self):
        return self.satz == 0 and self.absolut_wurf == 0 and self.bereich == "" and self.name == "" and self.folge == []

    def print(self, name: str = ""):
        print(f"{name}{' ' if name != '' else ''}Satz:{self.satz}-{self.absolut_wurf}-{self.name}\n\t{self.folge}")


class Answers(ABC):
    """
    Sammlung von Antworten eines Spielers auf ein Spiel.
    Alle Antworten sind einem Spieler zugeordnet.
    """

    def __init__(self, player_name: str = ""):
        self.player_name = player_name  # Name des Spielers
        self.answers: list[Answer] = list()  # Liste der Antworten

    def is_leer(self) -> bool:
        return len(self.answers) == 0

    def add(self, answer: Answer):
        """
        Fügt eine Antwort hinzu
        :param answer:
        :type answer:
        :return:
        :rtype:
        """
        self.answers.append(answer)

    def __add__(self, other: 'Answers') -> "Answers":
        """
        Fügt zwei Diplome(sammlungen) zusammen und gibt ein neues DiplomaAnswers zurück
        :param other: andere Diplome
        :type other:
        :return:
        :rtype:
        """
        if not isinstance(other, Answers):  # todo enable type
            raise Exception("Type Missmatch")
        back = Answers(self.player_name)
        for i in self.answers:
            back.add(i)
        for i in other.answers:
            back.add(i)
        return back

    def __iadd__(self, other: 'Answers') -> "Answers":
        """
        Fügt die rechte Diplome(sammlungen) der linken hinzu.
        :param other: andere Diplome
        :type other:
        :return:
        :rtype:
        """
        if not isinstance(other, Answers):
            raise Exception("Type Missmatch")
        for i in other.answers:
            self.add(i)
        return self

    def print(self):
        for i in self.answers:
            i.print(self.player_name)
