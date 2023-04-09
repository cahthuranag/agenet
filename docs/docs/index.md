[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/cahthuranag/Agewire/blob/3000891c482e715b3006264a88dfcf4ed4aedc7c/LICENSE)
![.github/workflows/test.yml](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/cahthuranag/agenet/branch/main/graph/badge.svg?token=k8Ix6Zv8x9)](https://codecov.io/gh/cahthuranag/agenet)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docs](https://img.shields.io/badge/docs-stable-blue.svg)](https://cahthuranag.github.io/agenet/)

# agenet
A Python 3.8 implementation of the System Model estimate the average AoI (AAoI) in an ultra-reliable low latency communication (URLLC) enabled  wireless  communication system with slotted aloha scheme  over the quasi-static Rayleigh block fading channels. A packet communication scheme is used to meet both the reliability and latency requirements of the  proposed wireless network. By resorting to finite block length information theory, queuing theory and stochastic processes, theoretical results were obtained for this research software.
## System Model
In this software,  a URLLC-enable wireless communication  system is proposed as illustrated in following figure. 
![System model.](agenet\docs\docs\figures/Fig1.png) 


## Requirements

The implementation requires Python 3.8+ to run.
The following libraries are also required:

- `numpy`
- `matplotlib`
- `pandas`
- `tabulate`
- `argparse`
- `itertools`
- `math`
- `scipy`
- `random`

## How to install

### From PyPI

```
pip install 
```

### From source/GitHub

Directly using pip:

```
pip install 
```

Or each step at a time:

```
git clone  https://github.com/cahthuranag/agenet.git
cd 
pip install .
```

### Installing for development and/or improving the package

```
git clone https://github.com/cahthuranag/agenet.git
cd 
pip install -e .[dev]
```

This way, the package is installed in development mode. As a result, the pytest dependencies/plugins are also installed.

## Documentation

* [*Agenet* package documentation](https://cahthuranag.github.io/agenet/)
* [Developer's guide]()
* [Scenario Description]()

## License

[MIT License](LICENSE)
## References

[1] [*Age of Information in an URLLC-enabled Decode-and-Forward Wireless Communication System*](https://ieeexplore.ieee.org/document/9449007)
