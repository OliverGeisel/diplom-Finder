from datetime import datetime

from spiel import DiplomaAnswers
from spiel.Answer import Answers


class PlayerDayCollection:

    def __init__(self, date: datetime.date, mannschaft: str, answers: Answers):
        """
        Erzeugt ein neues Diplom für einen Spieler an einem bestimmten Datum und einer bestimmten Mannschaft
        :param date: Datum des Diploms
        :type date: datetime.date
        :param mannschaft: Mannschaft des Spielers
        :type mannschaft: str
        :param answers:  Diplome des Spielers
        :type answers:  DiplomaAnswers
        """
        self.date = date
        self.mannschaft = mannschaft
        self.answers = answers
        self.name = answers.player_name

    def get_anzahl(self) -> int:
        return len(self.answers.answers)

    def __str__(self):
        return f"{self.name} - {self.mannschaft} - {self.date.strftime('%d.%m.%Y')}"

    def get_vorname(self) -> str:
        if len(self.name.split(" ")) == 1:
            return self.name
        return self.name.split(" ")[1]

    def get_nachname(self) -> str:
        return self.name.split(" ")[0]

    def get_full_name(self) -> str:
        return f"{self.get_vorname()} {self.get_nachname()}"

    def __eq__(self, other):
        if not isinstance(other, PlayerDayCollection):
            return False
        return self.name == other.name and self.date == other.date and self.mannschaft == other.mannschaft

    def __hash__(self):
        return hash(self.name) + hash(self.date) + hash(self.mannschaft)


class DiplomaPlayerDayCollection(PlayerDayCollection):
    """
    Eine Ansammlung von Diplomen eines Spielers an einem bestimmten Datum und einer bestimmten Mannschaft
    """

    def __init__(self, date: datetime.date, mannschaft: str, answers: Answers):
        super().__init__(date, mannschaft, answers)


class NegativePlayerDayCollection(PlayerDayCollection):

    def __init__(self, date: datetime.date, mannschaft: str, answers: Answers):
        super().__init__(date, mannschaft, answers)
