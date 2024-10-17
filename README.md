[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/cahthuranag/Agewire/blob/3000891c482e715b3006264a88dfcf4ed4aedc7c/LICENSE)
[![Tests](https://github.com/cahthuranag/agenet/actions/workflows/test.yml/badge.svg)](https://github.com/cahthuranag/agenet/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/cahthuranag/agenet/branch/main/graph/badge.svg?token=k8Ix6Zv8x9)](https://codecov.io/gh/cahthuranag/agenet)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docs](https://img.shields.io/badge/docs-stable-blue.svg)](https://cahthuranag.github.io/agenet/)
![GitHub Repo stars](https://img.shields.io/github/stars/cahthuranag/agenet?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/cahthuranag/agenet)

# agenet

Agenet is an open-source Python package designed to estimate the Age of Information (AoI) in cooperative wireless networks. By implementing a system model that combines finite blocklength information theory and AoI analysis over Rayleigh fading channels, Agenet provides researchers and practitioners with a comprehensive tool for studying short packet-based communication networks. This package is particularly valuable for those working on mission-critical wireless systems where the freshness of information is crucial.

## System model

The following figure illustrates the wireless communication system that is proposed in this application.

![System model.](https://raw.githubusercontent.com/cahthuranag/agenet/main/docs/docs/image/Fig1.png)

Agenet implements a short packet decode-and-forward (DF) cooperative wireless relaying system. This system consists of three key nodes: a source node (S) that generates and transmits new updates, a relay node (R) that receives, decodes, and forwards data, and a destination node (D) that receives the forwarded data. The communication process is structured into two time slots within each transmission block, with the source transmitting data to the relay in the first slot, and the relay decoding and forwarding the data to the destination in the second slot. This model accounts for both small-scale and large-scale channel gains, considering Rayleigh fading and path loss to provide a realistic representation of wireless communication environments.

## Features

Agenet offers a  set of features to support comprehensive analysis of wireless networks. The key features include:

- Signal-to-Noise Ratio (SNR) Calculation: Computes both instantaneous and average SNR for each receiving node.
- Block Error Probability Estimation: Calculates block error probabilities using finite blocklength information theory.
- Age of Information (AoI) Analysis: Provides tools to calculate both theoretical and simulated AoI.
- Flexible Parameter Configuration: Allows adjustment of various parameters such as power allocation, block length, packet size, and more.
- Monte Carlo Simulation: Supports multiple simulation runs for statistical reliability.
- Multi-parameter Analysis: Enables simulations across multiple parameter combinations for comprehensive system evaluation.

These features allow researchers to compare and validate their findings, facilitating in-depth exploration of different network scenarios. The package's support for Monte Carlo simulations and multi-parameter analysis makes it an invaluable tool for both academic research and practical applications in the field of wireless communications.

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



