"""
Fun facts about the 2016 St. Jude Memphis Marathon finishers:

See: http://www.besttimescct.com/results/marathon-results-by-place-2016.HTML


"""
import locale
from statistics import mean, median, mode
from collections import namedtuple, Counter
from html.parser import HTMLParser


RESULTS_FILE = "marathon-results-by-place-2016.HTML"


class TDParser(HTMLParser):
    """Keep all the text from <td> elements."""

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

        # elif tag == "td" and self.in_row:
            # print("Encountered a start tag:", tag)
            # Columns in the HTML doc:
            # Place	Name, Age, Sex/plc, Sex, Time, Pace, City, State, Bib No

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

            self.in_row = False
            self.row_values = []

    def handle_data(self, data):
        data = data.strip()
        if data and self.valid_cell:
            self.row_values.append(data)



if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')

    # print out some details about this thing.
    parser = TDParser()
    parser.feed(open(RESULTS_FILE).read())
    runners = parser.results

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