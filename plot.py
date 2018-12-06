#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from collections import defaultdict, OrderedDict

from matplotlib import pyplot

from gpx import track_day, track_distance


def main(arguments: Namespace):
    data = [
        {
            'file': gpx_file,
            'day': track_day(gpx_file),
            'distance': track_distance(gpx_file),
        } for gpx_file in arguments.gpx_files
    ]
    plot_by_month(data)
    plot_by_weekday(data)


def plot_by_month(data):
    # aggregate data by months
    agg = defaultdict(float)
    for gpx in data:
        month = gpx['day'].strftime('%Y-%m')
        agg[month] += gpx['distance']
    agg_ordered = OrderedDict([
        (month, agg[month])
        for month in sorted(agg)
    ])
    pyplot.plot(agg_ordered.keys(), agg_ordered.values())
    pyplot.show()


def plot_by_weekday(data):
    # aggregate data by weekday
    agg = defaultdict(float)
    for gpx in data:
        weekday = gpx['day'].strftime('%w%A')
        agg[weekday] += gpx['distance']
    agg_ordered = OrderedDict([
        (weekday, agg[weekday])
        # Sunday should be the last day of the week
        for weekday in sorted(agg, key=lambda v: int(v[0]) or 7)
    ])
    pyplot.bar(
        [weekday[1:] for weekday in agg_ordered.keys()],
        agg_ordered.values())
    pyplot.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('gpx_files', nargs='+')

    main(parser.parse_args())
