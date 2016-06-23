from setuptools import setup, find_packages

CONSOLE_SCRIPTS = ['pordego = pordego.cli:main']


setup(name="pordego",
      version="1.0.0",
      description="Command line tool for running configurable static analysis plugins on Python code",
      packages=find_packages(),
      entry_points={'console_scripts': CONSOLE_SCRIPTS},
      install_requires=["pyyaml"]
      )
