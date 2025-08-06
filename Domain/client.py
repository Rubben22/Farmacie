import datetime
from datetime import date
from pydantic import field_validator

from Domain.entitate import Entitate


class Client(Entitate):
    """
    Creeaza un card client:
    - id_card_client: id-ul cardului
    - nume: nume client
    - prenume: prenume client
    - CNP: codul numeric personal
    - data_nasterii: data nasterii
    - data_inregistrarii: data la care s-a facut inregistrarea
    """

    nume: str
    prenume: str
    CNP: int
    data_nasterii: date

    @field_validator("data_nasterii", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Data trebuie sa fie in formatul dd.mm.yyyy")
