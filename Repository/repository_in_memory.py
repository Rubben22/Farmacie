from Domain.entitate import Entitate
from Repository.repository import Repository


class NoSuchID(Exception):
    pass


class DuplicateID(Exception):
    pass


class RepositoryInMemory(Repository):
    def __init__(self):
        self.entitati = {}

    def read(self, id_entitate=None):
        """
        Citeste detaliile unui medicament in functie de id-ul entitatii
        :param id_entitate: parametrul dupa care se face citirea
        :return: detalii despre o entitate
        """
        if id_entitate is None:
            return list(self.entitati.values())

        if id_entitate in self.entitati:
            return self.entitati[id_entitate]
        else:
            return None

    def adauga(self, entitate: Entitate):
        """
        Adauga un medicament in lista
        :param entitate: entitatea care va fi adaugata in lista
        :return: O lista care contine entitatile vechi si cea adaugata
        """
        if self.read(entitate.id_entitate) is not None:
            raise DuplicateID("Exista deja o entitate cu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate

    def sterge(self, id_entitate: str):
        """
        Sterge o entitate dintr-o lista
        :param id_entitate: id-ul dupa care se face stergerea
        :return: O lista care contine entitatile vechi, mai putin cel sters
        """
        if self.read(id_entitate) is None:
            raise NoSuchID("Nu exista nicio entitate cu id-ul dat!")
        del self.entitati[id_entitate]

    def modifica(self, entitate: Entitate):
        """
        Modifica o entitate dintr-o lista
        :param entitate: entitatea cu care se va modifica lista
        :return: O lista care contine atat entitatile vechi, cat si cea
        modificata
        """
        if self.read(entitate.id_entitate) is None:
            raise NoSuchID("Nu exista nicio entitatecu id-ul dat!")
        self.entitati[entitate.id_entitate] = entitate
