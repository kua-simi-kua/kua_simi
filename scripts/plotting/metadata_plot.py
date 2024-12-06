import matplotlib.pyplot as matplt
import plotext 
import pandas as pd
from datetime import datetime
from argparse import ArgumentParser
from utils import json_helper

COLOUR_LIST = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


def main():
    argparser = ArgumentParser(description="Plot a graph of given metadata file")
    argparser.add_argument("-mf", "--metadata_file", help="Metadata file that contains data to be plotted", nargs = "*", required=True)
    argparser.add_argument("-f", "--field", help="Field to be plotted", nargs = "*", required=True)
    args = argparser.parse_args()

    metadata_dict = {}
    for mfile in args.metadata_file:
        mdict = json_helper.read_json(mfile)
        metadata_dict.update(mdict)


    metadata_df = pd.DataFrame.from_dict(metadata_dict, orient='index')

    field_list = args.field
    plot_data_series = pd.Series()
    plot_data_series_list = []
    for field in field_list:
        field_series = metadata_df.get(field)
        plot_data_series_list.append(field_series)
        plot_data_series = plot_data_series.add(field_series, fill_value=0)

    
    date_x_axis = [datetime.fromtimestamp(float(epoch_timestamp)/1000).strftime("%d/%m") for epoch_timestamp in plot_data_series.index]

    # plotext.scatter(date_x_axis, plot_data_series.values)
    # plotext.show()

    fig, ax = matplt.subplots()
    # ax.scatter(date_x_axis,plot_data_series.values)

    colour_counter = 0
    for f_series in plot_data_series_list:
        print(f_series.head(2))
        print("Hello")
        ax.plot(date_x_axis,f_series.values, color=COLOUR_LIST[colour_counter])
        colour_counter += 1
    # matplt.xticks([])
    # matplt.yticks([])

    matplt.show()


if __name__ == "__main__":
    main()