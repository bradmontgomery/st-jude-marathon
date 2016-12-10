St. Jude Memphis Marathon
-------------------------

This repo contains some tools to analyze the Marathon results from the
St. Jude Memphis Marathon.

## Contents

The `data/` directory contains (slightly sanitized) results from the 2002-2015
marathons, except for 2013 which got cancelled due to weather. This data came
from [the official results site](https://www.stjude.org/get-involved/at-play/fitness-for-st-jude/memphis-marathon/participants/results.html).

The `output/` directory contains some text files with generated facts &amp;
stats for each year.

## Usage

Run `python marathon_details.py <year>`, e.g.
`python marathon_details.py 2016` should give you the most recent results.

**Note** This is a work in progress, and I haven't yet written parsers for
each year.


## License

This python code in this repo is available under the terms of the MIT license
(see the LICENSE.txt file in this repo).
