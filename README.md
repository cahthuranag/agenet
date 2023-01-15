[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/cahthuranag/Agewire/blob/3000891c482e715b3006264a88dfcf4ed4aedc7c/LICENSE)
![.github/workflows/test.yml](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)
# agewire
A Python 3.8 implementation of the System Model estimate the average AoI (AAoI) in an ultra-reliable low latency communication (URLLC) enabled wireless  communication system with decode-and-forward relay scheme  over the quasi-static Rayleigh block fading channels. A packet communication scheme is used to meet both the reliability and latency requirements of the  proposed wireless network. By resorting to finite block length information theory, queuing theory and stochastic processes, theoretical results were obtained for this research software.
## System Model
In this software,  a URLLC-enable DF cooperative relaying system is proposed as illustrated in figure, where the source $(S)$ sends its newly generated updates to the destination $(D)$ via aid of the relay $(R)$. 
![System model.](/figures/Fig1.png) 
In this proposed cooperative communication system, each transmission block is split into two separate time slots. The source sends data to the relay in the first time slot. Then, relay decodes and re-transmits the received data to the destination during the second time slot. It is assumed that there is no direct transmission between the source and the destination due to unfavourable line-of-sight (LoS) connection between them. The transmitted signal by the source, the received signal at the relay, the transmitted signal by the relay, and the received signal at the destination are denoted by $X_{1}$, $Y_{1}$, $X_{2}$ and $Y_{2}$, respectively. The received signal at each communication node can be written as
$$ Y_{1}=\sqrt{P_{S}} H_{SR}X_{1}+W_{SR},$$
$$ Y_{2}=\sqrt{P_{R}}H_{RD}X_{2}+W_{RD}, $$
where $H_{ij}$ is the channel coefficient of the channel between node $i$ to node $j$ where  $i\in \left \{ S,R \right \}$ and $j\in \left \{ R,D \right \}$. The symbol $W_{ij}$ denotes the independent and identically distributed Addictive white Gaussian noise (AWGN) of the channel with zero mean and $\sigma^2$ variance. In this work, transmit power of the communication node $i$ is modelled as 
$$P_{i} = \varphi_{i}P,$$
where $P$ is the total transmission power constraint of the system and $0<\varphi_{i}\leq 1$ is the power allocation factor of each communication node. The distance between the source and the destination is considered  as $d$ and the distance between the source and the relay is represented by $d\tau$, where $0<\tau<1$. The small scale channel gain is denoted as $g_{ij}=|h_{ij}^2|$, where $h_{ij} \sim\mathcal{C}\mathcal{N}(0,1)$ denotes the Rayleigh fading channel coefficient. The probability density function (PDF) of the small scale channel gain $g_{ij}$ can be expressed as 
$$ f_{g_{ij}}(z)=e^{-z}.$$
The large scale channel gain $\alpha_{ij}$ between the communication nodes can be written as 
$$ -10log(\alpha_{\textit{i}\textit{j}} )= 20 log(d_{\textit{i}\textit{j}})+20log\bigg(\frac{4\pi f_{c}}{C}\bigg), $$
where $f_{c}$ and $d_{ij}$ are the carrier frequency and distance between the communication nodes $i$ and $j$ respectively. The variable $C$ denotes the speed of light in the space. Considering small and large scale channel gains, the channel coefficient between the communication nodes can be written as
$$
    H_{ij}=\sqrt{\alpha_{ij}g_{ij}}.
$$
The normalized received signal-to-noise ratio (SNR) $\gamma_{j}$ at the receiving node $j$ can be written as
 $$\gamma_{\textit{j}} =\frac{ \alpha_{\textit{i}\textit{j}} g_{\textit{i}\textit{j}}P_{\textit{i}}}{\sigma_{ij}^{2}}. $$
### Block Error Probability in the Finite-Block Length Regime
Considering DF relay protocol, the overall decoding error probability can be written as
 $$ \varepsilon =\varepsilon _{R}+\varepsilon _{D}(1-\varepsilon _{R}), $$
where $\varepsilon _{R}$ is the block error probability at the relay, $\varepsilon _{D}$ is the block error probability at the destination. Due to the static nature of the communication channels, it is assumed that the fading coefficients stay constant over the duration of each transmission block. Following Polyanskiy's results on short packet communication and assuming that the receiver has perfect channel state information, the expectation of the block error probability of a given block length can be written as
$$ \varepsilon_{j}=\mathbb{E}\left [ Q\left ( \frac{n_{ij}C(\gamma_{j})-k}{\sqrt{n_{ij}V(\gamma_{j})}} \right ) \right ], $$
where  $\mathbb{E}\left [ . \right ]$ is the expectation operator, $Q(x)=\frac{1}{\sqrt{2\pi }}\int_{x}^{\infty }e^{-\frac{t_{2}}{2}}dt$ and $V(\gamma_{\textit{j}})$ is the  channel dispersion, which can be written $V(\gamma_{j} )=\frac{{\log _{2}}^{2}e}{2}(1-\frac{1}{(1+\gamma_{j} )^2})$. The variable $C(\gamma_{j})$ denotes the channel capacity of a complex AWGN channel and it is given by $C(\gamma_{j})=\log _{2}(1+\gamma_{j})$. The number of bits per block represents by $k$.
### Average Age of Information of the proposed URLLC-enabled relaying scheme
The AAoI of the proposed system can be derived as 
$$ \Delta_{a} = \frac{\frac{1}{2}\mathbb{E}\left [ X^{2} \right ]}{\mathbb{E}\left [ X \right ]}+\mathbb{E}\left [ s \right ]+\frac{}{}\frac{\mathbb{E}\left [ wX \right ]}{\mathbb{E}\left [ X \right ]}. $$

This equation has been used to calculate the theoretical AAoI in this software.

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
git clone  https://github.com/cahthuranag/agewire.git
cd 
pip install .
```

### Installing for development and/or improving the package

```
git clone https://github.com/cahthuranag/agewire.git
cd 
pip install -e .[dev]
```

This way, the package is installed in development mode. As a result, the pytest dependencies/plugins are also installed.

## Documentation

* [*Agewire* package documentation]()
* [Developer's guide]()
* [Scenario Description]()

## License

[MIT License](LICENSE)
## References

[1] [*Age of Information in an URLLC-enabled Decode-and-Forward Wireless Communication System*](https://ieeexplore.ieee.org/document/9449007)
