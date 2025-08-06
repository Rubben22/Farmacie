import json

from Domain.entitate import Entitate
from Repository.repository_in_memory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename, entity_cls=Entitate):
        super().__init__()
        self.filename = filename
        self.entity_cls = entity_cls  # The Pydantic model class to use

    def __readFile(self):
        """
        Reads all entities from a file.
        :return: A dictionary containing all entities.
        """
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return {
                    k: self.entity_cls.model_validate(v)
                    for k, v in data.items()
                }
        except Exception:
            return {}

    def __writeFile(self) -> None:
        """
        Writes the current entities to a file.
        """
        with open(self.filename, "w") as f:
            json.dump(
                {k: v.model_dump() for k, v in self.entitati.items()},
                f,
                indent=2,
            )

    def read(self, id_entitate=None):
        """
        Reads an entity by id or all entities.
        """
        self.entitati = self.__readFile()
        return super().read(id_entitate)

    def adauga(self, entitate: Entitate) -> None:
        self.entitati = self.__readFile()
        super().adauga(entitate)
        self.__writeFile()

    def sterge(self, id_entitate: str) -> None:
        self.entitati = self.__readFile()
        super().sterge(id_entitate)
        self.__writeFile()

    def modifica(self, entitate: Entitate) -> None:
        self.entitati = self.__readFile()
        super().modifica(entitate)
        self.__writeFile()
