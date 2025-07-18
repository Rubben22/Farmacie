

from Service.medicament_service import MedicamentService


class Consola:
    def __init__(self,
                 medicamentService: MedicamentService):
        self.__medicamentService = medicamentService

    def run_principal_menu(self):
        while True:
            print("a. Adauga medicament")
            print("b. Sterge medicament")
            print("c. Modifica medicament")
            print("d. Afiseaza toate medicamentele")
            print("x. Revenire la meniul principal")
            optiune = input("Alegeti o optiune: ")
            if optiune == "a":
                self.ui_adauga_medicament()
            elif optiune == "b":
                self.ui_sterge_medicament()
            elif optiune == "c":
                self.ui_modifica_medicament()
            elif optiune == "d":
                self.ui_showAll_medicamente()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati")

    def ui_showAll_medicamente(self):
        for medicament in self.__medicamentService.getAll():
            print(medicament)

    def ui_adauga_medicament(self):
        try:
            id_medicament = input("Dati id-ul: ")
            nume = input("Dati numele: ")
            producator = input("Dati numele producatorului: ")
            pret = float(input("Dati pretul: "))
            reteta = input("Necesita reteta (da/nu): ")
            self.__medicamentService.adauga(id_medicament, nume, producator,
                                            pret, reteta)
        except ValueError as v:
            print(v)
        except Exception as e:
            print(e)

    def ui_sterge_medicament(self):
        try:
            id_medicament = input("Dati id-ul medicamentului de sters: ")
            self.__medicamentService.sterge(id_medicament)
        except Exception as e:
            print(e)

    def ui_modifica_medicament(self):
        try:
            id_medicament = input("Dati id-ul medicamentului de modificat: ")
            nume = input("Dati noul nume: ")
            producator = input("Dati noul producator: ")
            pret = float(input("Dati noul pret: "))
            reteta = input("Necesita reteta: ")
            self.__medicamentService.modifica(id_medicament, nume, producator,
                                              pret, reteta)
        except Exception as e:
            print(e)
