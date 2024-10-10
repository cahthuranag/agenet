import argparse
from typing import List
from .bler import blercal_th
from .snratio import snr_th
from .maincom import multi_param_ev_sim
import pandas as pd

def _main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="AGENet CLI")
    # Add all your arguments here
    parser.add_argument("--d", type=float, nargs="+", default=[100], help="Distance(s) in meters")
    parser.add_argument("--N0", type=float, nargs="+", default=[1e-13], help="Noise power(s) in Watts")
    parser.add_argument("--fr", type=float, nargs="+", default=[6e6], help="Frame rate(s) in Hz")
    parser.add_argument("--num_events", type=int, nargs="+", default=[50], help="Number of events")
    parser.add_argument("--num_nodes", type=int, nargs="+", default=[5], help="Number of nodes")
    parser.add_argument("--active_prob", type=float, nargs="+", default=[0.2], help="Active probability")
    parser.add_argument("--n", type=int, nargs="+", default=[150], help="Total number of qubits")
    parser.add_argument("--k", type=int, nargs="+", default=[50], help="Number of information qubits")
    parser.add_argument("--P", type=float, nargs="+", default=[8e-2], help="Depolarizing probability")
    parser.add_argument("--num_runs", type=int, default=10, help="Number of simulation runs")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--quiet", action="store_true", help="Suppress output")
    parser.add_argument("--blockerror", action="store_true", help="Calculate theoretical block error rate")
    parser.add_argument("--snr", action="store_true", help="Calculate theoretical SNR")
    parser.add_argument("--csv", type=str, help="Save results to CSV file")

    args = parser.parse_args()

    # Always run the simulation
    result = multi_param_ev_sim(
        d=args.d, N0=args.N0, fr=args.fr, numevnts=args.num_events,
        num_nodes=args.num_nodes, active_prob=args.active_prob,
        n=args.n, k=args.k, P=args.P, numruns=args.num_runs, seed=args.seed
    )

    # Process output options
    if args.snr:
        theoretical_snr = snr_th(args.N0[0], args.d[0], args.P[0], args.fr[0])
        if not args.quiet:
            print(f"Theoretical SNR: {theoretical_snr}")

    if args.blockerror:
        theoretical_bler = blercal_th(args.n[0], args.k[0], args.P[0])
        if not args.quiet:
            print(f"Theoretical Block Error Rate: {theoretical_bler}")

    if args.csv:
        result.to_csv(args.csv, index=False)

    if not args.quiet:
        print(result)
