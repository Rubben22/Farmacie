from pydantic import field_validator

from Domain.entitate import Entitate


class Medicament(Entitate):
    nume: str
    producator: str
    pret: float
    reteta: str

    @field_validator("pret")
    @classmethod
    def validate_pret(cls, pret):
        if pret < 0:
            raise ValueError("pret must be greater than or equal to 0")
        return pret

    def to_dict(self):
        return {
            "id_entitate": self.id_entitate,
            "nume": self.nume,
            "producator": self.producator,
            "pret": self.pret,
            "reteta": self.reteta,
        }
