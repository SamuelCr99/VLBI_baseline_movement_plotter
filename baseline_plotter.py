from utility.gui.gui import run_gui
from utility.plot.plot_baseline import plot_lines
from utility.data_selection.find_matching_station_data import find_matching_station_data
import argparse
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    """
    To run in GUI mode simply run the script with no arguments 

    In script mode the following arguments are available:
    station1: str - Station name of first station in baseline (required)
    station2: str - Station name of second station in baseline (required)
    --no_scatter: bool - Don't plot scatter plot (optional)
    --no_residual: bool - Don't plot residual plot (optional)
    --no_rolling_std: bool - Don't plot rolling std plot (optional)
    --no_raw: bool - Don't plot raw data (optional)
    --no_trimmed: bool - Don't plot trimmed data (optional)
    --no_trendline: bool - Don't plot trendline (optional)
    --outlier_lim: float - Limit for outliers in standard deviations (optional)
    --save_plots: bool - Save plots to file (optional)
    --show_plots: bool - Show plots (optional)
    --file_type: str - File type to save plots as (optional)
    --window_size: float - Window size for rolling std (months) (optional)
    """
    if len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == "--compat_mode":
        compat_mode = True if len(sys.argv) == 2 else False
        run_gui(compat_mode)

    else:
        # Create parser to allow program to be run in script mode
        parser = argparse.ArgumentParser(
            prog='Plot baseline',
            description='Plots baselines between 2 given stations')

        parser.add_argument('station1', type=str)
        parser.add_argument('station2', type=str)
        parser.add_argument('--no_scatter', action='store_true', help="don't plot scatter plot")
        parser.add_argument('--no_residual', action='store_true', help="don't plot residual plot")
        parser.add_argument('--no_rolling_std', action='store_true', help="don't plot rolling std plot")
        parser.add_argument('--no_raw', action='store_true', help="don't plot raw data")
        parser.add_argument('--no_trimmed', action='store_true', help="don't plot trimmed data")
        parser.add_argument('--no_trendline', action='store_true', help="don't plot trendline")
        parser.add_argument('--outlier_lim', type=float, default=3, help="limit for outliers in standard deviations")
        parser.add_argument('--start', type=float, default=1950, help="start year")
        parser.add_argument('--end', type=float, default=2023, help="end year")

        parser.add_argument('--save_plots', action='store_true', help="save plots to file")
        parser.add_argument('--show_plots', action='store_true', help="show plots")
        parser.add_argument('--file_type', type=str, default="png", help="file type to save plots as")
        parser.add_argument('--compat_mode', action='store_true', help="flag for increased compatibility when running GUI. Only use if plots don't work normally")
        # Note that compat_mode does not do anything in script mode. Only reason it is added as argument is so it appears when -h is run


        parser.add_argument('--window_size', type=float, default=12, help="window size for rolling std (months)")
        args = parser.parse_args()

        plotSettings = {
            "scatter": not args.no_scatter,
            "scatterRaw": not args.no_raw,
            "scatterTrimmed": not args.no_trimmed,
            "scatterTrendline": not args.no_trendline,
            "scatterLim": args.outlier_lim,
            "residual": not args.no_residual,
            "residualRaw": not args.no_raw,
            "residualTrimmed": not args.no_trimmed,
            "rolling_std": not args.no_rolling_std,
            "rolling_stdRaw": not args.no_raw,
            "rolling_stdTrimmed": not args.no_trimmed,
            "rolling_stdWindowSize": args.window_size/12
        }

        viewSettings = {
            "display": args.show_plots,
            "save": args.save_plots,
            "saveFormat": args.file_type
        }

        data = find_matching_station_data(args.station1, args.station2, args.start, args.end)
        plot_lines(data, 'length', plotSettings, viewSettings)
        if args.show_plots:
            plt.show()
