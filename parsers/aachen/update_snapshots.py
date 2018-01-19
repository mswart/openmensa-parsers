from urllib.request import urlretrieve

from parsers.aachen.regression_test import parse_mocked

url = 'http://www.studierendenwerk-aachen.de/speiseplaene/academica-w.html'

urlretrieve(url, 'snapshot-website.html')
with open('snapshot-result.xml', 'w') as result_file:
    result = parse_mocked(url)
    result_file.write(result)
