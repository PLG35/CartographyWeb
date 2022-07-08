# CartographyWeb
A tool crawling on a website to output a map of all the pages it contains.

## Dependencies
The code is made to run on Python 3.
In python 2.7, urllib.request should be replaced by urllib.

The library libCartography.py has the following dependencies :
- [urllib.request](https://docs.python.org/3/library/urllib.request.html)
- [urllib.parse](https://docs.python.org/3/library/urllib.parse.html)
- [html.parser](https://docs.python.org/3/library/html.parser.html)

## Input
As shown in the example, the main class of the library may be implemented with one and only one parameter : the URL of the webpage to test.

A second parameter is allowed to define how deep the crawler shall go. This parameter depth is defaulted to 2 (the root URL given at initialization and the URLs of links it contains).

## Output
The output is a string in JSON format containing :
> - status, providing the status failed or passed of the mapping.
> - maxdepth, reminding the value of the parameter depth used by the library when working of the mapping.
> - pages, providing a list of objects containing:
>   - url, showing the URL of the page.
>   - depth, providing the depth at which the page was found.
>   - status, providing the status of the parsing of the page.
>   - links, providing the list of URLs for which the page has a link to.

## Implementation

### Library
Cases where <a> balises are used to launch javascript functions are sorted out of the list of links returned by the method ParseURL.getLinks().

### Tests
Some tests require a valid URL to test. This URL is defined by the variable called :
> myTestURL

To launch those tests on your URL, in addition to the variable above, you will have to modify some expected values in the following tests :
- testGetLinks(self, testURL), where the value of expectation shall be modified to fit the content of the URL.
- testCartographie(self, testURL), where the value of expectation shall be modified to fit the content of the URL.