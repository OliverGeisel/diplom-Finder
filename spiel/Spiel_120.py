import re
from abc import ABC

from spiel.Satz import Satz


class Spiel(ABC):

    def get_alle_sätze(self) -> list:
        raise NotImplementedError("Class has no Implementation")

    def get_volle(self) -> int:
        return sum(self.satz1.volle) + sum(self.satz2.volle) + sum(self.satz3.volle) + sum(self.satz4.volle)

    def get_räumer(self) -> int:
        return sum(self.satz1.abräumer) + sum(self.satz2.abräumer) + sum(self.satz3.abräumer) + sum(self.satz4.abräumer)

    def get_fehlwürfe(self) -> int:
        return self.get(0)

    def get_sum(self) -> int:
        return self.get_volle() + self.get_räumer()

    def get_anzahl_holz(self, number: int) -> int:
        """
        Gibt an, wie oft eine bestimmte Anzahl an Holz (in einem Wurf) im ganzen Spiel vorkam
        :param number:  Anzahl an Holz pro Wurf
        :type number:  int
        :return:     Anzahl der Würfe mit der Anzahl an Holz
        :rtype:     int
        :exception: ValueError
        """
        if number < 0 or number > 9:
            raise ValueError("Anzahl muss zwischen 0 und 9 liegen")
        alles = self.get_alle()
        return alles.count(number)

    def is_valid(self):
        raise NotImplementedError("Class has no Implementation")


class Spiel120(Spiel):
    def get_alle_sätze(self) -> list[Satz]:
        return [self.satz1, self.satz2, self.satz3, self.satz4]

    def __init__(self):
        self.satz1 = Satz(1)
        self.satz2 = Satz(2)
        self.satz3 = Satz(3)
        self.satz4 = Satz(4)

    def get(self, number: int) -> int:
        """
        Gibt die Anzahl an Würfen mit einer bestimmten Anzahl an Holz zurück
        :param number:  Anzahl an Holz pro Wurf
        :type number:  int
        :return:   Anzahl der Würfe mit der Anzahl an Holz
        :rtype:  int
        """
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

    def get_alle(self) -> list:
        return self.satz1.volle + self.satz1.abräumer + self.satz2.volle + self.satz2.abräumer + self.satz3.volle + self.satz3.abräumer + self.satz4.volle + self.satz4.abräumer

    def get_satz(self, number: int) -> Satz:
        if number == 1:
            return self.satz1
        elif number == 2:
            return self.satz2
        elif number == 3:
            return self.satz3
        elif number == 4:
            return self.satz4
        else:
            raise ValueError("Satz muss zwischen 1 und 4 liegen")

    def get_anzahl_holz(self, number: int) -> int:
        """
        Gibt an, wie oft eine bestimmte Anzahl an Holz (in einem Wurf) im ganzen Spiel vorkam
        :param number:  Anzahl an Holz pro Wurf
        :type number:  int
        :return:     Anzahl der Würfe mit der Anzahl an Holz
        :rtype:     int
        :exception: ValueError
        """
        if number < 0 or number > 9:
            raise ValueError("Anzahl muss zwischen 0 und 9 liegen")
        alles = self.get_alle()
        return alles.count(number)

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

    def is_valid(self) -> bool:
        return len([satz for satz in self.get_alle_sätze() if satz.is_valid()]) == 4
