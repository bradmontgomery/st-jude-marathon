"""
Fun facts about the St. Jude Memphis Marathons.

Data retrieved from:
https://www.stjude.org/get-involved/at-play/fitness-for-st-jude/memphis-marathon/participants/results.html

"""
import locale
import sys

from statistics import mean, median, mode
from collections import namedtuple, Counter
from html.parser import HTMLParser


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


class TDParser(HTMLParser):
    """This is a simple HTML parser that keeps all the text from <td> elements."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.in_row = False  # Are we processing a row of data?
        self.valid_cell = False  # Are we processing valid cell of data (a <td>)
        self.row_values = []  # The values from a row of data
        self.results = []  # A list of namedtuples that we'll keep for all results.

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_row = True

        # Make sure we only get data from <td> cells.
        if tag == "td":
            self.valid_cell = True
        else:
            self.valid_cell = False

    def handle_endtag(self, tag):
        if tag == "tr" and len(self.row_values) > 0:
            # We're done processing a row, turn it into a namedtuple and
            # store in our list of final results.
            # Place, Name, Age, Sex/plc, Sex, Time, Pace, City, State, Bib No
            props = [
                'place', 'first_name', 'last_name', 'age', 'sexpl', 'sex',
                'time', 'pace', 'city', 'state', 'bib'
            ]
            Runner = namedtuple("Runner", props)
            self.results.append(Runner(*self.row_values))

            self.in_row = False  # we're done processing a row.
            self.row_values = []  # reset for the next row.

    def handle_data(self, data):
        # Saves the data from each <td> cell.
        data = data.strip()
        if data and self.valid_cell:
            self.row_values.append(data)


def print_data(year):
    locale.setlocale(locale.LC_ALL, '')  # Use locale to pretty-print the combined distance run.

    # parse our data...
    parser = TDParser()
    try:
        parser.feed(open(RESULTS_FILES[year]).read())
    except FileNotFoundError:
        print("No data for {}.".format(year))
        return

    runners = parser.results  # Save the results in a friendly name.

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
