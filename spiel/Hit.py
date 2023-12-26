from abc import ABC

from spiel.Answer import Answer

VOLLE = "volle"
RÄUMER = "räumer"
ALLES = "alles"


class Hit(ABC):

    def __init__(self, name, hit_type):
        self.name = name
        self.type = hit_type

    def check(self, element) -> Answer:
        raise NotImplementedError("Class has no Implementation")

    def __eq__(self, other: 'Hit') -> bool:
        if other is None or not isinstance(other, Hit):
            return False
        return self.name == other.name and self.type == other.type

    def __hash__(self) -> int:
        return super().__hash__() + hash(self.name) + hash(self.type)
