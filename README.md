# Pseudo Dojo

An open source python package to generate and validate pseudopotentials.

## About

Pseudo Dojo collects the latest approximations of the core electrons of each element, for use in Density Functional Theory (DFT), as well as providing a suite of tools for generating and testing new pseudopotentials. Seven tests are currently provided, executed using the [ABINIT](https://www.abinit.org/) software package:

- Delta guage
- Revised Delta Guage
- GBRV
- Tests for FCC/BCC/compounds
- Phonons at the gamma point
- Tests for presence of ghosts states both above and below the Fermi level

Barring the ghost and compound validations, each of these tests are performed as a function of the energy cutoff, where the outcome may provide hints for the energy cutoff in downstream calculations. Results of each test are tracked and stored in a `djrepo` TODO UPDATE? file, allowing high throughput validation of many pseudopotentials to be performed. 

This codebase is stored on github, with a web interface provided at [the Pseudo Dojo website](http://www.pseudo-dojo.org/). The latest stable release is hosted on [PyPi](https://pypi.org/project/pseudodojo/) for use in python scripts, recommended installation is via [poetry](https://python-poetry.org/) within a python virtual environment:

```bash
$ poetry init # Will create a new pyproject.toml if not already present
$ poetry add pseudodojo
$ poetry shell
```

Alternatively, via pip:

```bash
$ pip install pseudodojo
```

## Using Pseudo Dojo


## License

All pseudopotentials and their associated input files are released under a [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode) license, which allows them to be used, modified, and distributed in personal, academic, and commercial applications as long as the Pseudo Dojo project is credited for the original creation.

The Pseudo Dojo source code is released under a [GPL v2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html) license, which allows for the redistribution and modification of the code in both free and commercial software, as long as all modifications to the code are also freely distributed under a GPL license. Please read the linked license file for full terms of use.