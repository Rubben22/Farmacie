from typing import List

from Domain.medicament import Medicament
from Repository.repository import Repository


class MedicamentService:
    def __init__(self,
                 medicament_repository: Repository):
        self.__medicamentRepository = medicament_repository

    def getAll(self) -> List[ Medicament ]:
        """
        :return: toate medicamentele care sunt salvate in repository
        """
        return self.__medicamentRepository.read()

    def adauga(self, id_medicament, nume, producator, pret, reteta):
        """
        Adauga un medicament in repository
        :param id_medicament: id-ul medicamentului
        :param nume: numele medicamentului
        :param producator: numele producatorului
        :param pret: pretul medicamentului
        :param reteta: str
        :return: Un nou medicament care va fi adaugat in repository
        """

        medicament = Medicament(id_entitate=id_medicament,
                                nume=nume,
                                producator=producator,
                                pret=pret,
                                reteta=reteta)
        self.__medicamentRepository.adauga(medicament)

    def sterge(self, id_medicament):
        """
        Sterge un medicament din repository
        :param id_medicament: id-ul dupa care se va face stergerea
        :return: nu returneaza nimic
        """
        self.__medicamentRepository.sterge(id_medicament)

    def modifica(self, id_medicament, nume, producator, pret, reteta):
        """
        Modifica un medicament existent din repository
        :param id_medicament: id-ul medicamentului de modificat
        :param nume: noul nume
        :param producator: noul producator
        :param pret: noul pret
        :param reteta: str
        :return: Medicamentul modificat care il va adauga in repository
        """
        medicament = Medicament(id_entitate=id_medicament,
                                nume=nume,
                                producator=producator,
                                pret=pret,
                                reteta=reteta)
        self.__medicamentRepository.modifica(medicament)
