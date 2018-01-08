OpenMensa Parsers
=================

[![Build Status](https://api.travis-ci.org/mswart/openmensa-parsers.svg)](https://travis-ci.org/mswart/openmensa-parsers)

[OpenMensa] is a free canteen database. It depends on external parsers that provide the meal information for the specific canteens.

This repository contains a large collection of parsers for different canteens all over Germany - mostly university canteens provided by student unions.

Before you continue you may want to read the [feed documentation] describing the exchange format between parsers and OpenMensa.


## Contribute

**Corrections Welcome**: As I do not use most of the parsers myself it is likely that I miss some parsing issues. Feel free to report an issue or even better provide a pull request.

**Hosting Provided**: Your canteen is missing? You could write a parser for your canteen (in Python)? But you do not know where to host the parser? I can host your parser at omfeeds.devtation.de. Please provide a PR with the new parser.


## Overall Structure

The parsers itself are independent. But there is a small framework handling common tasks like URL parsing and output generation.

Each provider has it's own Python module. A provider represents a collection of canteens which are organisationally dependent and therefore can be parsed by the same process. The module itself has to implement a `parse_url(canteenidentifier, today=False)` method. This method is called to parse and return the feed for a specific canteen. What the `canteenidentifier` is exactly is up to the provider - mostly they are URL parts or URL suffixes.

The [config.py] contains a list of all known providers and it's canteens (plus the `canteenidentifier` that is passed to the `parse_url` method). The structure is hopefully self explaining. If not, please open an issue.


## Common implementation details of providers

At the moment all providers using [PyOpenMensa] ([documentation](https://pyopenmensa.readthedocs.io/), [repo](https://github.com/mswart/pyopenmensa)) to generate the XML feed and for some help for the parsing itself.

As many meal information are only available online as HTML, [Beautiful Soup 4] is used as a robust but easy to use HTML parser.


## Get started

1. Clone the source code

        git clone --recurse-submodules git://github.com/mswart/openmensa-parsers

2. Install the dependecies:
   * [Python 3]
   * [Beautiful Soup 4] - needed for most parsers/providers.
   * [python-lxml] Some parsers using the `lxml` backend of Beautiful Soup, so you might need the Python `lxml` module/extension.

3. Try some parsers

        python3 parse.py magdeburg ovgu-unten full.xml

   general:

        python3 parse.py <provider name> <canteen name> <feed name>.xml

   Almost all parsers implement a feed called `full` including all available menu information. Most parsers implement also a `today` feed returning primarily the menu for today.


## Tips for adding a new provider

1. Search where the meal information are accessible online. JSON or CSV downloads are mostly the best, HTML sites are also possible, but PDF is tricky.
2. Maybe take some look on other parsers how they solve the problem / which libraries they use.
3. Create the new provider
4. Register your provider with its canteens in `config.py`
5. Submit a PR
6. Wait until the PR is reviewed and merged
6. Register the new canteens on openmensa with the feed from `http://omfeeds.devtation.de/<provider identifier>/<canteen identifier>.xml` and (optional) today feed from `http://omfeeds.devtation.de/<provider identifier>/<canteen identifier>/today.xml`


## Further questions

* Read the [OpenMensa Documentation]
* Ask at the OpenMensa IRC channel `freenode#openmensa`
* The [add howto for developers of new parser](https://github.com/mswart/openmensa-parsers/issues/2) issue may be helpful.
* Open an issue

[OpenMensa]: https://openmensa.org
[OpenMensa Documentation]: https://doc.openmensa.org
[feed documentation]: https://doc.openmensa.org/feed/v2/
[config.py]: config.py
[PyOpenMensa]: https://pypi.python.org/pypi/pyopenmensa
[Beautiful Soup 4]: https://www.crummy.com/software/BeautifulSoup/
[python-lxml]: http://lxml.de/
[Python 3]: https://www.python.org/
