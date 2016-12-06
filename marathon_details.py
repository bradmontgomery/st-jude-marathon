"""
Fun facts about the St. Jude Memphis Marathons.

Data retrieved from:
https://www.stjude.org/get-involved/at-play/fitness-for-st-jude/memphis-marathon/participants/results.html

"""
import locale
import sys

from statistics import mean, median, mode
from collections import Counter

import parsers


RESULTS_FILES = {
    2002: 'data/stjude-marathon-agegroup-2002.txt',
    2003: 'data/stjude-marathon-top-2003.txt',
    2004: 'data/marathon-results-by-place-2004.txt',
    2005: 'data/marathon-results-by-place-2005.txt',
    2006: 'data/marathon-results-by-place-2006.txt',
    2007: 'data/marathon-results-by-place-2007.txt',
    2008: 'data/marathon-results-by-place-2008.txt',
    2009: 'data/marathon-results-by-place-2009.txt',
    2010: 'data/marathon-by-place-2010.txt',
    2011: 'data/marathon-results-by-place-2011.txt',
    2012: 'data/marathon-results-by-place-2012.txt',
    2014: 'data/marathon-results-by-place-2014.txt',
    2015: 'data/marathon-results-by-place-2015.HTML',
    2016: 'data/marathon-results-by-place-2016.HTML',
}

PARSERS = {
    2002: None,
    2003: None,
    2004: None,
    2005: None,
    2006: None,
    2007: None,
    2008: None,
    2009: None,
    2010: None,
    2011: None,
    2012: None,
    2014: None,
    2015: parsers.parse_2015,
    2016: parsers.parse_2016,
}


def print_data(year):
    locale.setlocale(locale.LC_ALL, '')  # Use locale to pretty-print the combined distance run.

    # parse our data...
    runners = None
    if year in RESULTS_FILES and year in PARSERS and PARSERS[year]:
        content = open(RESULTS_FILES[year]).read()
        runners = PARSERS[year](content)
    else:
        print("Sorry, either no data or parser for {}.".format(year))
        return

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
        print("Average age: {} mean / {} median / {} mode".format(
            int(mean(ages)), int(median(ages)), mode(ages)))

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
        mode_pace = mode(paces)
        mode_pace_minutes, mode_pace_seconds = divmod(mode_pace, 60)

        print("Average Pace: {}:{} mean / {}:{} median / {}:{} mode".format(
            mean_pace_minutes, mean_pace_seconds,
            median_pace_minutes, median_pace_seconds,
            mode_pace_minutes, mode_pace_seconds
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

        print("Average Finish Time: {} mean / {} median.".format(mean_time, median_time))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print_data(year=int(sys.argv[1]))
    else:
        print("Usage: python marathon_details.py <year>")
