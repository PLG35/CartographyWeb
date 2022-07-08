# -*-coding:Latin-1 -*

# Import the library
from libCartography import Cartographie as Cartography

# The rootURL is the URL of the website fro which you want to produce a map
rootUrl = "http://plgdev.fr:8000/index"

# Create instance of the worker with the rootURL as argument
carte = Cartography(rootUrl)

# Launch the crawler to produce the map
carte.cartographier()

# Print the output of the library
print(carte.carte)
