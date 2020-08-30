# OpenMensa Parsers
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


# Writing Parsers
## Learn
At the moment all providers in this repo are using [PyOpenMensa] ([documentation](https://pyopenmensa.readthedocs.io/), [repo](https://github.com/mswart/pyopenmensa)) to generate the XML feed and for the parsing itself.

As often the menu is only available as HTML, [Beautiful Soup 4] is used as a robust but easy to use HTML parser.

1. Clone the source code:

        git clone --recurse-submodules git://github.com/mswart/openmensa-parsers

2. Install the dependencies:
   * [Python 3]
   * [Beautiful Soup 4] - needed for most parsers/providers.
   * [python-lxml] Some parsers use the `lxml` backend of Beautiful Soup, so you might need the Python `lxml` module/extension.

3. See a working example of a feed. E. g. from the `ovgu-unten` canteen in `magdeburg`:

        python3 parse.py magdeburg ovgu-unten full.xml

   Command usage:

        python3 parse.py <provider name> <canteen name> <feed>.xml

   The `full` feed returns the entire menu and is called once a day. Alternatively, the `today` feed is called hourly, but is meant to only return today's menu. Use one of these as `<feed>` in the command.
    
4. Look at the parser's source code. All the `magdeburg` parsers are defined in `parsers/magedburg.py`. This is because the canteens only differ in their URLs and can share the same parser.

   You can compare multiple parsers to see what libraries they use and how they register parsers.


## Write
Let's imagine you want to create a parser for the `eatmaginary` canteen located in `essendorf`.

1. Find a online resource where the `eatmaginary` menu is accessible online.
   - JSON or CSV downloads are preferred
   - HTML sites are fine
   - PDF is tricky.
2. Create the new parser in e. g. `parsers/essendorf.py`. It has to have a function that creates a valid XML feed.
3. Export a `parser` by making it a global variable in `parsers/essendorf.py`. Use the `Parser` class from `utils.py` and pass it the function that creates the XML feed. You can also register multiple canteens with the same parser. Look at some parsers' source code to get a feel for how this works.
4. Register your parser in `config.py`. Normally it is enough to add your city, e. g. `essendorf`, to the `cities` list.
5. If you want to refactor your parser, you can create a [regression test](#regression-tests) that will tell you, if you've changed how the parser works.
6. Submit a PR to GitHub containing these changes. ([Tutorial](https://guides.github.com/activities/hello-world/#pr) for opening a pull request.)
7. Wait until the PR is reviewed and merged.
8. Register the new canteens on [openmensa] with the feed from `http://omfeeds.devtation.de/<provider identifier>/<canteen identifier>.xml` and (optional) today feed from `http://omfeeds.devtation.de/<provider identifier>/<canteen identifier>/today.xml`.
   In our example these URLs would be `http://omfeeds.devtation.de/essendorf/eatmaginary.xml`.

## <a name="snapshot-tests">Snapshot tests</a>
If you want to refactor your parser, that is you want to change the code, but the output should stay the same, then you can make use of snapshot tests. First, you create a snapshot of the current result. Then you make changes to your parser and test if the changed parser has a new result. If the result really is different, you might have an error in your code. Or you might find that the new result is better, in which case you can simply create a new snapshot that will be used for future tests.

To create or update a snapshot for the parser `aachen/academica`, you need to be in this repository's root directory (this README is in that directory) and run
```bash
python -m snapshot_tests.update aachen academica
```

To test for changes, install pytest (`pip install pytest`) and run
```bash
pytest snapshot_tests
```

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
