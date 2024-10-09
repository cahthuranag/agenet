import argparse
from typing import List
from .bler import blercal_th
from .snratio import snr_th
from .maincom import multi_param_ev_sim
import pandas as pd

def _main() -> None:
    """Command-line arguments and calls the multi_param_ev_sim function."""
    parser = argparse.ArgumentParser(
        description="Run multi-parameter event simulation and return results as a DataFrame."
    )
    
    parser.add_argument("--d", nargs="+", type=float, default=[700],
                        help="List of distances between nodes.")
    parser.add_argument("--N0", nargs="+", type=float, default=[1e-13],
                        help="List of noise power values.")
    parser.add_argument("--fr", nargs="+", type=float, default=[6e9],
                        help="List of signal frequencies.")
    parser.add_argument("--num-events", nargs="+", type=int, default=[50],
                        help="List of number of events.")
    parser.add_argument("--num-nodes", nargs="+", type=int, default=[5],
                        help="List of number of nodes.")
    parser.add_argument("--active-prob", nargs="+", type=float, default=[0.2],
                        help="List of active probabilities.")
    parser.add_argument("--n", nargs="+", type=int, 
                        default=[150],
                        help="List of block lengths.")
    parser.add_argument("--k", nargs="+", type=int, default=[50],
                        help="List of update sizes.")
    parser.add_argument("--P", nargs="+", type=float, 
                        default=[8e-2],
                        help="List of power values.")
    parser.add_argument("--num-runs", type=int, default=10,
                        help="Number of runs for each parameter combination.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducibility.")

    parser.add_argument("--quiet", action="store_true", help="Omit tables")
    parser.add_argument("--blockerror", action="store_true", help="Show theoretical block error")
    parser.add_argument("--snr", action="store_true", help="Show snr")
    parser.add_argument("--csv", type=str, help="Location to save csv file")

    args = parser.parse_args()

    output_action_taken = False

    if args.snr:
        # Note: This might need adjustment as we don't have single values for these parameters anymore
        snr_th_val = snr_th(args.N0[0], args.d[0], args.P[0], args.fr[0])
        print(f"Theoretical SNR: {snr_th_val}")
        output_action_taken = True

    if args.blockerror:
        # Note: This might need adjustment as we don't have single values for these parameters anymore
        ber_th = blercal_th(args.snr, args.n[0], args.k[0])
        print(f"Theoretical Block Error Rate: {ber_th}")
        output_action_taken = True
    pd.set_option("display.max_rows", 10000000)
    if not output_action_taken and not args.quiet:
        results = multi_param_ev_sim(
            d=args.d,
            N0=args.N0,
            fr=args.fr,
            numevnts=args.num_events,
            num_nodes=args.num_nodes,
            active_prob=args.active_prob,
            n=args.n,
            k=args.k,
            P=args.P,
            numruns=args.num_runs,
            seed=args.seed
        )
        if not  args.quiet:
            print(results)
        if args.csv:
            results.to_csv(args.csv, index=False)