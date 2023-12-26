from spiel.Answer import Answer, Answers


class NegativeAnswer(Answer):
    def __init__(self, name, satz: int, absolut_wurf: int, bereich: str, folge: list[int]):
        super().__init__(name, satz, absolut_wurf, bereich, folge)


class NegativeAnswerSpiel(NegativeAnswer):
    """
    Ein negatives Ereignis, das auf ein gesamtes Spiel angewendet wird. Es werden also Gesamtholz oder ähnliches ausgewertet.
    """

    def __init__(self, name):
        super().__init__(name, 0, 0, "ALLES", [])

    def print(self, name: str = ""):
        print(f"{name}{' ' if name != '' else ''}Spiel-{self.name}")


class NegativeAnswers(Answers):
    def __init__(self, player_name: str = ""):
        super().__init__(player_name)
        self.answers: list[NegativeAnswer] = list()
