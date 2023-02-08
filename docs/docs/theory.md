# Theory
## overview 

This section explains the theoretical basis for this system model. In this system, we analyze the age of information of a wireless communication model with several nodes. 
### Simulation Parameters

The _clugen_ algorithm (and consequently, the [`clugen()`][pyclugen.main.clugen]
function) has mandatory and optional parameters, listed and described in the tables
below. The optional parameters are set to sensible defaults, and in many situations
may be left unchanged. Nonetheless, these allow all of the algorithm's steps to be
fully customized by the user.

#### Mandatory parameters

| Symbol         | Parameter         | Description                                                      |
|:-------------- |:----------------- |:---------------------------------------------------------------- |
| $n$            | `num_dims`        | Number of dimensions.                                            |
| $c$            | `num_clusters`    | Number of clusters.                                              |
| $p$            | `num_points`      | Total number of points to generate.                              |
| $\mathbf{d}$   | `direction`       | Average direction of cluster-supporting lines ($n \times 1$).  |
| $\theta_\sigma$| `angle_disp`      | Angle dispersion of cluster-supporting lines (radians).          |
| $\mathbf{s}$   | `cluster_sep`     | Average cluster separation in each dimension ($n \times 1$).   |
| $l$            | `llength`         | Average length of cluster-supporting lines.                      |
| $l_\sigma$     | `llength_disp`    | Length dispersion of cluster-supporting lines.                   |
| $f_\sigma$     | `lateral_disp`    | Cluster lateral dispersion, i.e., dispersion of points from their projection on the cluster-supporting line. |