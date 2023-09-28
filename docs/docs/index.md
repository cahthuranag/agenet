[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/cahthuranag/Agewire/blob/3000891c482e715b3006264a88dfcf4ed4aedc7c/LICENSE)
![.github/workflows/test.yml](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/cahthuranag/agenet/branch/main/graph/badge.svg?token=k8Ix6Zv8x9)](https://codecov.io/gh/cahthuranag/agenet)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docs](https://img.shields.io/badge/docs-stable-blue.svg)](https://cahthuranag.github.io/agenet/)
![GitHub Repo stars](https://img.shields.io/github/stars/cahthuranag/agenet?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/cahthuranag/agenet)
# agenet
A Python 3.8 implementation of the System Model estimate the average AoI (AAoI) in an ultra-reliable low latency communication (URLLC) enabled  wireless  communication system with slotted aloha scheme  over the quasi-static Rayleigh block fading channels. A packet communication scheme is used to meet both the reliability and latency requirements of the  proposed wireless network. By resorting to finite block length information theory, queuing theory and stochastic processes, theoretical results were obtained for this research software.
## System Model
The following figure illustrates the wireless communication system that is proposed in this application. 
![System model.](https://github.com/cahthuranag/agenet/blob/main/docs/docs/image/Fig1.png)
The diagram illustrates a wireless network that consists of multiple nodes. The transmission between each node and the relay is done using a transmission scheme similar to that of the slotted ALOHA protocol, which is a popular random access method used in wireless communication systems.

However, the transmission between the relay and each destination uses dedicated communication channels, and as a result, no transmission scheme similar to ALOHA is employed for this part of the communication. This helps to reduce the possibility of collisions and improve the reliability of the communication.

Additionally, short packet communication is used for transmission. Since short packets are more susceptible to errors, a finite block length information theory is employed to calculate the block error rate. This allows for a more accurate estimation of the probability of errors occurring during transmission.
## Features
The agenet package allows the user to study the Age of Information (AoI) in a slotted URLLC-enabled ALOHA network, which can be used as a basis for implementing mission-critical wireless communication applications. This application can be used as a study tool to analyze the age of information in slotted ALOHA networks with multiple users and short packet communications scenarios to maintain URLLC (ultra-reliable low-latency communication). In this application, various parameters such as power allocation, block length, packet size, number of nodes in the network, and activation probability of each node can be adjusted to analyze how the age of information varies.

The agenet package contains several functions that can be used to study the Age of Information (AoI) in a slotted URLLC-enabled ALOHA network. These functions include:

- Calculates the Signal-to-Noise Ratio (SNR) at each receiving node. This function can be used to determine the SNR for each node in the network, which is an important factor in determining the quality of the communication link;

- Calculates the Block Error Rate (BER) at each destination. This function can be used to determine the BER for each destination in the network, which is an important metric for assessing the reliability of the network;

- Calculates the theoretical AoI and simulates the AoI for a given network configuration. This function can be used to determine the theoretical AoI for a given network configuration, which can be compared with the numerically simulated AoI to verify the accuracy of the simulation.
Also, it is useful for analyzing the performance of the network and assessing the impact of various parameters on the AoI ;

- Estimates the average AoI value for a given update generation time and receiving time. This function can be used to estimate the average AoI value for a given update generation time and receiving time, which is a useful metric for evaluating the performance of any network ;

The package can be used to analyze the performance of a slotted URLLC-enabled ALOHA network and to implement mission-critical wireless communication applications. Additionally, a command-line script is included in the package that allows for easy experimentation with the model. The user can run a simulation with default parameters using the command provided. To run a simulation with default parameters, the user can use a provided command. The simulation can generate both theoretical and simulated values for various factors such as block lengths, power allocations, packet sizes, activation probabilities, and number of nodes in the network. These values can be presented in the form of tables using following command.
```
ageprint
```

In addition to the tables, the simulation results can also be displayed as plots using the command 
```
ageplot
```


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


## License

[MIT License](LICENSE)
## References

[1] [*Age of Information in an URLLC-enabled Decode-and-Forward Wireless Communication System*](https://ieeexplore.ieee.org/document/9449007)