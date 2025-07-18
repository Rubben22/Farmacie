import jsonpickle

from Domain.entitate import Entitate
from Repository.repository_in_memory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __readFile(self):
        """
        Citeste toate detaliile despre fiecare card dintr-un fisier
        :return: O lista care contine toate cardurile si campurile lor
        """
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __writeFile(self) -> None:
        """
        Scrie intr-un fisier daca a ost adaugat, sters sau modificat un card
        :return: Un fisier care contine informatiile care au fost modificate
        """
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati, indent=2))

    def read(self, id_entitate=None):
        """
        Citeste detaliile unei entitati in functie de id
        :param id_entitate:id-ul entitatii
        :return:entitatea cu id=id_entitate sau None daca id_entitate nu e None
                lista cu toate entitatile daca id_entitate e None
        """
        self.entitati = self.__readFile()
        return super().read(id_entitate)

    def adauga(self, entitate: Entitate) -> None:
        """
        Adauga o entitate intr-o lista
        :param entitate: entitatea care va fi adaugata in lista
        :return: O lista care contine entitatile vechi si cea adaugata
        """
        self.entitati = self.__readFile()
        super().adauga(entitate)
        self.__writeFile()

    def sterge(self, id_entitate: str) -> None:
        """
        Sterge o entitate dintr-o lista
        :param id_entitate: id-ul dupa care se face stergerea
        """
        self.entitati = self.__readFile()
        super().sterge(id_entitate)
        self.__writeFile()

    def modifica(self, entitate: Entitate) -> None:
        """
        Modifica o entitate dintr-o lista
        :param entitate: entitatea cu care se va face modificare
        :return: O lista care contine entitatile vechi si cea modificata
        """
        self.entitati = self.__readFile()
        super().modifica(entitate)
        self.__writeFile()
