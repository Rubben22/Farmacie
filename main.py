
from Repository.repository_json import RepositoryJson

from Service.medicament_service import MedicamentService
from User_interface.console import Consola


def main():

    medicamentRepositoryJson = RepositoryJson("medicament.json")
    medicamentService = MedicamentService(medicamentRepositoryJson)



    consola = Consola(medicamentService)

    consola.run_principal_menu()


if __name__ == "__main__":
    main()