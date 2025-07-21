from setuptools import setup

setup(
    name='cli_tools',
    version='1.0',
    py_modules=[ 'crud_medicament', 'crud_client', 'crud_tranzactie' ],
    install_requires=[ 'click' ],
    entry_points={
        'console_scripts': [
            'medicament = crud_medicament:cli',
            'client = crud_client:cli',
            'tranzactie = crud_tranzactie:cli',
            'operations = crud_tranzactie:operations'
        ]
    }
)
