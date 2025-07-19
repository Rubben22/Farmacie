from setuptools import setup

setup(
    name='cli_tools',
    version='1.0',
    py_modules=[ 'crud_medicament' ],
    install_requires=[ 'click' ],
    entry_points={
        'console_scripts': [
            'medicament = crud_medicament:cli',
        ]
    }
)
