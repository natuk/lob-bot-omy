from twython import Twython, TwythonError
from lxml import html
import string
import random
import requests
import json

#load credentials from json file which looks like twitter_keys_default.json
with open("twitter_keys.json", "r") as file:
    creds = json.load(file)
# add credentials to access API
twitter = Twython(creds['APP_KEY'], creds['APP_SECRET'], creds['OAUTH_TOKEN'], creds['OAUTH_TOKEN_SECRET'])

#select a random letter
letter = random.choice(string.ascii_lowercase)
#build URL from alphabetical index page
url = "https://www.ligatus.org.uk/lob/alphabetical/" + letter
#fetch alphabetical list page for this letter
page = requests.get(url, timeout=5.000)
#success
if page.status_code == 200:
    #find out how many terms
    tree = html.fromstring(page.content)
    items = tree.xpath('//td[@class="views-field views-field-title active"]')
    noOfConcepts = len(items)
    #pick a random one
    conceptNo = random.randint(1, noOfConcepts)
    #get the link to the concept
    conceptUrl = items[conceptNo].xpath('./a/@href')
    #get the concept id from the link
    conceptId = conceptUrl[0][13:]
    #fetch item page
    conceptJson = requests.get("http://data.ligatus.org.uk/sparql?query=define%20sql%3Adescribe-mode%20%22CBD%22%20%20DESCRIBE%20%3Chttp%3A//w3id.org/lob/concept/" + conceptId + "%3E&output=application/rdf%2Bjson", timeout=5.000)
    #success
    if conceptJson.status_code == 200:
        #get json from Ligatus
        data = json.loads(conceptJson.content)
        #get the english label if it exists
        for prefLabel in data['http://w3id.org/lob/concept/' + conceptId]['http://www.w3.org/2004/02/skos/core#prefLabel']:
            if prefLabel['lang'] == "en":
                prefLabelValue = prefLabel['value']
        try:
            prefLabelValue
        except NameError:
            print("No english label for this concept")

        #get the english scope note if it exists TODO: fix protocol in data.ligatus.org.uk to include https
        for scopeNote in data['http://w3id.org/lob/concept/' + conceptId]['http://www.w3.org/2004/02/skos/core#scopeNote']:
            if scopeNote['lang'] == "en":
                scopeNoteValue = scopeNote['value']
        try:
            scopeNoteValue
        except NameError:
            print("No english scopeNote for this concept")

        #build the tweet
        tweet = prefLabelValue + "\n\n" + scopeNoteValue + "\n\nhttps://w3id.org/lob/concept/" + conceptId
        if len(tweet) > 280:
            lenReduce = 280 - len(tweet)
            tweet = prefLabelValue + "\n\n" + scopeNoteValue[:lenReduce-3] + "...\n\nhttps://w3id.org/lob/concept/" + conceptId
        print(tweet)

try:
	twitter.update_status(status=tweet)
except TwythonError as e:
	print(e)