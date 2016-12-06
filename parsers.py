"""

This module parses the data files from each year.

"""
from pandas import read_fwf
from collections import namedtuple
from html.parser import HTMLParser


# Map a year to the file containing its data.
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


def parse(year):
    """Parse the correct file for a given year."""
    if year in RESULTS_FILES and year in PARSERS and PARSERS[year]:
        parser = PARSERS[year]
        return parser(year, RESULTS_FILES[year])
    return None


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


def parse_2016(year, file):
    """Given a a string of content, parse it & return a list of namedtuples"""
    with open(file) as file:
        content = file.read()
        # Place, Name, Age, Sex/plc, Sex, Time, Pace, City, State, Bib No
        cols = [
            'place', 'first_name', 'last_name', 'age', 'sexpl', 'sex',
            'time', 'pace', 'city', 'state', 'bib'
        ]
        parser = TDParser(columns=cols)
        parser.feed(content)
        return parser.results


def parse_2015(year, file):
    """Given a a string of content, parse it & return a list of namedtuples"""
    with open(file) as file:
        content = file.read()
        # Place, Name, Age, Sex/plc, Sex, Time, Pace, City, State, Bib No,
        # Clock Time, Link (NOTE: not sure why omitting the link works, but it does)
        cols = [
            'place', 'first_name', 'last_name', 'age', 'sexpl', 'sex',
            'time', 'pace', 'city', 'state', 'bib', 'clocktime',
        ]
        parser = TDParser(columns=cols)
        parser.feed(content)
        return parser.results


def text_parser(content, columns):
    expected_items = len(columns)
    results = []
    for row in content.split("\n"):
        items = row.split()
        if len(items) == expected_items and not (
            items[0].startswith('=') or items[0].startswith('Place')
        ):
            Runner = namedtuple("Runner", columns)
            results.append(Runner(*items))
    return results


def parse_11_col_text(year, file):
    results = []
    # File had been modified to have a header (with ==='s underneath), so treat
    # the first two lines as headers.
    cols = [
        'place', 'first_name', 'last_name', 'age', 'sexpl', 'sex',
        'time', 'pace', 'city', 'state', 'bib',
    ]
    data = read_fwf(file, header=[0, 1])
    for index, row in data.iterrows():
        Runner = namedtuple("Runner", cols)
        results.append(Runner(*row))
    return results


# Map a year to a parser.
PARSERS = {
    2002: None,
    2003: None,
    2004: None,
    2005: None,
    2006: None,
    2007: None,
    2008: None,
    2009: parse_11_col_text,
    2010: parse_11_col_text,
    2011: parse_11_col_text,
    2012: parse_11_col_text,
    2014: parse_11_col_text,
    2015: parse_11_col_text,
    2016: parse_11_col_text,
}
