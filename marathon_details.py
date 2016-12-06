"""
Fun facts about the St. Jude Memphis Marathons.

Data retrieved from:
https://www.stjude.org/get-involved/at-play/fitness-for-st-jude/memphis-marathon/participants/results.html

"""
import locale
import sys

from statistics import mean, median, mode, StatisticsError
from collections import Counter

import parsers


def print_data(year):
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
        ages = [int(runner.age) for runner in runners]
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

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print_data(year=int(sys.argv[1]))
    else:
        print("Usage: python marathon_details.py <year>")
