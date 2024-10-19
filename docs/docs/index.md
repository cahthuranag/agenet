[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/cahthuranag/Agewire/blob/3000891c482e715b3006264a88dfcf4ed4aedc7c/LICENSE)
[![Tests](https://github.com/cahthuranag/agenet/actions/workflows/test.yml/badge.svg)](https://github.com/cahthuranag/agenet/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/cahthuranag/agenet/branch/main/graph/badge.svg?token=k8Ix6Zv8x9)](https://codecov.io/gh/cahthuranag/agenet)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docs](https://img.shields.io/badge/docs-stable-blue.svg)](https://cahthuranag.github.io/agenet/)
![GitHub Repo stars](https://img.shields.io/github/stars/cahthuranag/agenet?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/cahthuranag/agenet)

# agenet

Agenet is an open-source Python package designed to estimate the Age of Information (AoI) in cooperative wireless networks. By implementing a system model that combines finite blocklength information theory and AoI analysis over Rayleigh fading channels, Agenet provides users with a comprehensive tool for studying short packet-based communication networks. This package is particularly valuable for those working on mission-critical wireless systems where the freshness of information is crucial.

## System model

The following figure illustrates the wireless communication system that is proposed in this application.

![System model.](https://raw.githubusercontent.com/cahthuranag/agenet/main/docs/docs/image/Fig1.png)

Agenet implements a short packet decode-and-forward (DF) cooperative wireless relaying system. This system consists of three key nodes: a source node (S) that generates and transmits new updates, a relay node (R) that receives, decodes, and forwards data, and a destination node (D) that receives the forwarded data. The communication process is structured into two time slots within each transmission block, with the source transmitting data to the relay in the first slot, and the relay decoding and forwarding the data to the destination in the second slot. This wireless communication model accounts for both small-scale and large-scale channel gains, considering Rayleigh fading and path loss to provide a realistic representation of wireless communication environments.

## Features
The **agenet** package allows the user to estimate the Age of Information (AoI) in cooperative wireless networks, which can be used as a basis for implementing mission-critical wireless communication applications. This application can be used as a study tool to analyze the age of information in cooperative wireless networks under short packet communications scenarios to maintain URLLC (ultra-reliable low-latency communication). In this application, various parameters such as power allocation, block length and  packet size can be adjusted to analyze how the age of information varies.

The **agenet** package contains several functions that can be used to study the AoI in a cooperative wireless networks. These functions allow the user to:

- Calculate the Signal-to-Noise Ratio (SNR) at each receiving node in the network, which is an important factor in determining the quality of the communication link;

- Calculate the Block Error Rate (BER) for each destination in the network, which is an important metric for assessing the reliability of the network;

- Calculate the theoretical AoI and simulate the AoI for a given network configuration, allowing the comparison of both measures to verify the accuracy of the simulation, as well as analyzing the performance of the network and assessing the impact of various parameters on the AoI;

- Estimate the average AoI value for a given update generation time and receiving time, which is a useful metric for evaluating the performance of any network.

Additionally, the `agenet` command-line script is included in the package, allowing for easy experimentation with the model with default or user-defined parameters. The simulation can generate both theoretical and simulated values for various factors such as block lengths, power allocations and packet sizes in the network.
## How to install

Install from PyPI:

```
pip install agenet
```

Or directly from GitHub:

```
pip install git+https://github.com/cahthuranag/agenet.git#egg=agenet
```

### Installing for development and/or improving the package

```
git clone https://github.com/cahthuranag/agenet.git
cd agenet
pip install -e .[dev]
```

This way, the package is installed in development mode. As a result, development dependencies are also installed.

## Documentation

For more detailed information about Agenet's features and usage, please refer to the [Agenet package documentation](https://cahthuranag.github.io/agenet/).

## License

[MIT License](LICENSE)

## References

1. Y. Polyanskiy, H. V. Poor, and S. Verdu, "Channel coding rate in the finite blocklength regime," IEEE Trans. Inf. Theory, vol. 56, no. 5, pp. 2307–2359, 2010.
2. C. M. Wijerathna Basnayaka, D. N. K. Jayakody, T. D. Ponnimbaduge Perera, and M. Vidal Ribeiro, "Age of information in an urllc-enabled decode-and-forward wireless communication system," in 2021 IEEE 93rd Vehicular Technology Conference (VTC2021-Spring), 2021, pp. 1–6.
3. R. D. Yates, Y. Sun, D. R. Brown, S. K. Kaul, E. Modiano, and S. Ulukus, "Age of information: An introduction and survey," IEEE Journal on Selected Areas in Communications, vol. 39, no. 5, pp. 1183–1210, 2021.

## Also in this documentation

* [Reference](reference.md)
* [Developing this package](dev.md)


