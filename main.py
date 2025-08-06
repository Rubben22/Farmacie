from Repository.repository_json import RepositoryJson
from Domain.medicament import Medicament

from Service.medicament_service import MedicamentService
from User_interface.console import Consola


def main():
    medicament_repository_json = RepositoryJson(
        "medicament.json", entity_cls=Medicament
    )
    medicament_service = MedicamentService(medicament_repository_json)

    consola = Consola(medicament_service)

    consola.run_principal_menu()


if __name__ == "__main__":
    main()
