import matplotlib.pyplot as matplt
import plotext 
import pandas as pd
from datetime import datetime
from argparse import ArgumentParser
from utils import json_helper


def main():
    argparser = ArgumentParser(description="Plot a graph of given metadata file")
    argparser.add_argument("metadata_file", help="Metadata file that contains data to be plotted")
    argparser.add_argument("-f", "--field", help="Field to be plotted", nargs = "*", required=True)
    args = argparser.parse_args()

    metadata_dict = json_helper.read_json(args.metadata_file)

    metadata_df = pd.DataFrame.from_dict(metadata_dict, orient='index')

    field_list = args.field
    plot_data_series = pd.Series()
    for field in field_list:
        field_series = metadata_df.get(field)
        plot_data_series = plot_data_series.add(field_series, fill_value=0)
    
    date_x_axis = [datetime.fromtimestamp(float(epoch_timestamp)/1000).strftime("%d/%m/%Y") for epoch_timestamp in plot_data_series.index]

    # plotext.scatter(date_x_axis, plot_data_series.values)
    # plotext.show()

    fig, ax = matplt.subplots()
    ax.scatter(date_x_axis,plot_data_series.values)
    matplt.show()


if __name__ == "__main__":
    main()