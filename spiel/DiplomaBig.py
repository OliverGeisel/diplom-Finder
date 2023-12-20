from datetime import datetime

from spiel import DiplomaAnswers


class DiplomaBig:

    def __init__(self, date: datetime.date, mannschaft: str, diplomas: DiplomaAnswers):
        """
        Erzeugt ein neues Diplom für einen Spieler an einem bestimmten Datum und einer bestimmten Mannschaft
        :param date: Datum des Diploms
        :type date: datetime.date
        :param mannschaft: Mannschaft des Spielers
        :type mannschaft: str
        :param diplomas:  Diplome des Spielers
        :type diplomas:  DiplomaAnswers
        """
        self.date = date
        self.mannschaft = mannschaft
        self.diplomas = diplomas
        self.name = diplomas.name

    def get_diplome_anzahl(self) -> int:
        return len(self.diplomas.answers)

    def __str__(self):
        return f"{self.name} - {self.mannschaft} - {self.date.strftime('%d.%m.%Y')}"

    def get_vorname(self) -> str:
        return self.name.split(" ")[1]

    def get_nachname(self) -> str:
        return self.name.split(" ")[0]

    def get_full_name(self) -> str:
        return f"{self.get_vorname()} {self.get_nachname()}"
