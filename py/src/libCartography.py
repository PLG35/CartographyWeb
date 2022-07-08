# -*-coding:Latin-1 -*
import urllib.request
import urllib.parse
import html.parser

# Error handling adresse like : https://www.w3schools.comdefault.asp

class FindLinks(html.parser.HTMLParser):
    def __init__(self, *args, **kwargs):
        super(FindLinks, self).__init__(*args, **kwargs)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if(tag == "a"):
            for attr in attrs:
                if(attr[0] == 'href'):
                    link = attr[1].replace("\\'","")
                    if link[0] == ".":
                        link = link[1:]
                    self.links.append(link)

class FindContentByTag(html.parser.HTMLParser):
    def __init__(self, *args, **kwargs):
        super(FindContentByTag, self).__init__(*args, **kwargs)
        self.contents = []
        self.test = False

    def setTagname(self, tagName):
        self.tag = tagName

    def handle_starttag(self, tag, attrs):
        if tag == self.tag:
            self.test = True
        else:
            self.test = False

    def handle_data(self, data):
        if self.test:
            data = data.replace("\\n", "")
            data = data.replace("\\t", "")
            if len(data) > 0:
                self.contents.append(data)

class ParseURL:
    def __init__(self, url):
        self.myURL = url
        urlComponents = urllib.parse.urlparse(self.myURL)
        self.myComponents = [urlComponents.scheme, urlComponents.netloc, urlComponents.path, urlComponents.params, urlComponents.query, urlComponents.fragment]

    def getLinks(self):
        if not self.parseFailed:
            htmlContent = self.urlOpened.read()
            self.strHtml = str(htmlContent)

            # Parse HTML content
            myParser = FindLinks()
            myParser.feed(self.strHtml)

            # Format links found
            for link in myParser.links:
                # Prevent issues with <a> using a javascript handler
                if link[0:11] != "javascript:":

                    urlComponents = urllib.parse.urlparse(link)
                    formattedLink = ""
                    
                    if urlComponents.scheme == "":
                        formattedLink += self.myComponents[0]
                    else:
                        formattedLink += urlComponents.scheme
                    formattedLink += "://"

                    if urlComponents.netloc == "":
                        formattedLink += self.myComponents[1]
                    else:
                        formattedLink += urlComponents.netloc

                    if urlComponents.path == "":
                        formattedLink += self.myComponents[2]
                    else:
                        formattedLink += urlComponents.path

                    formattedLink += urlComponents.params + urlComponents.query + urlComponents.fragment
                    self.formattedLinks.append(formattedLink)

    def getContent(self, mode, name):
        if mode in ["tag", "class", "id"]:
            if not self.parseFailed:
                htmlContent = self.urlOpened.read()
                self.strHtml = str(htmlContent)
                #print(htmlContent) #DEBUG

                # Parse HTML content
                if mode == "tag":
                    myParser = FindContentByTag()
                    myParser.setTagname(name)
                    myParser.feed(self.strHtml)
                    print(myParser.contents)

    def parse(self):
        self.formattedLinks = []
        self.parseFailed = {'status':'error', 'errorType':'unknown'}

        # Get HTML content
        #print(self.myURL) # DEBUG
        try:
            self.urlOpened = urllib.request.urlopen(self.myURL) # In python 2.7, urllib.request should be replaced by urllib
            self.parseFailed = False
        except urllib.error.HTTPError as HTTPError:
            self.parseFailed = {'status':'error', 'errorType':'HTTPError', 'errorCode':HTTPError.code, 'errorReason':HTTPError.reason, 'errorHeaders':HTTPError.headers}
        except urllib.error.URLError as URLError:
            self.parseFailed = {'status':'error', 'errorType':'URLError', 'errorReason':URLError.reason}

# Define the main class that loop on the url provided
class Cartographie:
    def __init__(self, url, limit=2):
        self.depth = 0
        self.urls = [[url, self.depth]]
        self.limitDepth = limit

    def cartographier(self):
        self.carte = '{"status":"passed","maxdepth":' + str(self.limitDepth) + ',"pages":['
        # Loop on urls until we reach a limit of depth
        while self.depth < self.limitDepth:
            for url in self.urls:
                # Focus on current depth
                if url[1] == self.depth:
                    myParser = ParseURL(url[0])
                    myParser.parse()
                    myParser.getLinks()
                    
                    # Header of the output
                    self.carte += '{"url":"' + url[0] + '",'
                    self.carte += '"depth":"' + str(self.depth+1) + '",'
                    
                    # Add the formattedLinks to the output
                    if not myParser.parseFailed:
                        self.carte += '"status":"passed",'
                        self.carte += '"links":['
                        for link in myParser.formattedLinks:
                            self.carte += '"' + link + '",'
                        if(self.carte[-1:] != "["):
                            self.carte = self.carte[:-1]
                        self.carte += ']'

                    # Handling errors raised during the urlOpen
                    else:
                        self.carte += '"status":"failed",'
                        if myParser.parseFailed["errorType"] == "unknown":
                            self.carte += '"errorType":"unknown"'
                        if myParser.parseFailed["errorType"] == "HTTPError":
                            self.carte += '"errorType":"HTTPError",'
                            self.carte += '"errorCode":"' + str(myParser.parseFailed["errorCode"]) + '",'
                            self.carte += '"errorReason":"' + myParser.parseFailed["errorReason"] + '"'
                            #TOO LONG self.carte += '"errorHeaders":' + myParser.parseFailed["errorHeaders"].as_string()
                        if myParser.parseFailed["errorType"] == "URLError":
                            self.carte += '"errorType":"URLError",'
                            self.carte += '"errorReason":"' + str(myParser.parseFailed["errorReason"]) + '"'
                    
                    # Footer of the output
                    self.carte += '},'

                    # Merge the formattedLinks to the list of urls to parse
                    uniqueLinks = list(dict.fromkeys(myParser.formattedLinks))
                    for link in uniqueLinks:
                        if link not in self.urls:
                            self.urls.append([link, self.depth+1])
            
            # End of the loop on urls
            self.depth += 1

        self.carte = self.carte[:-1]
        self.carte += "]}"
