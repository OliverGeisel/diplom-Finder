from spiel.Answer import Answers, Answer


class DiplomaAnswer(Answer):

    def __init__(self, satz: int, absolut_wurf: int, bereich: str, name, folge: list[int]):
        """
        Ein Diplom mit allen Informationen in einem Spiel.

        :param satz: Satznummer im Spiel
        :type satz: int
        :param absolut_wurf: absoluter Wurf im Satz
        :type absolut_wurf: int
        :param bereich: Bereich des Wurfes (VOLLE oder RÄUMER)
        :type bereich: str
        :param name: Titel des Diploms
        :type name: str
        :param folge: Folge der Würfe.
        :type folge: list[int]
        """
        super().__init__(name, satz, absolut_wurf, bereich, folge)


class DiplomaAnswerSpiel(DiplomaAnswer):
    """
    Ein Diplom, das auf ein gesamtes Spiel angewendet wird. Es werden also Gesamtholz oder ähnliches ausgewertet.
    """

    def __init__(self, name):
        super().__init__(0, 0, "ALLES", name, [])

    def print(self, name: str = ""):
        print(f"{name}{' ' if name != '' else ''}Spiel-{self.name}")


class DiplomaAnswers(Answers):
    def __init__(self, player_name: str = ""):
        """
        Erzeugt neue DiplomeAntworten für einen Spieler
        :param player_name: Name des Spielers
        :type player_name: str
        """
        super().__init__(player_name)
        self.answers: list[DiplomaAnswer] = list()  # Liste der Antworten
