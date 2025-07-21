import datetime

from Domain.entitate import Entitate


class Tranzactie(Entitate):
    """
    Creeaza o tranzactie pe baza unui medicament si al cardului client
    - id_tranzactie: id-ul tranzactiei
    - id_medicament: id-ul medicamentului
    - id_card_client: id-ul cardului client
    - nr_bucati: numarul de bucati
    - data_ora: data si ora la care s-a facut tranzactia
    """
    id_medicament: str
    id_card_client: str
    nr_bucati: int
    data_ora: datetime
