from datetime import datetime

from spiel import DiplomaAnswers


class DiplomaBig:

    def __init__(self, date: datetime.date, mannschaft: str, diplomas: DiplomaAnswers):
        self.date = date
        self.mannschaft = mannschaft
        self.diplomas = diplomas
        self.name = diplomas.name

    def get_diplome_anzahl(self) -> int:
        return len(self.diplomas.answers)

    def __str__(self):
        return f"{self.name} - {self.mannschaft} - {self.date.strftime('%d.%m.%Y')}"
