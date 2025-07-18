from setuptools import setup
from setuptools.config.expand import entry_points

setup(
    name='cli_tools',
    version='1.0',
    py_modules=['greeter', 'calculator', 'authenticate', 'fileutils', 'notes'],
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'greetings=greeter:greet',
            'greet1=greeter:greet1',
            'add=calculator:add',
            'substract=calculator:substract',
            'authenticate=authenticate:auth',
            'note=fileutils:note',
            'notes=notes:main'
        ]
    }
)