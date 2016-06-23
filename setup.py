from setuptools import setup, find_packages

CONSOLE_SCRIPTS = ['pordego = pordego.cli:main']

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License"
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7"
]

setup(name="pordego",
      version="1.0.0",
      author="Tim Treptow",
      author_email="tim.treptow@gmail.com",
      description="Command line tool for running configurable static analysis plugins on Python code",
      packages=find_packages(),
      url="https://github.com/ttreptow/pordego",
      entry_points={'console_scripts': CONSOLE_SCRIPTS},
      install_requires=["pyyaml"],
      classifiers=CLASSIFIERS
      )
