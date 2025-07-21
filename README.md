## Farmacie online
Aceasta este o aplicație de linie de comandă (CLI) pentru gestionarea activităților dintr-o farmacie: clienți, medicamente și tranzacții.

### Structura aplicatiei
1. CRUD medicament: id, nume, producător, preț, necesită rețetă.
2. CRUD client: id, nume, prenume, CNP, data nașterii (dd.mm.yyyy)
3. CRUD tranzacție: id, id_medicament, id_client (poate fi nul), nr_bucăți, data și ora
4. Afișarea tuturor tranzacțiilor dintr-un interval de zile dat.
5. Afișarea medicamentelor ordonate descrescător după numărul de vânzări.
6. Ștergerea tuturor tranzacțiilor dintr-un anumit interval de zile

### Cerinte implementate
- Este o aplicatie de tip CLI(command-line interface) pentru gestionarea unei farmacii. Se pot adăuga și administra clienți, medicamente și tranzacții.
- Structura proiectului este gândită generic și extensibil. Modelele moștenesc dintr-o clasă de bază `Entitate`, iar operațiile CRUD sunt implementate separat pentru fiecare entitate.
- Datele sunt salvate și citite din fișiere `.json`.
- Pentru serializare/deserializare se foloseste `Pydantic`.
- Codul este lintat cu `flake8`.
- Aplicația nu urmează strict un model MVC sau MVCS complet, dar deși nu există servicii separate, codul este suficient de modular și extensibil pentru a fi organizat pe viitor într-un MVCS complet.
- Comenzile CLI sunt implementate cu `Click`.



