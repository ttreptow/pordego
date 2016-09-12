from setuptools import setup, find_packages

CONSOLE_SCRIPTS = ['pordego = pordego.cli:main']

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7"
]

VERSION = "1.2.1"

setup(name="pordego",
      version=VERSION,
      author="Tim Treptow",
      author_email="tim.treptow@gmail.com",
      description="Command line tool for running configurable static analysis plugins on Python code",
      packages=find_packages(exclude=["tests", "tests.*"]),
      url="https://github.com/ttreptow/pordego",
      download_url="https://github.com/ttreptow/pordego/tarball/{}".format(VERSION),
      entry_points={'console_scripts': CONSOLE_SCRIPTS,
                    "pordego.output": ["junit = pordego.junit_output:write_output_file",
                                       "stdout = pordego.logging_output:print_output"]},
      install_requires=["pyyaml", "junit-xml"],
      classifiers=CLASSIFIERS
      )
