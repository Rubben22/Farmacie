from pydantic import BaseModel, field_validator

from Domain.entitate import Entitate


class Medicament(Entitate):
    nume: str
    producator: str
    pret: float
    reteta: str

    @field_validator('pret')
    @classmethod
    def validate_pret(cls, pret):
        if pret < 0:
            raise ValueError("pret must be greater than or equal to 0")
        return pret