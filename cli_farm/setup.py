from setuptools import setup
from setuptools.config.expand import entry_points

setup(
    name='cli_tools',
    version='1.0',
    py_modules=['crud_medicament'],
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'medicament = crud_medicament:cli',
        ]
    }
)