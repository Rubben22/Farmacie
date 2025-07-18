import string
from typing import List
from uuid import uuid4

from faker.generator import random

from Domain.medicament import Medicament
from Repository.repository import Repository


class MedicamentService:
    def __init__(self,
                 medicamentRepository: Repository):
        self.__medicamentRepository = medicamentRepository

    def getAll(self) -> List[Medicament]:
        """
        :return: toate medicamentele care sunt salvate in repository
        """
        return self.__medicamentRepository.read()

    def adauga(self, id_entitate, nume, producator, pret, reteta):
        """
        Adauga un medicament in repository
        :param id_medicament: id-ul medicamentului
        :param nume: numele medicamentului
        :param producator: numele producatorului
        :param pret: pretul medicamentului
        :param reteta: str
        :return: Un nou medicament care va fi adaugat in repository
        """

        medicament = Medicament(id_entitate = id_entitate,
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
        medicament = self.__medicamentRepository.read(id_medicament)
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
        medicament_vechi = self.__medicamentRepository.read(id_medicament)
        medicament = Medicament(id_medicament, nume, producator, pret, reteta)
        self.__medicamentValidator.validate_medicament(medicament)
        self.__medicamentRepository.modifica(medicament)

