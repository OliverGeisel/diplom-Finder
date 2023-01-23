import re

from spiel import Satz
from spiel.Diploma import Diploma, DiplomaAnswers, DiplomaSatz


class Spiel120:
    def __init__(self):
        self.satz1 = Satz(1)
        self.satz2 = Satz(2)
        self.satz3 = Satz(3)
        self.satz4 = Satz(4)

    def get(self, number: int) -> int:
        gesamt = 0
        gesamt += self.satz1.get(number)
        gesamt += self.satz2.get(number)
        gesamt += self.satz3.get(number)
        gesamt += self.satz4.get(number)
        return gesamt

    def get_volle(self) -> int:
        return sum(self.satz1.volle) + sum(self.satz2.volle) + sum(self.satz3.volle) + sum(self.satz4.volle)

    def get_räumer(self) -> int:
        return sum(self.satz1.abräumer) + sum(self.satz2.abräumer) + sum(self.satz3.abräumer) + sum(self.satz4.abräumer)

    def get_fehlwürfe(self) -> int:
        return self.get(0)

    def get_sum(self) -> int:
        return self.get_volle() + self.get_räumer()

    def init(self, values: dict):
        # 1. Satz
        wurf_voll = [(min(int(value), 9) if value != "" else 0) for key, value in values.items() if
                     re.match(r"wurf-1-volle-\d\d?", key)]
        wurf_raeumer = [(min(int(value), 9) if value != "" else 0) for key, value in values.items() if
                        re.match(r"wurf-1-räumer-\d\d?", key)]
        self.satz1.volle = wurf_voll
        self.satz1.abräumer = wurf_raeumer
        # 2. Satz
        wurf_voll = [(min(int(value), 9) if value != "" else 0) for key, value in values.items() if
                     re.match(r"wurf-2-volle-\d\d?", key)]
        wurf_raeumer = [(min(int(value), 9) if value != "" else 0) for key, value in values.items() if
                        re.match(r"wurf-2-räumer-\d\d?", key)]
        self.satz2.volle = wurf_voll
        self.satz2.abräumer = wurf_raeumer
        # 3. Satz
        wurf_voll = [(min(int(value), 9) if value != "" else 0) for key, value in values.items() if
                     re.match(r"wurf-3-volle-\d\d?", key)]
        wurf_raeumer = [(min(int(value), 9) if value != "" else 0) for key, value in values.items() if
                        re.match(r"wurf-3-räumer-\d\d?", key)]
        self.satz3.volle = wurf_voll
        self.satz3.abräumer = wurf_raeumer
        # 4. Satz
        wurf_voll = [(min(int(value), 9) if value != "" else 0) for key, value in values.items() if
                     re.match(r"wurf-4-volle-\d\d?", key)]
        wurf_raeumer = [(min(int(value), 9) if value != "" else 0) for key, value in values.items() if
                        re.match(r"wurf-4-räumer-\d\d?", key)]
        self.satz4.volle = wurf_voll
        self.satz4.abräumer = wurf_raeumer

    def analyze(self, diploma: Diploma):
        answer = DiplomaAnswers()
        if isinstance(diploma, DiplomaSatz):
            for i in [self.satz1, self.satz2, self.satz3, self.satz4]:
                answer = answer + diploma.check(i)
        else:
            answer = diploma.check(self)
        return answer
