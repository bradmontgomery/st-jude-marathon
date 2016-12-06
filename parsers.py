"""

This module parses the data files from each year.

"""
from collections import namedtuple
from html.parser import HTMLParser


class TDParser(HTMLParser):
    """This is a simple HTML parser that keeps all the text from <td> elements.

    Required:

    - columns:  A list of column names for each column in the table to be parsed.

    Returns:

    Upon completion, this parser will have a `results` attribute containing
    a list of namedtuple objects for each row in the table. The names of the
    nametuple are generated from the provided column names.

    """

    def __init__(self, *args, **kwargs):
        self.columns = kwargs.pop('columns')
        if self.columns is None:
            raise ValueError("Must provide a list of column names for this Parser")
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
            Runner = namedtuple("Runner", self.columns)
            self.results.append(Runner(*self.row_values))

            self.in_row = False  # we're done processing a row.
            self.row_values = []  # reset for the next row.

    def handle_data(self, data):
        # Saves the data from each <td> cell.
        data = data.strip()
        if data and self.valid_cell:
            self.row_values.append(data)


def parse_2016(content):
    """Given a a string of content, parse it & return a list of namedtuples"""
    # Place, Name, Age, Sex/plc, Sex, Time, Pace, City, State, Bib No
    cols = [
        'place', 'first_name', 'last_name', 'age', 'sexpl', 'sex',
        'time', 'pace', 'city', 'state', 'bib'
    ]
    parser = TDParser(columns=cols)
    parser.feed(content)
    return parser.results


def parse_2015(content):
    """Given a a string of content, parse it & return a list of namedtuples"""
    # Place, Name, Age, Sex/plc, Sex, Time, Pace, City, State, Bib No,
    # Clock Time, Link (NOTE: not sure why omitting the link works, but it does)
    cols = [
        'place', 'first_name', 'last_name', 'age', 'sexpl', 'sex',
        'time', 'pace', 'city', 'state', 'bib', 'clocktime',
    ]
    parser = TDParser(columns=cols)
    parser.feed(content)
    return parser.results
