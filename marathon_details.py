"""
Fun facts about the St. Jude Memphis Marathons.

Data retrieved from:
https://www.stjude.org/get-involved/at-play/fitness-for-st-jude/memphis-marathon/participants/results.html

"""
import locale
import sys

from statistics import mean, median, mode, StatisticsError
from collections import Counter

import tablib
import parsers


def is_numeric(value):
    """given some value, test if it's numeric & can safely be converted to an int"""
    return any([
        type(value) is str and value.isnumeric(),
        hasattr(value, 'is_integer') and value.is_integer(),
        type(value) is int,
    ])


def print_data(year):
    """
    Print some fun facts & stats for the given year's marathon.

    """
    locale.setlocale(locale.LC_ALL, '')  # Use locale to pretty-print the combined distance run.

    # parse our data...
    runners = parsers.parse(year)
    if runners:

        print("\n\n{} Marathon Runners".format(len(runners)))
        print("From {} different states".format(len(set(runner.state for runner in runners))))
        print("Total distance combined ==> {:n}+ miles".format(int(len(runners) * 26.2)))

        print("Mostly from (top-10 cities):")
        cities = Counter(runner.city for runner in runners)
        for city, count in cities.most_common(10):
            print("- {} ({})".format(city, count))

        # Average age.
        ages = [int(runner.age) for runner in runners if is_numeric(runner.age)]
        try:
            mode_age = mode(ages)
        except StatisticsError:
            mode_age = 'No unique'

        print("Average age: {} mean / {} median / {} mode".format(
            int(mean(ages)), int(median(ages)), mode_age))

        # Count Female / Male participants.
        females = len([runner.sex for runner in runners if runner.sex == "F"])
        males = len([runner.sex for runner in runners if runner.sex == "M"])
        print("Females: {}!\nMales: {}!".format(females, males))

        # Calculate Average paces.
        paces = []
        for runner in runners:
            minutes, seconds = runner.pace.split(":")
            paces.append(int(seconds) + (int(minutes) * 60))

        mean_pace = int(mean(paces))
        mean_pace_minutes, mean_pace_seconds = divmod(mean_pace, 60)
        median_pace = int(median(paces))
        median_pace_minutes, median_pace_seconds = divmod(median_pace, 60)

        try:
            mode_pace = mode(paces)
            mode_pace_minutes, mode_pace_seconds = divmod(mode_pace, 60)
            mode_pace = "{}:{}".format(mode_pace_minutes, mode_pace_seconds)
        except StatisticsError:
            mode_pace = 'No unique'

        print("Average Pace: {}:{} mean / {}:{} median / {} mode".format(
            mean_pace_minutes, mean_pace_seconds,
            median_pace_minutes, median_pace_seconds,
            mode_pace
        ))

        # Average finish times.
        times = []
        for runner in runners:
            hours, minutes, seconds = runner.time.split(":")
            times.append(int(seconds) + (int(minutes) * 60) + (int(hours) * 3600))

        mean_time = int(mean(times))
        minutes, seconds = divmod(mean_time, 60)
        hours, minutes = divmod(minutes, 60)
        mean_time = "{}:{}:{}".format(hours, minutes, seconds)

        median_time = int(median(times))
        minutes, seconds = divmod(median_time, 60)
        hours, minutes = divmod(minutes, 60)
        median_time = "{}:{}:{}".format(hours, minutes, seconds)

        try:
            mode_time = mode(times)
            minutes, seconds = divmod(mode_time, 60)
            hours, minutes = divmod(minutes, 60)
            mode_time = "{}:{}:{}".format(hours, minutes, seconds)
        except StatisticsError:
            mode_time = 'No unique'
        print("Average Finish Time: {} mean / {} median / {} mode.".format(
            mean_time, median_time, mode_time))
    else:
        print("Sorry, either no data or parser for {}.".format(year))


def export_data():
    """
    Generate a CSV for all the years in which we have a parser.

    """
    # What we'll keep:
    # - total_runners
    # - num males
    # - num females
    # - num states
    # - combined distance
    # - average age (mean)
    # - average pace (mean)
    # - average finish time (mean)
    headers = [
        'Total Runners', 'Males', 'Females', 'States', 'Combined Distance',
        'Mean Age', 'Mean Pace', 'Mean Finish Time',
    ]
    data = tablib.Dataset(headers=headers)

    years = sorted([
        year for year, parser in parsers.PARSERS.items()
        if parser is not None
    ])
    for year in years:
        # parse the the data fot he year
        runners = parsers.parse(year)
        row = []
        if runners:

            row.append(len(runners))  # Total Runners
            row.append(len([runner.sex for runner in runners if runner.sex == "F"]))
            row.append(len([runner.sex for runner in runners if runner.sex == "M"]))
            row.append(len(set(runner.state for runner in runners)))  # Sates
            row.append(int(len(runners) * 26.2))  # Combined Distance

            # Average age.
            ages = [int(runner.age) for runner in runners if is_numeric(runner.age)]
            row.append(int(mean(ages)))

            # Average pace.
            paces = []
            for runner in runners:
                minutes, seconds = runner.pace.split(":")
                paces.append(int(seconds) + (int(minutes) * 60))
            mean_pace = int(mean(paces))
            mean_pace_minutes, mean_pace_seconds = divmod(mean_pace, 60)
            mean_pace = "{}:{}".format(mean_pace_minutes, mean_pace_seconds)
            row.append(mean_pace)

            # Average finish times.
            times = []
            for runner in runners:
                hours, minutes, seconds = runner.time.split(":")
                times.append(int(seconds) + (int(minutes) * 60) + (int(hours) * 3600))
            mean_time = int(mean(times))
            minutes, seconds = divmod(mean_time, 60)
            hours, minutes = divmod(minutes, 60)
            mean_time = "{}:{}:{}".format(hours, minutes, seconds)
            row.append(mean_time)

            # Append to our dataset
            data.append(row)
            print('Calculated data for {}...'.format(year))

    with open("output.csv", "w") as csvfile:
        csvfile.write(data.csv)
        print("Output written to 'output.csv'")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'export':
        export_data()
    elif len(sys.argv) == 2:
        print_data(year=int(sys.argv[1]))
    else:
        print("USAGE:\n\tpython marathon_details.py <year>")
        print("OR:\n\tpyton marathon_details.py export")
