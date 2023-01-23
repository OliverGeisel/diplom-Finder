from typing import List


class Satz:
    def __init__(self, number: int):
        self.number = number
        self.volle: List[int] = [None] * 15
        self.abräumer: List[int] = [None] * 15

    def get(self, number: int):
        return self.volle.count(number) + self.abräumer.count(number)
