from typing import List


class Satz:
    def __init__(self, number: int):
        self.number = number
        self.volle: List[int] = [None] * 15
        self.abräumer: List[int] = [None] * 15

    def get(self, number: int) -> int:
        """
        Gibt die Anzahl an Würfen mit einer bestimmten Anzahl an Holz zurück.
        :param number: Anzahl an Holz pro Wurf
        :type number: int
        :return: Anzahl der Würfe mit der Anzahl an Holz
        :rtype: int
        """
        return self.volle.count(number) + self.abräumer.count(number)

    def is_valid(self) -> bool:
        alle = self.volle + self.abräumer
        if len(alle) != 30:
            return False
        return len([x for x in alle if x in [None, -1]]) == 0

    def get_all(self) -> List[int]:
        return self.volle + self.abräumer
