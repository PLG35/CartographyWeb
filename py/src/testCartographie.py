# -*-coding:Latin-1 -*

# Imports
import libCartography as cart
import json

# Testing class 
class testCartographie:
    def __init__(self):
        self.outputs = []

    ###################
    # Class=FindLinks #
    ###################
    def testFindLinks(self):
        test = True

        strHtmlEmpty = "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'></head><body></body></html>"
        myParserEmpty = cart.FindLinks()
        myParserEmpty.feed(strHtmlEmpty)
        if(len(myParserEmpty.links) != 0):
            self.outputs.append({"class":"FindLinks","method":"feed(strHTML)","result":"error","message":"myParserEmpty.links n'est pas vide lorsque le code HTML ne contient aucun lien"})
            test = False

        strHtml2 = "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'></head><body><a href='http://www.test1.com'>test1</a><a href='http://www.test2.com'>test2</a></body></html>"
        myParser2 = cart.FindLinks()
        myParser2.feed(strHtml2)
        if(len(myParser2.links) != 2):
            self.outputs.append({"class":"FindLinks","method":"feed(strHTML)","result":"error","message":"myParserEmpty.links ne contient pas le bon nombre d'objets. Attendu : 2. Obtenus : " + str(len(myParser2.links))})
            test = False
        
        if(test):
            self.outputs.append({"class":"FindLinks","method":"feed(strHTML)","result":"success","message":""})

    ##########################
    # Class=FindContentByTag #
    ##########################
    def testFindContentByTag(self):
        test = True
        name = "p"
        value0 = "test2"
        value1 = "test4"

        strHtmlEmpty = "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'></head><body></body></html>"
        myParserEmpty = cart.FindContentByTag()
        myParserEmpty.setTagname(name)
        myParserEmpty.feed(strHtmlEmpty)
        if(len(myParserEmpty.contents) != 0):
            self.outputs.append({"class":"FindContentByTag","method":"feed(strHTML)","result":"error","message":"myParserEmpty.contents n'est pas vide lorsque le code HTML ne contient aucun lien"})
            test = False

        strHtml2 = "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'></head><body><p id='test1'>test2</p><p class='test3'>test4</p></body></html>"
        myParser2 = cart.FindContentByTag()
        myParser2.setTagname(name)
        myParser2.feed(strHtml2)
        if(len(myParser2.contents) != 2):
            self.outputs.append({"class":"FindContentByTag","method":"feed(strHTML)","result":"error","message":"myParser2.contents ne contient pas le bon nombre d'objets. Attendu : 2. Obtenus : " + str(len(myParser2.contents))})
            test = False
        if(myParser2.contents[0] != value0):
            self.outputs.append({"class":"FindContentByTag","method":"feed(strHTML)","result":"error","message":"myParser2.contents n'a pas le bon contenu. Le premier élément attendu est : " + value0 + ". La valeur trouvée est : " + myParser2.contents[0] + "."})
            test = False
        if(myParser2.contents[1] != value1):
            self.outputs.append({"class":"FindContentByTag","method":"feed(strHTML)","result":"error","message":"myParser2.contents n'a pas le bon contenu. Le second élément attendu est : " + value1 + ". La valeur trouvée est : " + myParser2.contents[1] + "."})
            test = False
        
        if(test):
            self.outputs.append({"class":"FindContentByTag","method":"feed(strHTML)","result":"success","message":""})

    ##################
    # Class=ParseURL #
    ##################

    # Method=parse
    def testParse(self):
        test = True

        strURLFailureHTTP = "http://www.domain.extension:1234/chemin/page.html?var1=val1&var2=val2"
        myParser = cart.ParseURL(strURLFailureHTTP)
        myParser.parse()
        if(not myParser.parseFailed or ("errorType" in myParser.parseFailed and myParser.parseFailed["errorType"] != 'URLError')):
            self.outputs.append({"class":"ParseURL","method":"parse()","result":"error","message":"La fonction n'échoue pas lorsqu'on lui fournit une adresse qui n'existe pas.\nURL : " + strURLFailureHTTP + "\nResult : " + str(myParser.parseFailed)})
            test = False

        strURLFailureURL = "htt://www.domain.extension:1234/chemin/page.html?var1=val1&var2=val2"
        myParser = cart.ParseURL(strURLFailureURL)
        myParser.parse()
        if(not myParser.parseFailed or ("errorType" in myParser.parseFailed and myParser.parseFailed["errorType"] != 'URLError')):
            self.outputs.append({"class":"ParseURL","method":"parse()","result":"error","message":"La fonction n'échoue pas lorsqu'on lui fournit une URL corrompue.\nURL : " + strURLFailureURL + "\nResult : " + str(myParser.parseFailed)})
            test = False
        
        if(test):
            self.outputs.append({"class":"ParseURL","method":"parse()","result":"success","message":""})

    # Method=getLinks
    def testGetLinks(self, testURL):
        test = True
        expectation = 5

        myParser = cart.ParseURL(testURL)
        myParser.parse()
        myParser.getLinks()
        if(len(myParser.formattedLinks) != expectation):
            self.outputs.append({"class":"ParseURL","method":"getLinks()","result":"error","message":"myParser.formattedLinks ne contient pas le bon nombre d'objets. Attendu : " + str(expectation) + ". Obtenus : " + str(len(myParser.formattedLinks))})
            test = False

        if(test):
            self.outputs.append({"class":"ParseURL","method":"getLinks()","result":"success","message":""})

    ################
    # Cartographie #
    ################
    def testCartographie(self, testURL):
        test = True
        expectation = 6

        carte = cart.Cartographie(testURL)
        carte.cartographier()
        jsonCarte = json.loads(carte.carte)
        if("pages" not in jsonCarte or len(jsonCarte["pages"]) != expectation):
            self.outputs.append({"class":"Cartographie","method":"cartographier()","result":"error","message":"La carte obtenue pour l'URL=" + testURL + " n'est pas conforme.\n" + str(carte.carte)})
            test = False

        if(test):
            self.outputs.append({"class":"Cartographie","method":"cartographier()","result":"success","message":""})

    # Display
    def launchTests(self, testURL):
        # Launch tests
        self.testFindLinks()
        self.testFindContentByTag()
        self.testParse()
        self.testGetLinks(testURL)
        self.testCartographie(testURL)

        # Provide return
        return self.outputs

# Launch the tests
myTestURL = "http://plgdev.fr/index"
myTestCartography = testCartographie()
myTestOutputs = myTestCartography.launchTests(myTestURL)
print(myTestOutputs)